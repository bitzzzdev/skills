#!/usr/bin/env python3
"""Production-readiness audit for a project folder.

usage: audit.py [PROJECT_ROOT] [--skills-dir DIR] [--type TYPE] [--strict]
                [--personal] [--no-indexing] [--force-release] [--skip-legal]
                [--skip-files FILES]

Guesses the project type, audits required, recommended, optional, and user-excluded
documentation assets for enterprise readiness, checks skill folder git status,
and lists which skills to USE and SKIP.
Exit status is 0 unless --strict is given and required items are missing or stale.
"""
import argparse
import json
import os
import re
import subprocess
import sys

SKIP = {".git", "node_modules", "dist", "build", ".venv", "venv", "__pycache__", ".next", "vendor"}
results = []


def add(status, label, detail="", tier=""):
    results.append((status, label, detail, tier))


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
    """Return True if package manifest or project markers indicate private or personal project."""
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
    cargo = os.path.join(root, "Cargo.toml")
    if os.path.isfile(cargo):
        text = read(cargo).lower()
        if "publish = false" in text:
            return True
    for marker in (".private", ".personal", ".internal"):
        if os.path.isfile(os.path.join(root, marker)):
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
    use = ["debug-and-fix (build, tests, lint)", "systematic-issue-sweep (sweep workspace for defect recurrences)",
           "error-docs-lookup (warnings and deprecations)", "human-writing (scan docs)", "context-rich-commits (commit)"]
    priority = []
    if is_skill_installed("agent-self-awareness", root, skills_dir):
        priority.append("agent-self-awareness (set execution mode and research gate from the active model tier)")
    if is_skill_installed("context-search", root, skills_dir):
        priority.append("context-search (recover prior agent sessions and verify them against git)")
    use = priority + use
    skip = []

    # Check 3D / WebGL for website
    has_three = False
    pj = os.path.join(root, "package.json")
    if os.path.isfile(pj):
        has_three = '"three"' in read(pj).lower()

    if "website" in types:
        if is_personal or no_indexing:
            skip.append("google-seo-skill (personal or internal project, avoid ranking optimization, verify noindex or robots disallow)")
            skip.append("SEO and search ranking (references/seo.md, ensure noindex is configured)")
        else:
            if is_skill_installed("google-seo-skill", root, skills_dir):
                use.append("google-seo-skill (official Google SEO and AI search audit)")
            else:
                use.append("SEO and performance check (references/seo.md)")
        use.append("accessibility pass")
        if has_three:
            if is_skill_installed("threejs-awwwards-site", root, skills_dir):
                use.append("threejs-awwwards-site (Three.js and WebGL scene checks)")
            else:
                skip.append("threejs-awwwards-site not installed, skip")
        else:
            skip.append("threejs-awwwards-site (no Three.js or WebGL detected)")
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
        legal = "personal or internal project: consumer terms and privacy optional unless external users onboarded"
    elif types and all(t in ("shaderpack", "library-cli", "game-mod") for t in types):
        legal = "terms and privacy usually not needed, license, credits, and contributing are"

    return use, skip, legal


def count_env_vars_in_code(root):
    env_in_code = set()
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x not in SKIP]
        for f in files:
            if f.endswith((".js", ".ts", ".tsx", ".jsx", ".py", ".go", ".rb", ".rs")):
                t = read(os.path.join(d, f))
                env_in_code |= set(re.findall(r"process\.env\.([A-Z][A-Z0-9_]{2,})", t))
                env_in_code |= set(re.findall(r"os\.environ(?:\.get)?[\[(]\s*['\"]([A-Z][A-Z0-9_]{2,})", t))
                env_in_code |= set(re.findall(r"os\.getenv\(\s*['\"]([A-Z][A-Z0-9_]{2,})", t))
    env_in_code -= {"NODE_ENV", "PATH", "HOME", "CI", "PORT"}
    return env_in_code


def check_files(root, types, is_personal=False, force_release=False, user_exclusions=None):
    if user_exclusions is None:
        user_exclusions = set()

    has_hosted_users = any(t in ("website", "api", "mobile-native", "bot") for t in types)
    env_vars = count_env_vars_in_code(root)

    # Base list of files and their search stems
    candidates = [
        ("README", {"readme"}),
        ("LICENSE", {"license", "licence", "copying"}),
        ("CHANGELOG", {"changelog", "changes", "history", "release_notes"}),
        ("TERMS", {"terms", "terms_of_service", "tos", "terms_and_conditions", "terms_of_use"}),
        ("PRIVACY", {"privacy", "privacy_policy"}),
        ("CREDITS", {"credits", "notice", "third_party_notices", "acknowledgements", "attributions"}),
        ("SECURITY", {"security", "security_policy"}),
        ("CONTRIBUTING", {"contributing"}),
        ("CODE_OF_CONDUCT", {"code_of_conduct", "conduct"}),
    ]

    found = {}
    for label, stems in candidates:
        hit = find(root, stems) or find(os.path.join(root, "docs"), stems) \
            or find(os.path.join(root, ".github"), stems)
        found[label] = hit

        if hit:
            content = read(os.path.join(root, hit))
            meta_m = re.search(
                r"\b(choose (one|a license) before (publishing|releasing)|"
                r"license (is )?not selected yet|"
                r"the license has not been (selected|chosen))\b",
                content,
                re.I,
            )
            if meta_m:
                add("STALE", label, "%s contains assistant meta-instruction ('%s'). Write as project owner." % (hit, meta_m.group(0)))
            else:
                add("OK", label, hit)
            continue

        # Item is not present on disk. Determine classification:
        if label in user_exclusions:
            add("USER-EXCLUDED", label, "excluded by user preference")
        elif force_release:
            if label in ("README", "LICENSE", "CHANGELOG", "TERMS", "PRIVACY", "CREDITS", "SECURITY"):
                add("REQUIRED", label, "required for full corporate release")
            else:
                add("RECOMMENDED", label, "recommended for corporate release")
        elif is_personal:
            if label in ("README", "CHANGELOG"):
                add("REQUIRED", label, "required for project orientation")
            elif label == "LICENSE":
                add("REQUIRED", label, "internal or proprietary notice required")
            elif label == "CREDITS":
                add("RECOMMENDED", label, "recommended for third-party compliance")
            else:
                add("OPTIONAL", label, "omitted for personal or internal project")
        else:
            # Public project
            if label in ("README", "LICENSE", "CHANGELOG"):
                add("REQUIRED", label, "required for public release")
            elif label in ("TERMS", "PRIVACY"):
                if has_hosted_users:
                    add("REQUIRED", label, "required for hosted service with users")
                else:
                    add("OPTIONAL", label, "not needed without hosted users or accounts")
            elif label == "CREDITS":
                if has_hosted_users:
                    add("REQUIRED", label, "required for third-party dependency attribution")
                else:
                    add("RECOMMENDED", label, "recommended for third-party dependency attribution")
            elif label == "SECURITY":
                if has_hosted_users:
                    add("REQUIRED", label, "required for vulnerability disclosure and SLA")
                else:
                    add("RECOMMENDED", label, "recommended for vulnerability reporting")
            elif label in ("CONTRIBUTING", "CODE_OF_CONDUCT"):
                add("RECOMMENDED", label, "recommended for open-source collaboration")
            else:
                add("OPTIONAL", label, "optional")

    # Check .env.example
    env_hit = find(root, {"env.example", "env.sample"}) or (
        ".env.example" if os.path.isfile(os.path.join(root, ".env.example")) else None
    ) or (
        ".env.sample" if os.path.isfile(os.path.join(root, ".env.sample")) else None
    )
    if env_hit:
        add("OK", ".env.example", env_hit)
    elif env_vars:
        add("REQUIRED", ".env.example", "environment variables used in code but no template found")
    else:
        add("OPTIONAL", ".env.example", "no environment variables detected in code")

    # Check CI workflow
    if os.path.isdir(os.path.join(root, ".github", "workflows")):
        add("OK", "CI workflow", "GitHub Actions workflows present")
    elif os.path.isfile(os.path.join(root, ".gitlab-ci.yml")):
        add("OK", "CI workflow", "GitLab CI configuration present")
    else:
        add("RECOMMENDED", "CI workflow", "recommended automated build and test pipeline")

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
    meta_m = re.search(
        r"\b(choose (one|a license) before (publishing|releasing)|"
        r"license (is )?not selected yet|"
        r"the license has not been (selected|chosen)|"
        r"replace (this|these) with your|"
        r"note to (the )?(developer|maintainer|user|author))\b",
        text,
        re.I,
    )
    if meta_m:
        add("STALE", "README assistant meta-instruction", "contains '%s'. Write as project owner." % meta_m.group(0))
    for heading, rx in (("install", r"install|getting started|setup"), ("usage", r"usage|run|quick ?start|example")):
        if not re.search(rx, text, re.I):
            add("STALE", "README section", "missing " + heading)
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
    env_in_code = count_env_vars_in_code(root)
    if env_in_code:
        documented = text + read(os.path.join(root, ".env.example")) + read(os.path.join(root, ".env.sample"))
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
    ap = argparse.ArgumentParser(description="Audit codebase for production readiness.")
    ap.add_argument("root", nargs="?", default=".", help="project root directory")
    ap.add_argument("--skills-dir", help="custom skills directory")
    ap.add_argument("--type", help="override detected type, comma separated: " + ", ".join(TYPES))
    ap.add_argument("--personal", action="store_true", help="mark project as personal or internal")
    ap.add_argument("--no-indexing", action="store_true", help="project should avoid search indexing")
    ap.add_argument("--force-release", action="store_true", help="enforce full corporate release suite even if private")
    ap.add_argument("--skip-legal", action="store_true", help="ignore legal files when user opts out")
    ap.add_argument("--skip-files", help="comma-separated list of document labels to exclude (e.g. terms,privacy)")
    ap.add_argument("--strict", action="store_true", help="exit with status 1 if required items are missing or stale")
    a = ap.parse_args()

    root = os.path.abspath(a.root)
    if not os.path.isdir(root):
        print("not a directory: " + root, file=sys.stderr)
        return 2

    # Determine project scope and release mode
    is_force_release = a.force_release
    is_detected_private = check_personal_or_private(root)
    is_personal = (a.personal or is_detected_private) and not is_force_release
    no_indexing = a.no_indexing or is_personal

    # Determine user-excluded documents
    user_exclusions = set()
    if a.skip_legal:
        user_exclusions.update({"TERMS", "PRIVACY", "LICENSE", "CREDITS", "SECURITY", "CONTRIBUTING", "CODE_OF_CONDUCT"})
    if a.skip_files:
        for f in a.skip_files.split(","):
            f_clean = f.strip().upper().replace("-", "_")
            if f_clean:
                user_exclusions.add(f_clean)

    types = [t.strip() for t in a.type.split(",")] if a.type else detect_types(root)
    unknown = [t for t in types if t not in TYPES]
    if unknown:
        print("unknown type: " + ", ".join(unknown), file=sys.stderr)
        return 2

    print("Project type: " + ", ".join(types))
    if is_force_release:
        print("Project scope: corporate release mode (full enterprise documentation suite enforced)")
    elif is_personal:
        print("Project scope: personal or internal (consumer legal docs and search indexing omitted)")

    found = check_files(root, types, is_personal=is_personal, force_release=is_force_release, user_exclusions=user_exclusions)
    if found.get("CHANGELOG"):
        check_changelog(root, found["CHANGELOG"])
    if found.get("README"):
        check_readme(root, found["README"])

    doc_files = [found.get(k) for k in ("README", "CHANGELOG", "TERMS", "PRIVACY", "LICENSE", "CREDITS", "SECURITY", "CONTRIBUTING", "CODE_OF_CONDUCT")]
    scan_writing(root, doc_files, a.skills_dir)
    check_skill_updates(root, a.skills_dir)

    # Print distinct sections
    req_rows = [r for r in results if r[0] == "REQUIRED"]
    rec_rows = [r for r in results if r[0] == "RECOMMENDED"]
    opt_rows = [r for r in results if r[0] == "OPTIONAL"]
    exc_rows = [r for r in results if r[0] == "USER-EXCLUDED"]
    stale_rows = [r for r in results if r[0] == "STALE"]
    ok_rows = [r for r in results if r[0] == "OK"]
    info_rows = [r for r in results if r[0] == "INFO"]

    print("\n== REQUIRED ==")
    if req_rows:
        for _, label, detail, _ in req_rows:
            print("  %-26s %s" % (label, detail))
    else:
        print("  All required files present")

    if rec_rows:
        print("\n== RECOMMENDED ==")
        for _, label, detail, _ in rec_rows:
            print("  %-26s %s" % (label, detail))

    if opt_rows:
        print("\n== OPTIONAL ==")
        for _, label, detail, _ in opt_rows:
            print("  %-26s %s" % (label, detail))

    if exc_rows:
        print("\n== USER-EXCLUDED ==")
        for _, label, detail, _ in exc_rows:
            print("  %-26s %s" % (label, detail))

    if stale_rows:
        print("\n== STALE ==")
        for _, label, detail, _ in stale_rows:
            print("  %-26s %s" % (label, detail))

    if ok_rows:
        print("\n== OK ==")
        for _, label, detail, _ in ok_rows:
            print("  %-26s %s" % (label, detail))

    if info_rows:
        print("\n== INFO ==")
        for _, label, detail, _ in info_rows:
            print("  %-26s %s" % (label, detail))

    use, skip, legal = report_skills(types, root, a.skills_dir, is_personal=is_personal, no_indexing=no_indexing)
    print("\n== USE ==")
    for u in dict.fromkeys(use):
        print("  " + u)
    print("\n== SKIP ==")
    for k in skip:
        print("  " + k)

    req_count = len(req_rows)
    stale_count = len(stale_rows)
    rec_count = len(rec_rows)
    exc_count = len(exc_rows)
    bad = req_count + stale_count

    print("\nLegal: " + legal)
    print("%d required item(s) missing, %d stale item(s) need attention." % (req_count, stale_count))
    if rec_count:
        print("%d recommended item(s) omitted." % rec_count)
    if exc_count:
        print("%d item(s) excluded by user preference." % exc_count)

    return 1 if (a.strict and bad) else 0


if __name__ == "__main__":
    sys.exit(main())
