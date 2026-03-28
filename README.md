# AI Progress Dashboard

A visual dashboard to track AI tools, news, regulations, and workflows — automatically kept up to date.

## How to Use

Visit the live dashboard: **[GitHub Pages link will be added after deployment]**

No installation needed. Works in any modern browser on Windows, Mac, Chromebook, or mobile.

## Features

- **AI Tools Database** — 55+ tools across 9 categories with pricing (CAD), rankings, and pros/cons
- **Try This ASAP** — Guided recommendations for what to test, with step-by-step instructions
- **News & Resources** — Curated newsletters, news sites, Reddit communities, and YouTube channels
- **Rankings** — Best overall, best free, best value, rising stars, and per-category leaders
- **Regulations** — Track AI regulations in Canada, USA, and worldwide
- **Workflows** — How to combine AI tools for real tasks
- **Auto-Updates** — Weekly refresh via GitHub Actions

## Updating Data

All data lives in the `data/` folder as JSON files. Edit them directly on GitHub's web interface — no developer tools needed. See `docs/update-guide.md` for step-by-step instructions.

## Running Locally

Just open `index.html` in Chrome or any modern browser. If data doesn't load (CORS issue), run:

```
python -m http.server 8000
```

Then visit `http://localhost:8000`
