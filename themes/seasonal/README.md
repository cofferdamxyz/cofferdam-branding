# Seasonal overlays

One JSON file per season. See `brand/sections/3-seasonal-themes.md` and the `cofferdam-seasonal-theme` skill. Only files with `"enabled": true` whose `window` contains today's date (UTC, `MM-DD`) are applied; two live at once fail the build. `christmas.json` is a disabled example.
