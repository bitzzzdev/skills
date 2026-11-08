#!/usr/bin/env python3
"""Check and pull updates for google-seo-skill from git.

Usage:
    python scripts/update_seo_skill.py [--check-only] [--force] [--skills-dir DIR]

Checks upstream repository (https://github.com/mikezupper/google-seo-skill).
If a new commit is available in git, pulls it, cleans em dashes and emoji
per human-writing rules, preserves frontmatter and conditional triggers,
and updates the local skill folder.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

UPSTREAM_URL = "https://github.com/mikezupper/google-seo-skill"
SKILL_NAME = "google-seo-skill"

SKILL_DESCRIPTION = (
    "Apply Google's official SEO and generative AI search (AEO/GEO) guidance when writing, "
    "reviewing, or auditing web pages, blog posts, or site architecture. Covers crawling, "
    "indexing, canonicalization, structured data, search appearance, and AI Overviews. "
    "Use when working on a web project where public search ranking and discoverability are "
    "needed. If working on a personal project, private repository, internal tool, or any site "
    "where search indexing is not desired, avoid this skill and configure noindex or disallow "
    "rules instead."
)


def run_cmd(cmd, cwd=None):
    try:
        res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=60)
        return res.returncode, res.stdout.strip(), res.stderr.strip()
    except Exception as exc:
        return 1, "", str(exc)


def get_upstream_head():
    code, out, err = run_cmd(["git", "ls-remote", UPSTREAM_URL, "HEAD"])
    if code == 0 and out:
        parts = out.split()
        if parts:
            return parts[0]
    return None


def get_local_commit(skill_dir):
    marker = os.path.join(skill_dir, ".upstream_commit")
    if os.path.isfile(marker):
        try:
            with open(marker, "r", encoding="utf-8") as f:
                return f.read().strip()
        except OSError:
            pass
    return None


def clean_human_writing(text):
    text = re.sub(r"(\*\*[^*]+\*\*)\s*[\u2014\u2015]\s*", r"\1: ", text)
    text = re.sub(r"\s*[\u2014\u2015]\s*", ": ", text)
    text = text.replace("\u2014", "-")
    text = text.replace("\u2013", "-")
    text = text.replace("\U0001F50D ", "")
    text = text.replace("google-seo-fundamentals", SKILL_NAME)
    return text


def update_skill(skill_dir, new_commit):
    with tempfile.TemporaryDirectory() as tmp_dir:
        clone_path = os.path.join(tmp_dir, "repo")
        code, _, err = run_cmd(["git", "clone", "--depth", "1", UPSTREAM_URL, clone_path])
        if code != 0:
            print("error: failed to clone upstream repo: " + err, file=sys.stderr)
            return False

        os.makedirs(skill_dir, exist_ok=True)
        ref_dir = os.path.join(skill_dir, "references")
        os.makedirs(ref_dir, exist_ok=True)

        # Copy and clean references
        upstream_refs = os.path.join(clone_path, "references")
        if os.path.isdir(upstream_refs):
            for ref_file in os.listdir(upstream_refs):
                if ref_file.endswith(".md"):
                    src_file = os.path.join(upstream_refs, ref_file)
                    dst_file = os.path.join(ref_dir, ref_file)
                    with open(src_file, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    content = clean_human_writing(content)
                    with open(dst_file, "w", encoding="utf-8") as f:
                        f.write(content)

        # Copy and clean LICENSE
        src_lic = os.path.join(clone_path, "LICENSE")
        if os.path.isfile(src_lic):
            shutil.copy2(src_lic, os.path.join(skill_dir, "LICENSE"))

        # Copy and clean README.md
        src_readme = os.path.join(clone_path, "README.md")
        if os.path.isfile(src_readme):
            with open(src_readme, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            content = clean_human_writing(content)
            with open(os.path.join(skill_dir, "README.md"), "w", encoding="utf-8") as f:
                f.write(content)

        # Build SKILL.md with standardized frontmatter and clean body
        src_skill = os.path.join(clone_path, "SKILL.md")
        if os.path.isfile(src_skill):
            with open(src_skill, "r", encoding="utf-8", errors="ignore") as f:
                raw_skill = f.read()
            body = raw_skill
            if raw_skill.startswith("---"):
                parts = raw_skill.split("---", 2)
                if len(parts) >= 3:
                    body = parts[2].lstrip()
            body = clean_human_writing(body)

            # Insert conditional trigger guidance in When to apply
            if "## When to apply this skill" in body and "## When to avoid this skill" not in body:
                avoid_section = (
                    "## When to avoid this skill\n\n"
                    "Do NOT use this skill when:\n"
                    "- Working on a personal project, private repository, internal dashboard, staging site, or enterprise intranet.\n"
                    "- The project explicitly requires no indexing (`noindex`, password protected, or internal use only). "
                    "In these cases, do not optimize for rankings: verify that `noindex` tags, `X-Robots-Tag: noindex` headers, "
                    "or robots disallow rules are properly configured to prevent indexing.\n"
                    "- The project is not a public website (for example: native mobile apps, desktop apps, Minecraft mods, "
                    "shaderpacks, private APIs, CLI tools). Non-web projects need store listing copy, registry descriptions, "
                    "or package metadata instead.\n\n"
                )
                body = body.replace("## When to apply this skill\n", "## When to apply this skill\n\n" + avoid_section)

            full_skill = f"---\nname: {SKILL_NAME}\ndescription: {SKILL_DESCRIPTION}\n---\n\n{body}"
            with open(os.path.join(skill_dir, "SKILL.md"), "w", encoding="utf-8") as f:
                f.write(full_skill)

        # Write upstream commit hash
        with open(os.path.join(skill_dir, ".upstream_commit"), "w", encoding="utf-8") as f:
            f.write(new_commit + "\n")

        return True


def main():
    parser = argparse.ArgumentParser(description="Check and pull updates for google-seo-skill from git.")
    parser.add_argument("--check-only", action="store_true", help="only check if an update is available")
    parser.add_argument("--force", action="store_true", help="pull even if commits match")
    parser.add_argument("--skills-dir", help="base directory containing google-seo-skill")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    if args.skills_dir:
        target_dir = os.path.join(os.path.abspath(args.skills_dir), SKILL_NAME)
    else:
        target_dir = os.path.join(root, SKILL_NAME)

    remote_head = get_upstream_head()
    if not remote_head:
        print("warning: could not reach upstream git repository to check for updates")
        return 0

    local_commit = get_local_commit(target_dir)

    if local_commit == remote_head and not args.force:
        print(f"google-seo-skill is up to date with git ({remote_head[:7]}).")
        return 0

    if args.check_only:
        print(f"Update available: {local_commit[:7] if local_commit else 'none'} -> {remote_head[:7]}")
        return 0

    print(f"Pulling google-seo-skill update from git ({remote_head[:7]})...")
    ok = update_skill(target_dir, remote_head)
    if ok:
        print("Successfully updated google-seo-skill.")
        # Also sync to runtime dir if present
        runtime_skill = os.path.expanduser(f"~/.gemini/antigravity-cli/skills/{SKILL_NAME}")
        if os.path.isdir(os.path.dirname(runtime_skill)) and os.path.abspath(target_dir) != os.path.abspath(runtime_skill):
            try:
                shutil.copytree(target_dir, runtime_skill, dirs_exist_ok=True)
                print(f"Synchronized to runtime directory: {runtime_skill}")
            except Exception as e:
                print(f"warning: runtime sync skipped: {e}")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
