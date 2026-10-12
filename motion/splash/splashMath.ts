// Pure timeline + geometry helpers for the Cofferdam splash.
// Everything used inside Reanimated callbacks is marked 'worklet'.
import type { PieceId } from './cofferdamMark';

// All times in milliseconds.
export const SPLASH_TIMING = {
  start: 40, // quiet beat before the first piece — the app is ready fast, so the mark starts at once
  dur: 200, // time to draw one piece
  gap: 20, // pause between pieces: only ever one piece moving at a time
  bumpDur: 220, // settle bump after the last piece lands
  hold: 40, // short hold on the finished mark
  exitDur: 220, // fade/scale-out into the app
  gradientFadeIn: 400, // the ground's gradient fades in over the first draw
} as const;

// Draw order follows one continuous path around the mark:
// up the left stem -> across the top arm -> down the right stem -> back along the bottom arm.
export const PIECE_ORDER: PieceId[] = ['a-stem', 'a-arm', 'b-stem', 'b-arm'];

export const PIECE_START: Record<PieceId, number> = {
  'a-stem': SPLASH_TIMING.start,
  'a-arm': SPLASH_TIMING.start + 1 * (SPLASH_TIMING.dur + SPLASH_TIMING.gap),
  'b-stem': SPLASH_TIMING.start + 2 * (SPLASH_TIMING.dur + SPLASH_TIMING.gap),
  'b-arm': SPLASH_TIMING.start + 3 * (SPLASH_TIMING.dur + SPLASH_TIMING.gap),
};

export const BUMP_AT = SPLASH_TIMING.start + 4 * SPLASH_TIMING.dur + 3 * SPLASH_TIMING.gap; // 900
export const HOLD_END = BUMP_AT + SPLASH_TIMING.bumpDur + SPLASH_TIMING.hold; // 1160

export function clamp01(x: number): number {
  'worklet';
  return x < 0 ? 0 : x > 1 ? 1 : x;
}

export function easeOutCubic(x: number): number {
  'worklet';
  const k = 1 - x;
  return 1 - k * k * k;
}

export function easeInOut(x: number): number {
  'worklet';
  return 3 * x * x - 2 * x * x * x;
}

/** Scale pulse applied to the whole mark once every piece has landed (0 before BUMP_AT). */
export function settleBump(tMs: number): number {
  'worklet';
  if (tMs < BUMP_AT) return 0;
  const u = clamp01((tMs - BUMP_AT) / SPLASH_TIMING.bumpDur);
  return 0.035 * Math.sin(Math.PI * easeInOut(u));
}

/**
 * Wipe reveal: clip a polygon against one axis-aligned half-plane and return an SVG
 * `points` string. axis 0 = x, 1 = y. keepGreater keeps the side with larger coordinates.
 * (Used by the web replay; the native splash animates a Path through `wipePath`.)
 */
export function wipePoints(pts: number[][], axis: 0 | 1, edge: number, keepGreater: boolean): string {
  'worklet';
  let s = '';
  const n = pts.length;
  let prev = pts[n - 1];
  let prevIn = keepGreater ? prev[axis] >= edge : prev[axis] <= edge;
  for (let i = 0; i < n; i++) {
    const cur = pts[i];
    const curIn = keepGreater ? cur[axis] >= edge : cur[axis] <= edge;
    if (curIn !== prevIn) {
      const t = (edge - prev[axis]) / (cur[axis] - prev[axis]);
      s += prev[0] + t * (cur[0] - prev[0]) + ',' + (prev[1] + t * (cur[1] - prev[1])) + ' ';
    }
    if (curIn) s += cur[0] + ',' + cur[1] + ' ';
    prev = cur;
    prevIn = curIn;
  }
  return s === '' ? '0,0 0,0 0,0' : s;
}

/**
 * The same clip as an SVG path `d`. react-native-svg converts a Polygon's `points`
 * into a path only while React renders, so UI-thread animated props must drive
 * Path's `d` directly — animating `points` reaches the native view and is ignored.
 */
export function wipePath(pts: number[][], axis: 0 | 1, edge: number, keepGreater: boolean): string {
  'worklet';
  const parts = wipePoints(pts, axis, edge, keepGreater).trim().split(' ');
  let d = 'M' + parts[0];
  for (let i = 1; i < parts.length; i++) d += ' L' + parts[i];
  return d + ' Z';
}
