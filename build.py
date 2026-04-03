#!/usr/bin/env python3
"""
Minimal static site builder.

Reads page files from src/pages/, applies the base template from
src/templates/base.html, and writes the result to dist/.

Page files use a simple YAML-ish front matter block (delimited by ---)
to set template variables like `title`. Everything after the front matter
is injected as `{{ content }}`.

Static assets (css/, js/) are copied to dist/ unchanged.

Usage:
    python3 build.py            # builds to ./dist
    python3 build.py --watch    # rebuilds on file changes (needs inotify)
"""

import os
import re
import shutil
import sys

SRC_DIR = os.path.join(os.path.dirname(__file__), "src")
DIST_DIR = os.path.join(os.path.dirname(__file__), "dist")
TEMPLATES_DIR = os.path.join(SRC_DIR, "templates")
PAGES_DIR = os.path.join(SRC_DIR, "pages")

# Directories that get copied as-is into dist/
STATIC_DIRS = ["css", "js"]


def parse_front_matter(text):
    """Split front matter (---) from content. Returns (vars_dict, content)."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        return {}, text

    raw = match.group(1)
    variables = {}
    for line in raw.strip().splitlines():
        key, _, value = line.partition(":")
        variables[key.strip()] = value.strip()

    content = text[match.end():]
    return variables, content


def render_template(template, variables):
    """Replace {{ key }} placeholders with values from variables dict."""
    def replacer(m):
        key = m.group(1).strip()
        return variables.get(key, m.group(0))
    return re.sub(r"\{\{\s*(\w+)\s*\}\}", replacer, template)


def build():
    # Clean dist contents (but keep the directory itself)
    if os.path.exists(DIST_DIR):
        for item in os.listdir(DIST_DIR):
            path = os.path.join(DIST_DIR, item)
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
    else:
        os.makedirs(DIST_DIR)

    # Copy static assets
    for dirname in STATIC_DIRS:
        src = os.path.join(SRC_DIR, dirname)
        dst = os.path.join(DIST_DIR, dirname)
        if os.path.isdir(src):
            shutil.copytree(src, dst)

    # Load base template
    base_path = os.path.join(TEMPLATES_DIR, "base.html")
    with open(base_path) as f:
        base_template = f.read()

    # Process each page
    page_count = 0
    for filename in sorted(os.listdir(PAGES_DIR)):
        if not filename.endswith(".html"):
            continue

        with open(os.path.join(PAGES_DIR, filename)) as f:
            raw = f.read()

        variables, content = parse_front_matter(raw)
        variables["content"] = content

        output = render_template(base_template, variables)

        out_path = os.path.join(DIST_DIR, filename)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w") as f:
            f.write(output)

        page_count += 1
        print(f"  built: {filename}")

    print(f"\nDone — {page_count} page(s) written to dist/")


if __name__ == "__main__":
    build()
