# Footage

Product footage and real app captures carry the website's story (brand README, "Imagery and texture"). This section is how that footage is shot, cut, encoded and shown. Values live in `tokens/brand.json` → `web.video`; the build checks that a loop can hold its vignettes.

## What we film

Screen recordings of the Cofferdam app itself, shown on the website on a plain phone the site draws in three.js, on a studio stage (On the page). Never stock footage, people, hands or props, and never a rendering of a real handset.

| Film | Shows | Where | Form |
|---|---|---|---|
| Home | Home, then the map opening on the live listing ("Hirers can find your profile"), the founder's biggest selling point (2026-11-27) | Hero | Play-once |
| Open to work | Home's card swiping from the Work Profile (Looking for work on) to the job history the CV filled | Scene "Workers" | Loop |
| AI chat | A job described in one sentence, then what the assistant understood (the count, the pay, the start), shown by about 5 s | Scene "Hirers" | Loop |

The Developers scene keeps the mark and the hook name; it has no film.

## Capture

- The real app in dark mode on the Pixel 10, recorded and driven from the Mac (`cofferdam-footage`, `yarn take`; the workspace's `docs/runbooks/demo-edit.md`, Website takes), at native resolution and up to 60 fps. The master is the phone's own screen size (`web.video.master`, 1080 × 2424; the founder, 2026-11-27, moved the films from the iPhone's shape to the Pixel's, so the site's phone follows).
- A seeded demo account: no real names, handles, balances, passport data or locations (a made-up person, a test location set on the phone). Crop or blur nothing afterwards; if something personal is on screen, re-shoot.
- A clean status bar: 9:41, full battery, full signal (Android's demo mode; on the iOS simulator `xcrun simctl status_bar booted override --time 9:41 --batteryState charged --batteryLevel 100`).
- Touches, when the gesture matters, show as a plain white disc at 40% opacity, with no glow, no ripple and no halo.

## Edit

Two forms only.

- **Play-once** (`web.video.playOnce`): 4 s. The motion has settled by 3.5 s and the film ends on a composed frame. That end frame is also the poster, the no-script frame and the Reduce Motion frame.
- **Loop** (`web.video.loop`): at most 10 s in two or three vignettes, so the proof moment shows within the first 5 s (the founder, 2026-11-27: a reply after 7 s of typing went unseen). Each vignette changes for at most `slower` (520 ms) of tween, then holds at least 2 s on any screen with text to read. The seam sits inside a hold, so the first and last frames are the same screen.

The app's own transitions are used as recorded. Nothing is added in the edit except a plain cross-fade between vignettes: no zoom inside the screen (the founder, 2026-11-27, set the push-in aside), no blur, no wipe, no glow, no speed ramp. The camera's move belongs to the page (On the page). Colour lands once, on the proof moment (a verified tick, the Ready chip, a live state), near where the eye rests. No music, no audio track.

## Encode

- Delivery at 540 × 1212 (`web.video.delivery`, half the master, twice the largest frame the site shows), 30 fps, a keyframe every second and on every cut, BT.709 tagged. Check on a real screen that the ground stays the app's black.
- Two sources per film: HEVC (`hvc1`) first, then an H.264 fallback. No audio track.
- At most 1 MB per file (`maxBytes`); a loop that needs more is too busy.
- A poster per film as WebP or AVIF at the delivery size: the end frame for play-once films, frame 0 for loops.

## On the page

- The film plays on the screen of a phone drawn in three.js (cofferdam-pages `PhoneStage`), on a studio stage: pale paper in light, near black in dark, a soft spotlight behind the phone, a pool of light or shade below, a still grain and a vignette. As the page scrolls the camera moves in towards the screen and the phone turns to face it, from the side its scene sets (the founder, 2026-11-27, after Bleap's films). The phone is a plain dark slab with a thin border at the screen's aspect (`--cd-video-aspect`), never a real handset. The stage reserves its box (4:5) before anything loads, so nothing shifts; until the film's first frame is in, or where WebGL fails, the film shows flat in a plain frame on the stage.
- `muted`, `playsinline`, `preload="none"` below the fold, `aria-hidden` (the scene's copy carries the meaning), no `autoplay` attribute: script plays it when its scene is on screen and selected, and pauses it otherwise.
- Scroll never moves the playhead. Scroll moves the camera and the phone (`2-motion.md`, On the website).
- A loop runs longer than 5 s, so it always carries a visible pause control (WCAG 2.2.2), which also stills the phone's idle sway. Controls sit under the stage, never over the footage, where they would cover the app's own bar.
- Reduce Motion: the poster shows, flat, with a visible play control; nothing starts on its own, and the phone neither sways nor moves with the scroll.

## Placeholders

Until the real films exist, the site carries synthetic slates made by us, with nothing licensed: the app's black ground, the film's name, form, size and a running timecode, and grey blocks that change and hold on the exact rhythm above. They have the final sizes, durations and seams, so spacing, crops, posters and loop seams can be judged on the page. A real film replaces a slate file for file.
