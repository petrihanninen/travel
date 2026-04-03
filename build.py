#!/usr/bin/env python3
"""
Minimal static site builder.

Reads page files from src/pages/, applies the base template from
src/templates/base.html, and writes the result to dist/.

Page files use a simple YAML-ish front matter block (delimited by ---)
to set template variables like `title`. Everything after the front matter
is injected as `{{ content }}`.

An index page is auto-generated from src/templates/index.html, listing
every page in src/pages/ with its title and description. Adding a new
page to src/pages/ is all that's needed — the index updates automatically.

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


def build_page_card(filename, title, description):
    """Generate an HTML card for a single page entry on the index."""
    href = f"/{filename}"
    desc_html = f'<p class="card-desc">{description}</p>' if description else ""
    return f"""      <a href="{href}" class="index-card">
        <h3 class="card-title">{title}</h3>
        {desc_html}
        <span class="card-arrow">&rarr;</span>
      </a>"""


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

    # ── First pass: process all pages & collect metadata ──
    pages_meta = []
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

        # Collect metadata for the index
        pages_meta.append({
            "filename": filename,
            "title": variables.get("title", filename.replace(".html", "").replace("-", " ").title()),
            "description": variables.get("description", ""),
        })

    # ── Generate auto-index page ──
    index_template_path = os.path.join(TEMPLATES_DIR, "index.html")
    if os.path.exists(index_template_path):
        with open(index_template_path) as f:
            index_template = f.read()

        cards_html = "\n".join(
            build_page_card(p["filename"], p["title"], p["description"])
            for p in pages_meta
        )

        index_output = render_template(index_template, {"page_cards": cards_html})

        with open(os.path.join(DIST_DIR, "index.html"), "w") as f:
            f.write(index_output)

        print(f"  built: index.html (auto-generated, {len(pages_meta)} link(s))")
        page_count += 1

    print(f"\nDone — {page_count} page(s) written to dist/")


if __name__ == "__main__":
    build()
