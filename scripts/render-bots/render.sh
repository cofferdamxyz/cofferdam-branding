#!/bin/sh
# Render a Cofferdam bot's picture: Coworkers' own TV head (the `robot-heads`
# package the bots app draws its faces with) in the brand's colours, on the
# splash gradient, 1024 px, circle-safe for GitHub.
#
#   sh scripts/render-bots/render.sh [engineering|security|ops] [idle|working|happy|searching|idle-transparent ...]
#
# Each bot has its own shape and colours (below, from tokens):
#   engineering  rectangle, shell accent #3c8aff, trim mark-a-stem #b5cff7
#   security     hexagon, shell dark mark-mono-a-stem #c4c4ca, trim accent #3c8aff
#   ops          square, shell base-tan #b8a581, trim accent #3c8aff
# `idle-transparent` is the head alone on transparency, the GitHub App's logo.
#
# Bundles with the esbuild and robot-heads under ../coworkers/node_modules
# (pnpm install there first) and screenshots with the Mac's Chrome. Writes
# assets/github/bot-<bot>-<state>.png. Change the colours here from tokens;
# never by hand in the PNG.
set -eu
HERE=$(cd "$(dirname "$0")" && pwd); ROOT=$(cd "$HERE/../.." && pwd); CW=$ROOT/../coworkers
ESB=$(ls -d "$CW"/node_modules/.pnpm/esbuild@*/node_modules/esbuild/bin/esbuild | tail -1)
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

BOT=engineering
case "${1:-}" in engineering|security|ops) BOT=$1; shift ;; esac
case $BOT in
  engineering) LOOK="shape=rectangle&color=%233c8aff&trim=%23b5cff7" ;;
  security) LOOK="shape=hexagon&color=%23c4c4ca&trim=%233c8aff" ;;
  ops) LOOK="shape=square&color=%23b8a581&trim=%233c8aff" ;;
esac

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
