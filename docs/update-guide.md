# How to Update the AI Progress Dashboard

No developer tools needed — all updates can be done through GitHub's web interface.

## Adding a New AI Tool

1. Go to your repository on GitHub.com
2. Navigate to `data/tools.json`
3. Click the pencil icon (Edit this file)
4. Copy an existing tool entry and paste it at the end (before the closing `]`)
5. Update all fields for the new tool
6. Make sure the `category` matches one of the IDs in `categories.json`
7. Click "Commit changes" (green button)
8. The live site updates automatically within a few minutes

## Updating Pricing or Information

1. Navigate to `data/tools.json` on GitHub
2. Click the pencil icon
3. Find the tool you want to update (Ctrl+F to search)
4. Make your changes
5. Update the `lastVerified` date to today
6. Click "Commit changes"

## Updating News Sources

Same process — edit `data/news-sources.json` on GitHub.

## Updating Regulations

Same process — edit `data/regulations.json` on GitHub.

## Triggering a Manual Update

1. Go to your repository on GitHub.com
2. Click the "Actions" tab
3. Click "Weekly Data Refresh" in the left sidebar
4. Click "Run workflow" button
5. Click the green "Run workflow" button

## Reverting a Change

1. Go to your repository on GitHub.com
2. Click the "Commits" link (or go to the Code tab and click the commit count)
3. Find the commit you want to undo
4. Click the commit hash
5. Click "Revert" to create a new commit that undoes the change
