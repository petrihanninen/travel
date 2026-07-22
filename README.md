# Travel Slideshows

Personal travel research site. Each page is a full-screen scrollable slideshow comparing destinations, activities, accommodation options, etc. for an upcoming trip.

Hosted on GitHub Pages at [https://travel.petrihanninen.com](https://travel.petrihanninen.com).

## Build & deploy

- `python3 build.py` — builds the site to `dist/` (Python stdlib only, no dependencies)
- Push to `main` — GitHub Actions (`.github/workflows/pages.yml`) runs `python3 build.py` and deploys `dist/` to GitHub Pages

See `CLAUDE.md` for content structure and slideshow authoring conventions.
