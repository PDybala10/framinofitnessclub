#!/bin/zsh
# Rebuild static/css/tailwind.css after template changes.
# Requires the Tailwind standalone CLI (see docs/INSTALL.md, lot 9).
cd "$(dirname "$0")"
.tools/tailwindcss -i static/css/input.css -o static/css/tailwind.css \
  --content "./templates/**/*.html,./**/templates/**/*.html" --minified
