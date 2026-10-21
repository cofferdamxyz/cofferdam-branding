# Footage

Product footage and real app captures carry the website's story (brand README, "Imagery and texture"). This section is how that footage is shot, cut, encoded and shown. Values live in `tokens/brand.json` → `web.video`; the build checks that a loop can hold its vignettes.

## What we film

Screen recordings of the Cofferdam app itself, shown on the website inside its device frame on the stone stage. Never rendered phones, composited props, stock footage or people.

| Film | Shows | Where | Form |
|---|---|---|---|
| Home | The balance bar and Home's cards, the balance settling | Hero | Play-once |
| Open to work | The map with the range disc, the Open to work toggle, a funded job arriving | Scene "Workers" | Loop |
| AI chat | A job described in one sentence, what the assistant understood, the confirm step | Scene "Hirers" | Loop |

The Developers scene keeps the mark and the hook name; it has no film.

## Capture

- The real app in dark mode, on a device or the iOS simulator, at native resolution and 60 fps. The master is the phone's own screen size (`web.video.master`, 1179 × 2556).
- A seeded demo account: no real names, handles, balances, passport data or locations. Crop or blur nothing afterwards; if something personal is on screen, re-shoot.
- A clean status bar: 9:41, full battery, full signal (`xcrun simctl status_bar booted override --time 9:41 --batteryState charged --batteryLevel 100`).
- Touches, when the gesture matters, show as a plain white disc at 40% opacity, with no glow, no ripple and no halo.

## Edit

Two forms only.

- **Play-once** (`web.video.playOnce`): 4 s. The motion has settled by 3.5 s and the film ends on a composed frame. That end frame is also the poster, the no-script frame and the Reduce Motion frame.
- **Loop** (`web.video.loop`): 15 s in three vignettes of about 5 s. Each vignette changes for at most `slower` (520 ms) of tween, then holds at least 2 s on any screen with text to read. The seam sits inside a hold, so the first and last frames are the same screen.

The app's own transitions are used as recorded. Nothing is added in the edit except a plain cross-fade between vignettes: no blur, no wipe, no glow, no zoom, no speed ramp. Colour lands once, on the proof moment (a verified tick, the Ready chip, a live state), near where the eye rests. No music, no audio track.

## Encode

- Delivery at 590 × 1278 (`web.video.delivery`, half the master, twice the largest frame the site shows), 30 fps, a keyframe every second and on every cut, BT.709 tagged. Check on a real screen that the ground stays the app's black.
- Two sources per film: HEVC (`hvc1`) first, then an H.264 fallback. No audio track.
- At most 1 MB per file (`maxBytes`); a loop that needs more is too busy.
- A poster per film as WebP or AVIF at the delivery size: the end frame for play-once films, frame 0 for loops.

## On the page

- The film sits in the device frame at `--cd-video-aspect`, on the scene's stone stage. The page reserves its box before the file loads, so nothing shifts.
- `muted`, `playsinline`, `preload="none"` below the fold, `aria-hidden` (the scene's copy carries the meaning), no `autoplay` attribute: script plays it when its scene is on screen and selected, and pauses it otherwise.
- Scroll never moves the playhead. Scroll may move the frame (`2-motion.md`, On the website).
- Reduce Motion: the poster shows, with a visible play control; nothing starts on its own.

## Placeholders

Until the real films exist, the site carries synthetic slates made by us, with nothing licensed: the app's black ground, the film's name, form, size and a running timecode, and grey blocks that change and hold on the exact rhythm above. They have the final sizes, durations and seams, so spacing, crops, posters and loop seams can be judged on the page. A real film replaces a slate file for file.
