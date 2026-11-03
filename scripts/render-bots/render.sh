#!/bin/sh
# Render a Cofferdam bot's picture: Coworkers' own TV head (the `robot-heads`
# package the bots app draws its faces with) in Cofferdam Cerulean, trim
# `mark-a-stem`, on the splash gradient, 1024 px, circle-safe for GitHub.
#
#   sh scripts/render-bots/render.sh [idle|working|happy ...]
#
# Bundles with the esbuild and robot-heads under ../coworkers/node_modules
# (pnpm install there first) and screenshots with the Mac's Chrome. Writes
# assets/github/bot-engineering-<state>.png. Change the colours in entry.tsx
# from tokens; never by hand in the PNG.
set -eu
HERE=$(cd "$(dirname "$0")" && pwd); ROOT=$(cd "$HERE/../.." && pwd); CW=$ROOT/../coworkers
ESB=$(ls -d "$CW"/node_modules/.pnpm/esbuild@*/node_modules/esbuild/bin/esbuild | tail -1)
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
cd "$HERE" && NODE_PATH="$CW/node_modules" "$ESB" entry.tsx --bundle --outfile=bundle.js --jsx=automatic --define:process.env.NODE_ENV='"production"' --log-level=warning
for st in "${@:-idle}"; do
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --window-size=1024,1024 \
    --virtual-time-budget=4000 --screenshot="$ROOT/assets/github/bot-engineering-$st.png" "file://$HERE/avatar.html?state=$st&size=900" 2>/dev/null
  echo "assets/github/bot-engineering-$st.png"
done
rm -f bundle.js
