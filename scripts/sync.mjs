#!/usr/bin/env node
/**
 * Copy the generated brand files into the consumer repositories.
 *
 *   node scripts/sync.mjs                                  # dry run against ../cofferdam-app and ../cofferdam-pages
 *   node scripts/sync.mjs --write                          # actually copy
 *   node scripts/sync.mjs --app=/path/app --pages=/path/pages --write
 *   node scripts/sync.mjs --only=pages --write
 *
 * Run `node scripts/build.mjs` first. Only the files in TARGETS are ever written,
 * and only when their bytes differ; nothing is deleted. Exit code 0 = in sync after
 * the run (or nothing to do), 2 = dry run found differences.
 */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const args = Object.fromEntries(process.argv.slice(2).map((a) => { const [k, v] = a.replace(/^--/, '').split('='); return [k, v ?? true]; }));
const repos = {
  app: path.resolve(ROOT, args.app ?? '../cofferdam-app'),
  pages: path.resolve(ROOT, args.pages ?? '../cofferdam-pages'),
};

const wallpapers = fs.readdirSync(path.join(ROOT, 'assets/wallpapers')).filter((f) => f.endsWith('.png'));
const textures = fs.readdirSync(path.join(ROOT, 'assets/textures')).filter((f) => f.endsWith('.webp'));
const LOGOS = ['cofferdam-mark-v5.svg', 'cofferdam-mark-v5-on-dark.svg', 'cofferdam-mark-v5-white.svg', 'cofferdam-mark-v5-black.svg', 'cofferdam-mark-v5-mono.svg', 'cofferdam-mark-v5-mono-on-dark.svg'];
const LOCKUPS = ['horizontal', 'stacked'].flatMap((l) => ['on-dark', 'on-light', 'white', 'black'].map((v) => `cofferdam-lockup-${l}-${v}.svg`));
const fonts = fs.readdirSync(path.join(ROOT, 'fonts')).filter((f) => /\.(woff2?|ttf|otf)$/.test(f));

/** [repo, from (in this repo), to (in the consumer)] */
const TARGETS = [
  ['app', 'dist/app/brand.generated.ts', 'src/lib/brand.generated.ts'],
  ['app', 'dist/brand.resolved.json', 'src/lib/brand.resolved.json'],
  ...wallpapers.map((f) => ['app', `assets/wallpapers/${f}`, `assets/wallpapers/${f}`]),
  ...fonts.map((f) => ['app', `fonts/${f}`, `assets/fonts/${f}`]),
  ['pages', 'dist/pages/brand.generated.css', 'src/app/brand.generated.css'],
  ...textures.map((f) => ['pages', `assets/textures/${f}`, `public/textures/${f}`]),
  ...['CofferdamSplash.tsx', 'splashMath.ts', 'cofferdamMark.ts'].map((f) => ['app', `motion/splash/${f}`, `src/components/brand/splash/${f}`]),
  ...LOGOS.map((f) => ['app', `assets/logos/v5/${f}`, `assets/brand/${f}`]),
  ...LOGOS.map((f) => ['pages', `assets/logos/v5/${f}`, `public/brand/${f}`]),
  ...LOCKUPS.map((f) => ['app', `assets/logos/lockups/${f}`, `assets/brand/${f}`]),
  ...LOCKUPS.map((f) => ['pages', `assets/logos/lockups/${f}`, `public/brand/${f}`]),
];

const hash = (p) => (fs.existsSync(p) ? crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex') : null);
let changed = 0;
for (const [repo, from, to] of TARGETS) {
  if (args.only && args.only !== repo) continue;
  if (!fs.existsSync(repos[repo])) {
    console.log(`- skip ${repo}: ${repos[repo]} not found`);
    continue;
  }
  const src = path.join(ROOT, from);
  if (!fs.existsSync(src)) {
    console.error(`✗ ${from} missing — run node scripts/build.mjs first`);
    process.exit(1);
  }
  const dst = path.join(repos[repo], to);
  const before = hash(dst);
  if (before === hash(src)) continue;
  changed++;
  console.log(`${args.write ? '✓ wrote' : '~ would write'} ${repo}/${to}${before ? '' : ' (new)'}`);
  if (args.write) {
    fs.mkdirSync(path.dirname(dst), { recursive: true });
    fs.copyFileSync(src, dst);
  }
}
console.log(changed ? `${changed} file(s) ${args.write ? 'updated' : 'differ'}` : 'consumers already in sync');
process.exit(changed && !args.write ? 2 : 0);
