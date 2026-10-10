import React, { useEffect, useRef, useState } from 'react';
import { AccessibilityInfo, StyleSheet, useColorScheme, useWindowDimensions } from 'react-native';
import Animated, {
  Easing,
  useAnimatedProps,
  useAnimatedStyle,
  useSharedValue,
  withTiming,
  type SharedValue,
} from 'react-native-reanimated';
import Svg, { Defs, LinearGradient, Polygon, Rect, Stop } from 'react-native-svg';

import { MARK_PIECES, type MarkPiece } from './cofferdamMark';
import {
  BUMP_AT,
  HOLD_END,
  PIECE_START,
  SPLASH_TIMING,
  clamp01,
  easeInOut,
  easeOutCubic,
  settleBump,
  wipePoints,
} from './splashMath';

const AnimatedPolygon = Animated.createAnimatedComponent(Polygon);

// The native splash must be a plain colour with the SAME value, so the first frame is seamless.
const THEME = {
  light: { base: '#3C8AFF', from: '#60A6FF', to: '#2262E8' },
  dark: { base: '#121A33', from: '#1B2645', to: '#0B1124' },
} as const;

function Piece({ piece, t, dark }: { piece: MarkPiece; t: SharedValue<number>; dark: boolean }) {
  const start = PIECE_START[piece.id];
  const animatedProps = useAnimatedProps(() => {
    const p = easeOutCubic(clamp01((t.value - start) / SPLASH_TIMING.dur));
    const edge = piece.from + (piece.to - piece.from) * p;
    return { points: wipePoints(piece.pts, piece.axis, edge, piece.keepGreater) };
  });
  return <AnimatedPolygon animatedProps={animatedProps} fill={dark ? piece.dark : piece.light} />;
}

export type CofferdamSplashProps = {
  /** Fires once the first frame is laid out. Hide the native splash here. */
  onMounted?: () => void;
  /** Keep the finished mark on screen until the app is ready (fonts, session, ...). Default: true. */
  ready?: boolean;
  /** Fires after the exit fade. Unmount the splash here. */
  onDone: () => void;
  /** Mark width as a fraction of the screen width. Default: 0.74. */
  markScale?: number;
};

export function CofferdamSplash({ onMounted, ready = true, onDone, markScale = 0.74 }: CofferdamSplashProps) {
  const { width, height } = useWindowDimensions();
  const dark = useColorScheme() === 'dark';
  const theme = dark ? THEME.dark : THEME.light;
  const size = width * markScale;

  const t = useSharedValue(0); // draw timeline in ms
  const exit = useSharedValue(0); // 0 -> 1 during the exit
  const [drawn, setDrawn] = useState(false);

  const onDoneRef = useRef(onDone);
  onDoneRef.current = onDone;

  // Draw + settle. Honours the system "reduce motion" setting (jumps straight to the finished mark).
  useEffect(() => {
    let timer: ReturnType<typeof setTimeout> | undefined;
    let cancelled = false;
    AccessibilityInfo.isReduceMotionEnabled().then((reduced) => {
      if (cancelled) return;
      if (reduced) {
        t.value = HOLD_END;
        timer = setTimeout(() => setDrawn(true), 400);
      } else {
        t.value = withTiming(HOLD_END, { duration: HOLD_END, easing: Easing.linear });
        timer = setTimeout(() => setDrawn(true), HOLD_END);
      }
    });
    return () => {
      cancelled = true;
      if (timer) clearTimeout(timer);
    };
  }, [t]);

  // Exit once drawing is finished AND the app is ready.
  useEffect(() => {
    if (!drawn || !ready) return;
    exit.value = withTiming(1, { duration: SPLASH_TIMING.exitDur, easing: Easing.inOut(Easing.cubic) });
    const timer = setTimeout(() => onDoneRef.current(), SPLASH_TIMING.exitDur);
    return () => clearTimeout(timer);
  }, [drawn, ready, exit]);

  const rootStyle = useAnimatedStyle(() => ({ opacity: 1 - exit.value }));
  const gradientStyle = useAnimatedStyle(() => ({ opacity: clamp01(t.value / 700) }));
  const markStyle = useAnimatedStyle(() => ({
    transform: [{ scale: 1 + settleBump(t.value) + 0.08 * exit.value }],
  }));

  return (
    <Animated.View
      accessible
      accessibilityLabel="Cofferdam"
      style={[StyleSheet.absoluteFill, { backgroundColor: theme.base }, rootStyle]}
      onLayout={() => onMounted?.()}
    >
      <Animated.View style={[StyleSheet.absoluteFill, gradientStyle]} pointerEvents="none">
        <Svg width="100%" height="100%">
          <Defs>
            <LinearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
              <Stop offset="0" stopColor={theme.from} />
              <Stop offset="1" stopColor={theme.to} />
            </LinearGradient>
          </Defs>
          <Rect width="100%" height="100%" fill="url(#bg)" />
        </Svg>
      </Animated.View>

      <Animated.View
        pointerEvents="none"
        style={[
          { position: 'absolute', left: (width - size) / 2, top: (height - size) / 2, width: size, height: size },
          markStyle,
        ]}
      >
        <Svg width={size} height={size} viewBox="0 0 1024 1024">
          {MARK_PIECES.map((piece) => (
            <Piece key={piece.id} piece={piece} t={t} dark={dark} />
          ))}
        </Svg>
      </Animated.View>
    </Animated.View>
  );
}
