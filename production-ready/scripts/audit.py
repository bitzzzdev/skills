#!/usr/bin/env python3
"""Production-readiness audit for a project folder.

usage: audit.py [PROJECT_ROOT] [--skills-dir DIR] [--strict]

Reports MISSING, STALE and OK items for the changelog, docs, legal and
community files, then lists the skills to run in the refresh pass.
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


def check_files(root):
    wanted = [
        ("README", {"readme"}, "required"),
        ("LICENSE", {"license", "licence", "copying"}, "required"),
        ("CHANGELOG", {"changelog", "changes", "history", "release_notes"}, "required"),
        ("CONTRIBUTING", {"contributing"}, "recommended"),
        ("CODE_OF_CONDUCT", {"code_of_conduct"}, "recommended"),
        ("SECURITY", {"security"}, "recommended"),
        ("TERMS", {"terms", "terms_of_service", "tos", "terms_and_conditions"}, "if the project has users"),
        ("PRIVACY", {"privacy", "privacy_policy"}, "if the project has users"),
    ]
    found = {}
    for label, stems, need in wanted:
        hit = find(root, stems) or find(os.path.join(root, "docs"), stems) \
            or find(os.path.join(root, ".github"), stems)
        found[label] = hit
        if hit:
            add("OK", label, hit)
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
    homes = [skills_dir] if skills_dir else []
    homes += [os.path.join(root, ".claude", "skills"), os.path.expanduser("~/.claude/skills"),
              os.path.join(root, "..", "skills"), root]
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
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    if not os.path.isdir(root):
        print("not a directory: " + root, file=sys.stderr)
        return 2

    found = check_files(root)
    if found.get("CHANGELOG"):
        check_changelog(root, found["CHANGELOG"])
    if found.get("README"):
        check_readme(root, found["README"])
    scan_writing(root, [found.get(k) for k in ("README", "CHANGELOG", "TERMS", "PRIVACY", "CONTRIBUTING")], a.skills_dir)

    for status in ("MISSING", "STALE", "OK", "INFO"):
        rows = [r for r in results if r[0] == status]
        if rows:
            print("\n== %s ==" % status)
            for _, label, detail in rows:
                print("  %-26s %s" % (label, detail))
    bad = sum(1 for r in results if r[0] in ("MISSING", "STALE"))
    print("\nRefresh pass: debug-and-fix (build, tests), error-docs-lookup (warnings), "
          "human-writing (scan docs), context-rich-commits (commit).")
    print("%d item(s) need attention." % bad)
    return 1 if (a.strict and bad) else 0


if __name__ == "__main__":
    sys.exit(main())
