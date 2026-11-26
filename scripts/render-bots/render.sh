#!/bin/sh
# Render a Cofferdam bot's picture: Coworkers' own TV head (the `robot-heads`
# package the bots app draws its faces with) in the brand's colours, on the
# splash gradient, 1024 px, circle-safe for GitHub.
#
#   sh scripts/render-bots/render.sh [engineering|security|ops|marketing] [idle|working|happy|searching|idle-transparent ...]
#
# Each bot's shape and colours come from `bots` in tokens/brand.json, read
# resolved from dist/brand.resolved.json (run `node scripts/build.mjs` first):
#   engineering  rectangle, shell accent, trim mark-a-stem
#   security     hexagon, shell mark-mono-a-stem (dark), trim accent
#   ops          square, shell base-tan, trim accent
#   marketing    circle, shell base-pink, trim accent
# The bots app reads the same looks from dist/bots/bot-looks.generated.ts.
# `idle-transparent` is the head alone on transparency, the GitHub App's logo.
#
# Bundles with the esbuild and robot-heads under ../coworkers/node_modules
# (pnpm install there first; COWORKERS=/path overrides the folder) and
# screenshots with the Mac's Chrome. Writes assets/github/bot-<bot>-<state>.png.
# Change the looks in tokens/brand.json; never by hand in the PNG.
set -eu
HERE=$(cd "$(dirname "$0")" && pwd); ROOT=$(cd "$HERE/../.." && pwd); CW=${COWORKERS:-$ROOT/../coworkers}
ESB=$(ls -d "$CW"/node_modules/.pnpm/esbuild@*/node_modules/esbuild/bin/esbuild | tail -1)
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

BOT=engineering
case "${1:-}" in engineering|security|ops|marketing) BOT=$1; shift ;; esac
LOOK=$(node -e '
  const b = require(process.argv[1]).bots?.[process.argv[2]];
  if (!b) { console.error("no bot " + process.argv[2] + " in dist/brand.resolved.json; run node scripts/build.mjs"); process.exit(1); }
  process.stdout.write(new URLSearchParams({ shape: b.shape, color: b.color, trim: b.trimColor }).toString());
' "$ROOT/dist/brand.resolved.json" "$BOT")

cd "$HERE" && NODE_PATH="$CW/node_modules" "$ESB" entry.tsx --bundle --outfile=bundle.js --jsx=automatic --define:process.env.NODE_ENV='"production"' --log-level=warning
for st in "${@:-idle}"; do
  page=avatar.html; face=$st
  if [ "$st" = idle-transparent ]; then page=avatar-transparent.html; face=idle; fi
  out="$ROOT/assets/github/bot-$BOT-$st.png"
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --window-size=1024,1024 \
    --default-background-color=00000000 --virtual-time-budget=4000 --screenshot="$out" \
    "file://$HERE/$page?state=$face&size=900&$LOOK" 2>/dev/null
  echo "assets/github/bot-$BOT-$st.png"
done
rm -f bundle.js
