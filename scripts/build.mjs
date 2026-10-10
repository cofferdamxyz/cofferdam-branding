#!/usr/bin/env node
/**
 * cofferdam-branding build — the ONE place brand values turn into code.
 *
 *   node scripts/build.mjs                 # build for today's date
 *   node scripts/build.mjs --date=2026-12-10   # preview what a date would ship
 *   node scripts/build.mjs --season=christmas  # force a season (or --season=none)
 *   node scripts/build.mjs --check         # validate + contrast only, write nothing
 *
 * Inputs : tokens/tokens.json, tokens/brand.json, themes/seasonal/*.json,
 *          brand/README.md, brand/sections/*.md, components/**, fonts/*
 * Outputs: dist/brand.resolved.json        — every value resolved, season applied (any consumer)
 *          dist/app/brand.generated.ts      — cofferdam-app (React Native)
 *          dist/pages/brand.generated.css   — cofferdam-pages (Next.js / Tailwind v4)
 *          dist/tokens.css                  — plain CSS custom properties
 *          dist/design-system/project/**    — the Claude Design System artifact files
 *
 * No dependencies: Node 20+.
 */
import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

import { contrast, over, parseColor, resolveColors, withAlpha } from './lib/color.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const args = Object.fromEntries(
  process.argv.slice(2).map((a) => {
    const [k, v] = a.replace(/^--/, '').split('=');
    return [k, v ?? true];
  }),
);

const readJSON = (p) => JSON.parse(fs.readFileSync(path.join(ROOT, p), 'utf8'));
const write = (p, text) => {
  if (args.check) return;
  const abs = path.join(ROOT, p);
  fs.mkdirSync(path.dirname(abs), { recursive: true });
  fs.writeFileSync(abs, text);
};
const copy = (from, to) => {
  if (args.check) return;
  const abs = path.join(ROOT, to);
  fs.mkdirSync(path.dirname(abs), { recursive: true });
  fs.copyFileSync(path.join(ROOT, from), abs);
};
const camel = (s) => s.replace(/-([a-z0-9])/g, (_, c) => c.toUpperCase());
const px = (v) => (typeof v === 'number' ? v : parseFloat(String(v)));

const errors = [];
const warnings = [];

// ── 1. Load ───────────────────────────────────────────────────────────────
const baseTokens = readJSON('tokens/tokens.json');
const brand = readJSON('tokens/brand.json');
const seasonsDir = path.join(ROOT, 'themes/seasonal');
const seasons = fs
  .readdirSync(seasonsDir)
  .filter((f) => f.endsWith('.json'))
  .map((f) => ({ file: `themes/seasonal/${f}`, ...JSON.parse(fs.readFileSync(path.join(seasonsDir, f), 'utf8')) }));

// ── 2. Pick the active season ─────────────────────────────────────────────
const today = args.date ? new Date(`${args.date}T12:00:00Z`) : new Date();
const mmdd = `${String(today.getUTCMonth() + 1).padStart(2, '0')}-${String(today.getUTCDate()).padStart(2, '0')}`;
const inWindow = ({ start, end }) => (start <= end ? mmdd >= start && mmdd <= end : mmdd >= start || mmdd <= end);
const forced = args.season ?? brand.season?.force ?? null;
let season = null;
if (forced && forced !== 'none') {
  season = seasons.find((s) => s.id === forced);
  if (!season) errors.push(`season "${forced}" not found in themes/seasonal/`);
} else if (!forced) {
  const live = seasons.filter((s) => s.enabled && s.window && inWindow(s.window));
  if (live.length > 1) errors.push(`overlapping seasons live on ${mmdd}: ${live.map((s) => s.id).join(', ')}`);
  season = live[0] ?? null;
}

// ── 3. Apply the overlay ──────────────────────────────────────────────────
const tokens = structuredClone(baseTokens);
const effBrand = structuredClone(brand);
if (season) {
  for (const [name, val] of Object.entries(season.color ?? {})) {
    const tok = tokens.color.tokens.find((t) => t.name === name);
    if (!tok) {
      errors.push(`${season.file}: colour "${name}" is not a token in tokens.json`);
      continue;
    }
    const prev = typeof tok.value === 'string' ? Object.fromEntries(tokens.color.themes.map((t) => [t.id, tok.value])) : tok.value;
    tok.value = typeof val === 'string' ? val : { ...prev, ...val };
  }
  const merge = (a, b) => {
    for (const [k, v] of Object.entries(b ?? {})) {
      if (k.startsWith('$')) continue;
      a[k] = v && typeof v === 'object' && !Array.isArray(v) ? merge(a[k] ?? {}, v) : v;
    }
    return a;
  };
  merge(effBrand.defaults, season.defaults);
  merge(effBrand.web, season.web);
  for (const a of season.assets?.wallpapers ?? []) if (!fs.existsSync(path.join(ROOT, a))) errors.push(`${season.file}: missing asset ${a}`);
}

// ── 4. Resolve + validate ─────────────────────────────────────────────────
let colors;
try {
  colors = resolveColors(tokens.color);
} catch (e) {
  errors.push(e.message);
  colors = {};
}
const names = new Set();
for (const fam of ['color', 'spacing', 'radius', 'shadow', 'opacity']) {
  for (const t of tokens[fam]?.tokens ?? []) {
    if (!/^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$/.test(t.name)) errors.push(`bad token name "${t.name}"`);
    if (names.has(t.name)) errors.push(`duplicate token name "${t.name}"`);
    names.add(t.name);
    if (!t.usage) warnings.push(`token "${t.name}" has no usage note`);
  }
}
for (const f of tokens.type.fonts) if (!fs.existsSync(path.join(ROOT, f.file))) errors.push(`font file missing: ${f.file}`);
const tokenNames = new Set(tokens.color.tokens.map((t) => t.name));
for (const a of brand.accents) if (!tokenNames.has(a.token)) errors.push(`accent ${a.id} points at unknown token ${a.token}`);
for (const b of brand.backgrounds) for (const k of ['image', 'webTexture']) if (b[k] && !fs.existsSync(path.join(ROOT, b[k]))) errors.push(`background ${b.id}: missing ${b[k]}`);

// Contrast: text tokens on the grounds they are documented for. Pairs the
// SOURCE already misses are known (kept exact, flagged in their usage notes);
// anything else below the floor fails the build.
const KNOWN = new Set(['dark:fg-muted-2', 'light:fg-muted-2', 'light:warning', 'light:success']);
const TEXT = ['fg', 'fg-muted', 'fg-muted-2', 'accent', 'danger', 'warning', 'success', 'info'];
const GROUNDS = ['bg', 'web-bg', 'card', 'surface-2'];
const report = [];
for (const theme of Object.keys(colors)) {
  for (const t of TEXT) {
    const fg = parseColor(colors[theme][t]);
    const worst = Math.min(...GROUNDS.map((g) => contrast(fg, parseColor(colors[theme][g]))));
    const floor = 4.5;
    const key = `${theme}:${t}`;
    report.push({ theme, token: t, worst });
    if (worst < floor) {
      if (KNOWN.has(key)) warnings.push(`contrast ${key} ${worst}:1 (known, from source)`);
      else errors.push(`contrast ${key} is ${worst}:1 on its grounds — needs ≥ ${floor}:1`);
    }
  }
  // Control outlines must be findable: 3:1 against every ground a control sits on.
  if (colors[theme]['border-control']) {
    const bc = Math.min(...['bg', 'card', 'surface-2'].map((g) => contrast(parseColor(colors[theme]['border-control']), parseColor(colors[theme][g]))));
    if (bc < 3) errors.push(`contrast ${theme}:border-control is ${bc}:1 — needs ≥ 3:1 on bg, card and surface-2`);
  }
  // Mark faces must read as graphics (3:1): greyscale mark on bg / surface-2; dark colour mark on the navy tile.
  const markGrounds = [['mark-mono-', ['bg', 'surface-2', 'tile-mono-from', 'tile-mono-to']], ...(theme === 'dark' ? [['mark-', ['splash-bg', 'splash-gradient-from', 'splash-gradient-to']]] : [])];
  for (const [prefix, grounds] of markGrounds) {
    for (const piece of ['a-stem', 'a-arm', 'b-stem', 'b-arm']) {
      const v = colors[theme][prefix + piece];
      if (!v) continue;
      const worst = Math.min(...grounds.map((g) => contrast(parseColor(v), parseColor(colors[theme][g]))));
      if (worst < 3) errors.push(`contrast ${theme}:${prefix}${piece} is ${worst}:1 — needs ≥ 3:1 on ${grounds.join(', ')}`);
    }
  }
  // Accent text on its own dim fill (the Ready chip / verified pill).
  const chip = contrast(parseColor(colors[theme].accent), over(parseColor(colors[theme]['accent-dim']), parseColor(colors[theme].bg)));
  if (chip < 4.5) errors.push(`contrast ${theme}:accent on accent-dim is ${chip}:1 — needs ≥ 4.5:1`);
}
const accentReport = brand.accents.map((a) => {
  const scheme = a.scheme;
  const value = colors[scheme]?.[a.token];
  const ratio = value ? contrast(parseColor(value), parseColor(colors[scheme].bg)) : 0;
  return { id: a.id, scheme, value, ratio, text: ratio >= 4.5, marks: ratio >= 3 };
});

// The splash source (motion/splash/) hard-codes its palette for the native first frame;
// it must agree with the tokens so a token change can't silently diverge from the splash.
if (colors.dark && fs.existsSync(path.join(ROOT, 'motion/splash/cofferdamMark.ts'))) {
  const mark = fs.readFileSync(path.join(ROOT, 'motion/splash/cofferdamMark.ts'), 'utf8');
  for (const m of mark.matchAll(/id: '([a-z-]+)'[\s\S]*?light: '(#[0-9A-Fa-f]{6})', dark: '(#[0-9A-Fa-f]{6})'/g)) {
    for (const [theme, v] of [['light', m[2]], ['dark', m[3]]]) {
      const want = colors[theme][`mark-${m[1]}`];
      if (!want || want.toLowerCase() !== v.toLowerCase()) errors.push(`motion/splash/cofferdamMark.ts ${m[1]} ${theme} is ${v}, tokens say mark-${m[1]} = ${want}`);
    }
  }
  const comp = fs.readFileSync(path.join(ROOT, 'motion/splash/CofferdamSplash.tsx'), 'utf8');
  for (const theme of ['light', 'dark']) {
    const m = new RegExp(`${theme}: \\{ base: '(#\\w+)', from: '(#\\w+)', to: '(#\\w+)'`).exec(comp);
    const want = [colors[theme]['splash-bg'], colors[theme]['splash-gradient-from'], colors[theme]['splash-gradient-to']];
    if (!m || m.slice(1).some((v, i) => v.toLowerCase() !== want[i].toLowerCase())) errors.push(`motion/splash/CofferdamSplash.tsx THEME.${theme} disagrees with splash-bg / splash-gradient-* tokens`);
  }
}

// Generated blocks in hand-written sources: components/bundle.js carries the splash timing (tokens/brand.json →
// motion.splash) and the wordmark outline (assets/logos/lockups/wordmark.json) between @generated markers.
// A normal build rewrites them in place; --check fails if they are stale.
{
  const f = 'components/bundle.js';
  const src = fs.readFileSync(path.join(ROOT, f), 'utf8');
  const { $comment, ...splashTiming } = brand.motion.splash;
  const blocks = {
    'splash-timing': `var SPLASH = ${JSON.stringify(splashTiming)};`,
    wordmark: `var WORDMARK = ${fs.readFileSync(path.join(ROOT, 'assets/logos/lockups/wordmark.json'), 'utf8').trim()};`,
  };
  let out = src;
  for (const [id, body] of Object.entries(blocks)) {
    const re = new RegExp(`(/\\* @generated:${id} \\*/\\n)[\\s\\S]*?(\\n\\s*/\\* @end:${id} \\*/)`);
    if (!re.test(out)) { errors.push(`${f}: missing @generated:${id} block`); continue; }
    out = out.replace(re, (m, a, b) => a + '  ' + body + b);
  }
  if (out !== src) {
    if (args.check) errors.push(`${f}: generated blocks are stale — run node scripts/build.mjs`);
    else { fs.writeFileSync(path.join(ROOT, f), out); warnings.push(`${f}: refreshed generated blocks`); }
  }
}

// Generated logo files (scripts/make-logos.py) bake the mark tones in; they must match the tokens.
{
  const pieces = ['a-stem', 'a-arm', 'b-stem', 'b-arm'];
  const expect = [
    ['assets/logos/v5/cofferdam-mark-v5-mono.svg', pieces.map((p) => colors.light[`mark-mono-${p}`])],
    ['assets/logos/v5/cofferdam-mark-v5-mono-on-dark.svg', pieces.map((p) => colors.dark[`mark-mono-${p}`])],
    ['assets/logos/lockups/cofferdam-lockup-horizontal-on-light.svg', [...pieces.map((p) => colors.light[`mark-mono-${p}`]), colors.light.fg]],
    ['assets/logos/lockups/cofferdam-lockup-stacked-on-light.svg', [...pieces.map((p) => colors.light[`mark-mono-${p}`]), colors.light.fg]],
    ['assets/logos/lockups/cofferdam-lockup-horizontal-on-dark.svg', pieces.map((p) => colors.dark[`mark-${p}`])],
    ['assets/logos/lockups/cofferdam-lockup-stacked-on-dark.svg', pieces.map((p) => colors.dark[`mark-${p}`])],
  ];
  for (const [f, want] of expect) {
    const p = path.join(ROOT, f);
    if (!fs.existsSync(p)) { errors.push(`${f} is missing — run python3 scripts/make-logos.py`); continue; }
    const svg = fs.readFileSync(p, 'utf8').toLowerCase();
    const miss = want.filter((v) => v && !svg.includes(`fill="${v.toLowerCase()}"`));
    if (miss.length) errors.push(`${f} is stale (missing ${miss.join(', ')}) — run python3 scripts/make-logos.py`);
  }
}

if (errors.length) {
  console.error('✗ build failed\n  ' + errors.join('\n  '));
  process.exit(1);
}

// ── 5. Emit ───────────────────────────────────────────────────────────────
let commit = 'uncommitted';
try {
  commit = execSync('git rev-parse --short HEAD', { cwd: ROOT, stdio: ['ignore', 'pipe', 'ignore'] }).toString().trim();
} catch {}
const stamp = { brandVersion: brand.version, tokensVersion: tokens.version, commit, season: season?.id ?? null, builtFor: mmdd };
const HEADER = (c) => `${c} AUTO-GENERATED by cofferdam-branding (${commit}${season ? `, season: ${season.id}` : ''}). Do not edit — change cofferdam-branding/tokens and re-run the sync.`;

const accentColor = (scheme, id) => {
  const a = effBrand.accents.find((x) => x.id === id);
  return a ? colors[scheme][a.token] : null;
};
const accents = effBrand.accents.map((a) => ({ id: a.id, name: a.name, scheme: a.scheme, color: colors[a.scheme][a.token].toUpperCase() }));

// 5a. resolved JSON
const resolved = {
  ...stamp,
  colors,
  type: tokens.type,
  spacing: Object.fromEntries(tokens.spacing.tokens.map((t) => [t.name, t.value])),
  radius: Object.fromEntries(tokens.radius.tokens.map((t) => [t.name, t.value])),
  shadow: Object.fromEntries(tokens.shadow.tokens.map((t) => [t.name, t.value])),
  opacity: Object.fromEntries(tokens.opacity.tokens.map((t) => [t.name, t.value])),
  accents,
  backgrounds: effBrand.backgrounds,
  defaults: effBrand.defaults,
  web: effBrand.web,
  motion: effBrand.motion,
  accentAlpha: effBrand.accentAlpha,
};
write('dist/brand.resolved.json', JSON.stringify(resolved, null, 2) + '\n');

// 5b. React Native module — keys match cofferdam-app/src/lib/theme.ts exactly.
const APP_KEYS = ['bg', 'surface', 'surface-2', 'card', 'card-border', 'border', 'border-control', 'divider', 'fg', 'fg-muted', 'fg-muted-2', 'fg-dim', 'accent', 'accent-dim', 'accent-border', 'identity', 'danger', 'danger-dim', 'danger-border', 'warning', 'success', 'info', 'base-blue', 'overlay', 'scrim', 'glass-scrim', 'chain-tile', 'chain-tile-testnet', 'chain-tile-edge', 'chain-mark'];
const appPalette = (theme) =>
  '{\n' + APP_KEYS.map((k) => `  ${camel(k).replace('surface2', 'surface2')}: '${colors[theme][k].startsWith('#') ? colors[theme][k].toUpperCase() : colors[theme][k]}',`).join('\n') + '\n}';
const rnShadow = (s) => {
  const m = /^(-?[\d.]+)(?:px)?\s+(-?[\d.]+)(?:px)?\s+([\d.]+)(?:px)?\s+(rgba?\([^)]*\)|#[0-9a-f]+)$/i.exec(s.trim());
  if (!m) return null;
  const c = parseColor(m[4]);
  return { shadowColor: '#000', shadowOffset: { width: +m[1], height: +m[2] }, shadowOpacity: c.a, shadowRadius: +m[3] };
};
const ELEVATION = { 'shadow-card-sm': 1, 'shadow-card': 2, 'shadow-card-lg': 4, 'shadow-fab': 8 };
const typeEntries = tokens.type.groups.flatMap((g) => g.styles.map((s) => ({ ...s, family: s.family ?? g.family })));
const familyName = (key) => tokens.type.families[key].match(/"([^"]+)"/)?.[1] ?? key;
const rnType = typeEntries
  .map((s) => {
    const o = { fontFamily: familyName(s.family), fontSize: px(s.fontSize), fontWeight: String(s.fontWeight) };
    if (s.letterSpacing) o.letterSpacing = String(s.letterSpacing).endsWith('em') ? +(parseFloat(s.letterSpacing) * px(s.fontSize)).toFixed(2) : px(s.letterSpacing);
    o.lineHeight = px(s.lineHeight);
    return `  ${camel(s.name)}: ${JSON.stringify(o).replace(/"(\w+)":/g, '$1: ')},`;
  })
  .join('\n');
const app = `${HEADER('//')}
/* eslint-disable */
import { Platform } from 'react-native';

export const BRAND = ${JSON.stringify(stamp, null, 2)} as const;

export const darkColors = ${appPalette('dark')};

export const lightColors: typeof darkColors = ${appPalette('light')};

/** Official Base palette + Self teal (theme-neutral swatches; Self teal has a light variant). */
export const palette = {
${tokens.color.tokens.filter((t) => t.name.startsWith('base-') || t.name === 'self-teal').map((t) => `  ${camel(t.name)}: { dark: '${colors.dark[t.name].toUpperCase()}', light: '${colors.light[t.name].toUpperCase()}' },`).join('\n')}
} as const;

export const spacing = {
${tokens.spacing.tokens.filter((t) => !t.name.startsWith('space-section')).map((t) => `  ${camel(t.name.replace('space-', ''))}: ${px(t.value)},`).join('\n')}
} as const;

export const radii = {
${tokens.radius.tokens.filter((t) => t.name !== 'radius-web').map((t) => `  ${camel(t.name.replace('radius-', ''))}: ${px(t.value)},`).join('\n')}
} as const;

/** Geist is registered by expo-font under these family names (see fonts/README.md). */
export const fonts = {
  sans: '${familyName('sans')}',
  mono: Platform.select({ ios: '${familyName('mono')}', default: '${familyName('mono')}' }) as string,
} as const;

export const type = {
${rnType}
  tabular: { fontVariant: ['tabular-nums'] as const },
  mono: { fontFamily: '${familyName('mono')}', letterSpacing: 0 },
} as const;

export const motion = {
${Object.entries(effBrand.motion.duration).map(([k, v]) => `  ${k}: ${v},`).join('\n')}
  spring: ${JSON.stringify(effBrand.motion.spring).replace(/"(\w+)":/g, '$1: ')},
} as const;

/** Launch splash + app icon (v5 mark). Timings match motion/splash/splashMath.ts. */
export const splash = {
  timing: ${JSON.stringify(Object.fromEntries(Object.entries(effBrand.motion.splash).filter(([k]) => !k.startsWith('$')))).replace(/"(\w+)":/g, '$1: ')},
${['dark', 'light'].map((th) => `  ${th}: { base: '${colors[th]['splash-bg'].toUpperCase()}', from: '${colors[th]['splash-gradient-from'].toUpperCase()}', to: '${colors[th]['splash-gradient-to'].toUpperCase()}', mark: { 'a-stem': '${colors[th]['mark-a-stem'].toUpperCase()}', 'a-arm': '${colors[th]['mark-a-arm'].toUpperCase()}', 'b-stem': '${colors[th]['mark-b-stem'].toUpperCase()}', 'b-arm': '${colors[th]['mark-b-arm'].toUpperCase()}' } },`).join('\n')}
} as const;

export const shadow = {
${tokens.shadow.tokens.map((t) => `  ${camel(t.name.replace('shadow-', ''))}: ${JSON.stringify({ ...rnShadow(t.value), elevation: ELEVATION[t.name] ?? 1 }).replace(/"(\w+)":/g, '$1: ')},`).join('\n')}
} as const;

export const ACCENT_ALPHA = ${JSON.stringify(effBrand.accentAlpha).replace(/"(\w+)":/g, '$1: ')} as const;

export const ACCENTS = ${JSON.stringify(accents, null, 2).replace(/"(\w+)":/g, '$1: ')} as const;

/** Wallpapers: \`image\` is the file name under assets/wallpapers/ — map it to require() in customization.ts. */
export const BACKGROUNDS = ${JSON.stringify(
  effBrand.backgrounds.map(({ webTexture, ...b }) => ({ ...b, image: b.image ? path.basename(b.image) : undefined })),
  null,
  2,
).replace(/"(\w+)":/g, '$1: ')} as const;

export const DEFAULT_CUSTOMIZATION = {
  scheme: '${effBrand.defaults.scheme}',
  accentId: '${effBrand.defaults.accent[effBrand.defaults.scheme]}',
  homeBackgroundId: '${effBrand.defaults.homeBackground}',
  lockBackgroundId: '${effBrand.defaults.lockBackground}',
} as const;

/** Default accent per scheme (the light default applies when the user switches to light). */
export const DEFAULT_ACCENT = ${JSON.stringify(effBrand.defaults.accent).replace(/"(\w+)":/g, '$1: ')} as const;
`;
write('dist/app/brand.generated.ts', app);

// 5c. Website CSS — :root is light, .dark is dark (next-themes class strategy).
const cssVal = (v) => v;
const cdVars = (theme) =>
  tokens.color.tokens
    .filter((t) => !t.name.startsWith('base-') && t.name !== 'self-teal')
    .map((t) => `  --cd-${t.name}: ${cssVal(colors[theme][t.name])};`)
    .join('\n');
const brandFor = (theme) => {
  const tokenName = effBrand.web.brandAccent[theme];
  const hex = colors[theme][tokenName];
  return `  --brand: var(--${tokenName});\n  --brand-dim: ${withAlpha(hex, effBrand.accentAlpha.dim)};\n  --brand-border: ${withAlpha(hex, effBrand.accentAlpha.border)};`;
};
const textureFor = (theme) => {
  const id = effBrand.web.texture[theme];
  const b = effBrand.backgrounds.find((x) => x.id === id);
  const op = tokens.opacity.tokens.find((t) => t.name === `opacity-texture-${theme}`)?.value;
  return `  --texture: url("/textures/${path.basename(b.webTexture)}");\n  --texture-opacity: ${op};`;
};
const pages = `${HEADER('/*')} */
/* Import from globals.css AFTER the tailwind imports:  @import "./brand.generated.css";
   Then point the shadcn variables at the --cd-* tokens (see cofferdam-branding/.claude/skills/cofferdam-brand-sync). */

:root {
  /* Official Base palette (locked) + Self teal. Raw swatches — components read --brand. */
${tokens.color.tokens.filter((t) => t.name.startsWith('base-')).map((t) => `  --${t.name}: ${colors.light[t.name]};`).join('\n')}
  --self-teal: ${colors.dark['self-teal']};

  /* Light theme */
${cdVars('light')}
${brandFor('light')}
${textureFor('light')}
  --cd-font-sans: ${tokens.type.families.sans};
  --cd-font-mono: ${tokens.type.families.mono};
${tokens.spacing.tokens.map((t) => `  --cd-${t.name}: ${t.value};`).join('\n')}
${tokens.radius.tokens.map((t) => `  --cd-${t.name}: ${t.value};`).join('\n')}
${tokens.shadow.tokens.map((t) => `  --cd-${t.name}: ${t.value};`).join('\n')}
${Object.entries(effBrand.motion.duration).map(([k, v]) => `  --cd-duration-${k}: ${v}ms;`).join('\n')}
}

.dark {
${cdVars('dark')}
${brandFor('dark')}
${textureFor('dark')}
}
`;
write('dist/pages/brand.generated.css', pages);

// 5d. Plain tokens.css (same layout as the Design System artifact compiles).
const themeBlock = (theme, sel) => {
  const lines = tokens.color.tokens.map((t) => {
    const raw = typeof t.value === 'string' ? t.value : t.value[theme] ?? t.value.dark;
    const alias = /^\{([^}]+)\}$/.exec(raw);
    return `  --${t.name}: ${alias ? `var(--${alias[1]})` : raw};`;
  });
  if (theme === 'dark') lines.push(...tokens.shadow.tokens.map((t) => `  --${t.name}: ${t.value};`));
  return `${sel} {\n${lines.join('\n')}\n}`;
};
const typeClasses = typeEntries
  .map(
    (s) =>
      `.${s.name} { font-family: var(--font-${s.family}); font-size: ${s.fontSize}; line-height: ${s.lineHeight}; font-weight: ${s.fontWeight};${s.letterSpacing ? ` letter-spacing: ${s.letterSpacing};` : ''} }`,
  )
  .join('\n');
const tokensCss = `/* Cofferdam — generated from tokens.json */
${themeBlock('dark', ':root, [data-theme="dark"]')}
${themeBlock('light', '[data-theme="light"]')}
:root {
${[...tokens.spacing.tokens, ...tokens.radius.tokens, ...tokens.opacity.tokens].map((t) => `  --${t.name}: ${t.value};`).join('\n')}
  --font-sans: ${tokens.type.families.sans};
  --font-mono: ${tokens.type.families.mono};
}
${typeClasses}
${tokens.type.fonts.map((f) => `@font-face { font-family: "${f.family}"; src: url("${f.file}") format("woff2"); font-weight: ${f.weight}; font-style: ${f.style ?? 'normal'}; font-display: swap; }`).join('\n')}
`;
write('dist/tokens.css', tokensCss);

// 5e. Design System artifact files (canonical, no season: the artifact is the brand book).
const DS = 'dist/design-system/project';
const dsTokens = structuredClone(baseTokens);
let repo = 'cofferdamxyz/cofferdam-branding';
dsTokens.meta = {
  source: 'github',
  repo,
  ref: `main@${commit}`,
  paths: { tokens: ['tokens/tokens.json', 'tokens/brand.json'], fonts: ['fonts/'], assets: ['assets/'], docs: ['brand/'] },
  synced: today.toISOString().slice(0, 10),
};
write(`${DS}/tokens.json`, JSON.stringify(dsTokens, null, 2) + '\n');
copy('brand/README.md', `${DS}/README.md`);
for (const f of fs.readdirSync(path.join(ROOT, 'brand/sections')).filter((f) => f.endsWith('.md'))) copy(`brand/sections/${f}`, `${DS}/${f}`);
for (const f of tokens.type.fonts) copy(f.file, `${DS}/${f.file}`);
const walk = (dir) =>
  fs.readdirSync(path.join(ROOT, dir), { withFileTypes: true }).flatMap((d) => (d.isDirectory() ? walk(`${dir}/${d.name}`) : [`${dir}/${d.name}`]));
for (const f of fs.readdirSync(path.join(ROOT, 'brand/asset-groups')).filter((f) => f.endsWith('.md'))) copy(`brand/asset-groups/${f}`, `${DS}/assets/${f.replace(/\.md$/, '')}/README.md`);
// {{mark-polygons}} in a static preview (the Cover) → the four official v5 pieces, classed m-a-stem … m-b-arm.
const markSvg = fs.readFileSync(path.join(ROOT, 'assets/logos/v5/cofferdam-mark-v5-on-dark.svg'), 'utf8');
const MARK_POLYGONS = ['a-stem', 'a-arm', 'b-stem', 'b-arm']
  .map((id) => `<polygon class="m-${id}" points="${new RegExp(`<polygon id="${id}" points="([^"]+)"`).exec(markSvg)[1]}"/>`)
  .join('');
const assetLock = fs.existsSync(path.join(ROOT, 'design-system.assets.json')) ? readJSON('design-system.assets.json').files : {};
for (const f of walk('components')) {
  if (!f.endsWith('.html')) {
    copy(f, `${DS}/${f}`);
    continue;
  }
  const html = fs.readFileSync(path.join(ROOT, f), 'utf8').replace(/\{\{mark-polygons\}\}/g, () => MARK_POLYGONS).replace(/\{\{asset:([^}]+)\}\}/g, (m, p) => {
    if (!assetLock[p]) {
      warnings.push(`${f}: ${p} has no asset-store record in design-system.assets.json`);
      return `../../${p}`;
    }
    return `/_blob/${assetLock[p].blob}`;
  });
  write(`${DS}/${f}`, html);
}

// ── 6. Report ─────────────────────────────────────────────────────────────
console.log(`✓ cofferdam-branding ${commit} · ${mmdd} · season: ${season?.id ?? 'none'}${args.check ? ' · check only' : ''}`);
for (const w of warnings) console.log(`  ! ${w}`);
if (args.verbose) {
  console.table(report);
  console.table(accentReport);
} else {
  const weak = accentReport.filter((a) => !a.marks).map((a) => `${a.id} ${a.ratio}:1`);
  if (weak.length) console.log(`  ! accent options below 3:1 on their scheme's bg (marks only, never text): ${weak.join(', ')}`);
}
