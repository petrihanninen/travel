# Travel Slideshows

Personal travel research site. Each page is a full-screen scrollable slideshow comparing destinations, activities, accommodation options, etc. for an upcoming trip.

## What this repo does

Static site that builds HTML slideshows from `src/pages/`. A Python build script (`build.py`) applies a base template and generates an index page. Output goes to `dist/`, served via nginx in Docker. Deployed as a container image to GHCR on push to main.

## Content: the slideshows

The only real content so far is `src/pages/alpine-trip.html` — use it as the reference for tone, structure, and visual style when creating new pages.

Each slideshow is a single HTML file using these slide types (CSS classes defined in `src/css/styles.css`):

- **`slide--cover`** — Title slide. Big gradient heading (`<h1>`), subtitle, and meta pills.
- **`slide--hero`** — Full-bleed background image (Unsplash URL) with overlaid section label, heading, tagline, and pill tags. Used to introduce each destination/topic.
- **`slide--split`** — Two-column: image on one side, text on the other. Use `style="direction: rtl"` on the section to flip image to the right. Used for detailed content (hike descriptions, activity lists, practicalities).
- **`slide--text`** — Full-width text slide, centered `div.inner`. Used for weather data, comparison grids, tables, and recommendations.

### Content patterns in alpine-trip

Each destination follows this sequence of slides:

1. **Hero** — destination intro with Unsplash background, accent color, tagline, pills
2. **Split** — full-day hikes/activities (image left, details right). Each activity has a `.hike-name`, `.stat` pills (distance, time, type), and `.hike-desc`.
3. **Split (flipped)** — half-day highlights, food & stay, season notes (image right, lists left)
4. **Weather text slide** — two-column `.weather-grid` with May and June `.weather-month` cards, each with `.wx-row` items (icon + label + value), plus a `.wx-note` takeaway box

After all destinations: comparison grid, weather comparison table, recommendation slide, next-steps slide.

### Style notes

- Dark theme (`--bg: #1a1a1e`). Each destination gets its own CSS custom-property accent color.
- Fonts: Syne (headings, bold/display), Inter (body).
- Images from Unsplash with `w=1920&q=80` (hero) or `w=1200&q=80` (split). Always include `auto=format&fit=crop`.
- Tone is personal, opinionated, concise. Not a guidebook — more like notes to yourself or a travel companion. Short punchy sentences.
- Use emoji only in weather data rows as icons.

## Project structure

```
src/
  pages/          # Slideshow HTML files (front matter: title, description)
  templates/
    base.html     # Wraps page content, adds nav dots + JS
    index.html    # Auto-generated index listing all pages
  css/styles.css  # All slide type styles, responsive breakpoints
  js/main.js      # Nav dots, scroll observer, keyboard nav
build.py          # Static site builder (front matter parsing, template rendering)
dist/             # Build output (gitignored)
```

## Adding a new slideshow

1. Create `src/pages/my-trip.html` with front matter:
   ```
   ---
   title: Page Title
   description: One-line summary for the index card
   ---
   ```
2. Write slide sections using the CSS classes above.
3. Run `python3 build.py` — outputs to `dist/` and updates the index.

## Build & deploy

- `python3 build.py` — build locally
- `docker compose up --build` — build and serve at localhost:80
- Push to `main` — GitHub Actions builds and pushes image to `ghcr.io/petrihanninen/travel`
