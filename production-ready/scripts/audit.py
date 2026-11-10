#!/usr/bin/env python3
"""Production-readiness audit for a project folder.

usage: audit.py [PROJECT_ROOT] [--skills-dir DIR] [--type TYPE] [--strict]
                [--personal] [--no-indexing]

Guesses the project type, reports MISSING, STALE and OK items for the
changelog, docs, legal and community files, then lists which skills to USE
and which to SKIP for that type and indexing requirements.
Exit status is 0 unless --strict is given and something is MISSING or STALE.
"""
import argparse
import json
import os
import re
import subprocess
import sys

SKIP = {".git", "node_modules", "dist", "build", ".venv", "venv", "__pycache__", ".next", "vendor"}
results = []


def add(status, label, detail=""):
    results.append((status, label, detail))


def find(root, names):
    """Return the first existing file whose lowercase stem matches one of names."""
    try:
        entries = os.listdir(root)
    except OSError:
        return None
    for e in sorted(entries):
        stem = os.path.splitext(e)[0].lower().replace("-", "_")
        if stem in names and os.path.isfile(os.path.join(root, e)):
            return e
    return None


def run(cmd, cwd):
    try:
        out = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=30)
        return out.stdout.strip() if out.returncode == 0 else ""
    except Exception:
        return ""


def read(path):
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            return f.read()
    except OSError:
        return ""


def manifest_version(root):
    pj = os.path.join(root, "package.json")
    if os.path.isfile(pj):
        try:
            return json.loads(read(pj)).get("version"), "package.json"
        except ValueError:
            pass
    for name, rx in (("pyproject.toml", r'^\s*version\s*=\s*"([^"]+)"'),
                     ("Cargo.toml", r'^\s*version\s*=\s*"([^"]+)"'),
                     ("VERSION", r"^\s*(\S+)\s*$")):
        p = os.path.join(root, name)
        if os.path.isfile(p):
            m = re.search(rx, read(p), re.M)
            if m:
                return m.group(1), name
    return None, None


def check_personal_or_private(root):
    """Return True if package manifest or project markers indicate private/personal project."""
    pj = os.path.join(root, "package.json")
    if os.path.isfile(pj):
        try:
            data = json.loads(read(pj))
            if data.get("private") is True:
                return True
        except ValueError:
            pass
    pyproj = os.path.join(root, "pyproject.toml")
    if os.path.isfile(pyproj):
        text = read(pyproj).lower()
        if 'classifiers = ["private' in text or "private = true" in text:
            return True
    return False


def get_skill_homes(root, skills_dir=None):
    """Return list of existing directories where skills may be installed."""
    homes = [skills_dir] if skills_dir else []
    homes += [
        os.path.join(root, ".gemini", "skills"),
        os.path.expanduser("~/.gemini/antigravity-cli/skills"),
        os.path.expanduser("~/.gemini/antigravity-cli/builtin/skills"),
        os.path.expanduser("~/.gemini/config/skills"),
        os.path.expanduser("~/.gemini/skills"),
        os.path.join(root, ".copilot", "skills"),
        os.path.expanduser("~/.copilot/skills"),
        os.path.join(root, ".agents", "skills"),
        os.path.expanduser("~/.agents/skills"),
        os.path.join(root, ".claude", "skills"),
        os.path.expanduser("~/.claude/skills"),
        os.path.join(root, "skills"),
        os.path.join(root, "..", "skills"),
        root
    ]
    seen = set()
    valid = []
    for h in homes:
        if h and h not in seen and os.path.isdir(h):
            seen.add(h)
            valid.append(h)
    return valid


def check_skill_updates(root, skills_dir=None):
    homes = get_skill_homes(root, skills_dir)
    checked = set()
    for h in homes:
        real = os.path.realpath(h)
        if real in checked:
            continue
        checked.add(real)
        git_dir = os.path.join(real, ".git")
        if not os.path.exists(git_dir):
            continue
        status = run(["git", "status", "--short", "--branch"], real)
        if not status:
            continue
        lines = status.splitlines()
        first_line = lines[0] if lines else ""
        parent_name = os.path.basename(os.path.dirname(real))
        folder_name = os.path.basename(real)
        display_name = f"{parent_name}/{folder_name}" if parent_name else folder_name
        label = f"Skill folder ({display_name})"
        if "behind" in first_line:
            add("STALE", label, "behind upstream: " + first_line.lstrip("# ").strip())
        elif "ahead" in first_line:
            add("INFO", label, "ahead of upstream: " + first_line.lstrip("# ").strip())
        elif len(lines) > 1:
            add("INFO", label, "local changes present (%d files)" % (len(lines) - 1))
        else:
            add("OK", label, "up to date (" + first_line.lstrip("# ").strip() + ")")


def is_skill_installed(name, root, skills_dir=None):
    homes = get_skill_homes(root, skills_dir)
    return any(os.path.isdir(os.path.join(h, name)) for h in homes)


TYPES = ("website", "mobile-native", "desktop", "game-mod", "shaderpack", "library-cli", "bot", "api")


def detect_types(root):
    """Return a list of project types guessed from marker files and dependencies."""
    found = []
    names, text = set(), ""
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x not in SKIP]
        if d.count(os.sep) - root.count(os.sep) > 3:
            dirs[:] = []
        for f in files:
            names.add(f)
            if f in ("package.json", "pyproject.toml", "requirements.txt", "Cargo.toml", "go.mod",
                     "build.gradle", "build.gradle.kts", "pubspec.yaml", "Gemfile", "composer.json"):
                text += "\n" + read(os.path.join(d, f)).lower()
            if f.endswith((".fsh", ".vsh", ".glsl")):
                names.add("__shader__")
    has = lambda *ws: any(w in text for w in ws)
    if "AndroidManifest.xml" in names or "pubspec.yaml" in names or "Info.plist" in names \
            or any(n.endswith(".xcodeproj") for n in names) or has("react-native", '"expo"', "com.android.application"):
        found.append("mobile-native")
    if "fabric.mod.json" in names or "mods.toml" in names or "neoforge.mods.toml" in names:
        found.append("game-mod")
    if "__shader__" in names and any(os.path.isdir(os.path.join(root, x)) for x in ("shaders", "assets")):
        found.append("shaderpack")
    if has('"electron"', "tauri", "pyqt", "pyside", "wpf") or "tauri.conf.json" in names:
        found.append("desktop")
    if has("discord.js", "discord.py", "discord-py", "telegraf", "python-telegram-bot", "@slack/bolt", "slack_bolt"):
        found.append("bot")
    web = has('"next"', '"nuxt"', '"astro"', "gatsby", "@sveltejs/kit", "@remix-run", "wordpress", "jekyll", "hugo") \
        or "index.html" in names or "wp-config.php" in names
    if web and "mobile-native" not in found and "game-mod" not in found:
        found.append("website")
    if has("express", "fastify", "fastapi", "flask", "django", "rails", "gin-gonic", "actix", "axum", "koa") \
            and "website" not in found and "bot" not in found:
        found.append("api")
    if not found:
        found.append("library-cli")
    return found


SPECIFIC = {
    "mobile-native": ("android-app-dev", "native Android project"),
    "game-mod": ("minecraft-fabric-mod", "Minecraft mod project"),
    "shaderpack": ("iris-shaderpack-dev", "Minecraft shaderpack"),
}


def report_skills(types, root, skills_dir, is_personal=False, no_indexing=False):
    use = ["debug-and-fix (build, tests, lint)", "error-docs-lookup (warnings and deprecations)",
           "human-writing (scan docs)", "context-rich-commits (commit)"]
    skip = []

    # Check 3D / WebGL for website
    has_three = False
    pj = os.path.join(root, "package.json")
    if os.path.isfile(pj):
        has_three = '"three"' in read(pj).lower()

    if "website" in types:
        if is_personal or no_indexing:
            skip.append("google-seo-skill (personal/internal project or no indexing needed; avoid ranking optimization, verify noindex or robots disallow)")
            skip.append("SEO and search ranking (references/seo.md; personal/internal project, ensure noindex is configured)")
        else:
            if is_skill_installed("google-seo-skill", root, skills_dir):
                use.append("google-seo-skill (official Google SEO & AI search audit)")
            else:
                use.append("SEO and performance check (references/seo.md)")
        use.append("accessibility pass")
        if has_three:
            if is_skill_installed("threejs-awwwards-site", root, skills_dir):
                use.append("threejs-awwwards-site (Three.js/WebGL scene checks)")
            else:
                skip.append("threejs-awwwards-site not installed, skip")
        else:
            skip.append("threejs-awwwards-site (no Three.js/WebGL detected)")
    else:
        kinds = "/".join(t for t in types)
        listing = {"mobile-native": "store listing text", "desktop": "landing page only if one exists",
                   "game-mod": "mod page text", "shaderpack": "mod page text", "bot": "bot listing text",
                   "api": "docs site only", "library-cli": "registry description"}
        alt = ", ".join(sorted({listing[t] for t in types if t in listing}))
        skip.append("google-seo-skill (%s has no public search-ranked pages, write %s instead)" % (kinds, alt or "a clear description"))
        skip.append("SEO and Core Web Vitals (%s has no search-ranked pages), write %s instead" % (kinds, alt or "a clear description"))
        skip.append("threejs-awwwards-site (not a website)")

    if "mobile-native" in types or "desktop" in types:
        use.append("accessibility pass")

    for t in types:
        if t in SPECIFIC:
            name, why = SPECIFIC[t]
            if is_skill_installed(name, root, skills_dir):
                use.append("%s (%s)" % (name, why))
            else:
                skip.append("%s not installed, skip" % name)

    others = {"android-app-dev": "mobile-native", "minecraft-fabric-mod": "game-mod", "iris-shaderpack-dev": "shaderpack"}
    for name, t in others.items():
        if t not in types:
            skip.append("%s (project is not %s)" % (name, t))

    legal = "terms and privacy needed if the project has users or collects data"
    if is_personal:
        legal = "personal project: terms and privacy optional unless external users onboarded"
    elif types and all(t in ("shaderpack", "library-cli", "game-mod") for t in types):
        legal = "terms and privacy usually not needed, license and contributing are"

    return use, skip, legal


def check_files(root, is_personal=False):
    wanted = [
        ("README", {"readme"}, "required"),
        ("LICENSE", {"license", "licence", "copying"}, "required"),
        ("CHANGELOG", {"changelog", "changes", "history", "release_notes"}, "required"),
        ("CONTRIBUTING", {"contributing"}, "recommended"),
        ("CODE_OF_CONDUCT", {"code_of_conduct"}, "recommended"),
        ("SECURITY", {"security"}, "recommended"),
        ("TERMS", {"terms", "terms_of_service", "tos", "terms_and_conditions"}, "if the project has users" if not is_personal else "optional for personal projects"),
        ("PRIVACY", {"privacy", "privacy_policy"}, "if the project has users" if not is_personal else "optional for personal projects"),
    ]
    found = {}
    for label, stems, need in wanted:
        hit = find(root, stems) or find(os.path.join(root, "docs"), stems) \
            or find(os.path.join(root, ".github"), stems)
        found[label] = hit
        if hit:
            add("OK", label, hit)
        else:
            if is_personal and label in ("TERMS", "PRIVACY"):
                add("INFO", label, "omitted for personal project")
            else:
                add("MISSING", label, need)
    if os.path.isfile(os.path.join(root, ".env.example")) or os.path.isfile(os.path.join(root, ".env.sample")):
        add("OK", ".env.example")
    elif any(re.search(r"\.env", n) for n in os.listdir(root)):
        add("MISSING", ".env.example", "a .env exists but no example file")
    if os.path.isdir(os.path.join(root, ".github", "workflows")):
        add("OK", "CI workflow")
    else:
        add("MISSING", "CI workflow", "recommended")
    return found


def check_changelog(root, name):
    text = read(os.path.join(root, name))
    version, source = manifest_version(root)
    heads = re.findall(r"^##\s*\[?v?(\d+\.\d+[^\]\s]*)\]?", text, re.M)
    latest = heads[0] if heads else None
    if "unreleased" in text.lower():
        add("OK", "Unreleased section", "present")
    else:
        add("STALE", "Unreleased section", "none, add one for pending changes")
    if version and latest and version != latest:
        add("STALE", "Changelog version", "%s says %s, changelog top entry is %s" % (source, version, latest))
    elif version and not latest:
        add("STALE", "Changelog version", "no version headings found, manifest is %s" % version)
    elif version:
        add("OK", "Changelog version", version)

    if os.path.isdir(os.path.join(root, ".git")):
        tag = run(["git", "describe", "--tags", "--abbrev=0"], root)
        if tag:
            n = run(["git", "rev-list", "--count", tag + "..HEAD"], root)
            if n and n != "0":
                add("STALE", "Commits since " + tag, "%s commit(s), check they are in the changelog" % n)
            else:
                add("OK", "Commits since " + tag, "none")
        else:
            add("INFO", "Git tags", "no release tags yet")
        last = run(["git", "log", "-1", "--format=%ct", "--", name], root)
        head = run(["git", "log", "-1", "--format=%ct"], root)
        if last and head and int(head) - int(last) > 30 * 86400:
            add("STALE", "Changelog age", "not touched in over 30 days of project activity")


def check_readme(root, name):
    text = read(os.path.join(root, name))
    if len(text.strip()) < 200:
        add("STALE", "README length", "very short")
    for heading, rx in (("install", r"install|getting started|setup"), ("usage", r"usage|run|quick ?start|example")):
        if not re.search(rx, text, re.I):
            add("MISSING", "README section", heading)
    bad = []
    for ref in set(re.findall(r"`([\w./-]+/[\w./-]+\.\w{1,5})`", text)):
        if not ref.startswith(("http", "~", "/")) and not os.path.exists(os.path.join(root, ref)):
            bad.append(ref)
    if bad:
        add("STALE", "README file references", "not found: " + ", ".join(sorted(bad)[:8]))
    pj = os.path.join(root, "package.json")
    if os.path.isfile(pj):
        try:
            scripts = json.loads(read(pj)).get("scripts", {})
            missing = [s for s in set(re.findall(r"npm run ([\w:-]+)", text)) if s not in scripts]
            if missing:
                add("STALE", "README npm scripts", "not in package.json: " + ", ".join(sorted(missing)))
        except ValueError:
            pass
    env_in_code = set()
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x not in SKIP]
        for f in files:
            if f.endswith((".js", ".ts", ".tsx", ".jsx", ".py", ".go", ".rb")):
                t = read(os.path.join(d, f))
                env_in_code |= set(re.findall(r"process\.env\.([A-Z][A-Z0-9_]{2,})", t))
                env_in_code |= set(re.findall(r"os\.environ(?:\.get)?[\[(]\s*['\"]([A-Z][A-Z0-9_]{2,})", t))
                env_in_code |= set(re.findall(r"os\.getenv\(\s*['\"]([A-Z][A-Z0-9_]{2,})", t))
    env_in_code -= {"NODE_ENV", "PATH", "HOME", "CI", "PORT"}
    if env_in_code:
        documented = text + read(os.path.join(root, ".env.example"))
        undoc = sorted(v for v in env_in_code if v not in documented)
        if undoc:
            add("STALE", "Undocumented env vars", ", ".join(undoc[:10]))


def scan_writing(root, files, skills_dir):
    homes = get_skill_homes(root, skills_dir)
    scanner = None
    for h in homes:
        p = os.path.join(h, "human-writing", "scripts", "scan.py")
        if os.path.isfile(p):
            scanner = p
            break
    if not scanner:
        add("INFO", "human-writing scan", "skill not found, skipped")
        return
    paths = [os.path.join(root, f) for f in files if f and os.path.isfile(os.path.join(root, f))]
    if not paths:
        return
    r = subprocess.run([sys.executable, scanner, "--hard-only"] + paths, capture_output=True, text=True)
    if r.returncode == 0:
        add("OK", "human-writing scan", "no em dashes or emoji in docs")
    else:
        add("STALE", "human-writing scan", "hard hits found, run the scanner and fix them")
        sys.stdout.write(r.stdout[-1500:])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--skills-dir")
    ap.add_argument("--type", help="override detected type, comma separated: " + ", ".join(TYPES))
    ap.add_argument("--personal", action="store_true", help="mark project as personal/internal (avoids public SEO/terms)")
    ap.add_argument("--no-indexing", action="store_true", help="project should avoid search indexing")
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    if not os.path.isdir(root):
        print("not a directory: " + root, file=sys.stderr)
        return 2

    is_personal = a.personal or check_personal_or_private(root)
    no_indexing = a.no_indexing or is_personal

    types = [t.strip() for t in a.type.split(",")] if a.type else detect_types(root)
    unknown = [t for t in types if t not in TYPES]
    if unknown:
        print("unknown type: " + ", ".join(unknown), file=sys.stderr)
        return 2
    print("Project type: " + ", ".join(types))
    if is_personal or no_indexing:
        print("Project scope: personal / internal (search indexing avoided)")
    found = check_files(root, is_personal=is_personal)
    if found.get("CHANGELOG"):
        check_changelog(root, found["CHANGELOG"])
    if found.get("README"):
        check_readme(root, found["README"])
    scan_writing(root, [found.get(k) for k in ("README", "CHANGELOG", "TERMS", "PRIVACY", "CONTRIBUTING")], a.skills_dir)
    check_skill_updates(root, a.skills_dir)

    for status in ("MISSING", "STALE", "OK", "INFO"):
        rows = [r for r in results if r[0] == status]
        if rows:
            print("\n== %s ==" % status)
            for _, label, detail in rows:
                print("  %-26s %s" % (label, detail))
    bad = sum(1 for r in results if r[0] in ("MISSING", "STALE"))
    use, skip, legal = report_skills(types, root, a.skills_dir, is_personal=is_personal, no_indexing=no_indexing)
    print("\n== USE ==")
    for u in dict.fromkeys(use):
        print("  " + u)
    print("\n== SKIP ==")
    for k in skip:
        print("  " + k)
    print("\nLegal: " + legal)
    print("%d item(s) need attention." % bad)
    return 1 if (a.strict and bad) else 0


if __name__ == "__main__":
    sys.exit(main())
