# Cofferdam splash (Expo)

Draws the official mark one piece at a time along a single continuous path, settles with a small pulse,
holds until the app is ready, then fades into the app. About 2.4 s total, plus any extra wait for your app to load.

## Install
    npx expo install react-native-reanimated react-native-svg expo-splash-screen react-native-worklets

(`react-native-worklets` is only needed on Reanimated 4; `expo install` picks the right versions for your SDK.
Make sure the Reanimated babel plugin is configured as described in its docs.)

## Files
- `cofferdamMark.ts`  generated geometry (1024 viewBox) + per-piece wipe direction and colours
- `splashMath.ts`     timing constants, easing, wipe-clipping (worklets)
- `CofferdamSplash.tsx` the overlay component
- `App.example.tsx`   wiring with expo-splash-screen
- `app.json.snippet`  native splash = plain colour only (no image), so frame 0 matches the overlay exactly

## Tuning
All timings live in `SPLASH_TIMING` (splashMath.ts). Draw order is `PIECE_ORDER`. Mark size is the `markScale` prop.

## Notes
- Respects the system "reduce motion" setting (shows the finished mark briefly, then exits).
- Dark mode uses the dark palette from the icon previews.
- If your SDK's splash plugin insists on an image, use a 1x1 transparent PNG.
- Written against current Expo/Reanimated APIs but not yet run on a device: test on iOS and Android dev builds.
