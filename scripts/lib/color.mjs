// Colour helpers: parse hex / rgba(), alias resolution, WCAG contrast. No dependencies.

export function parseColor(v) {
  if (typeof v !== 'string') return null;
  const s = v.trim().toLowerCase();
  let m = /^#([0-9a-f]{3,4})$/.exec(s);
  if (m) {
    const [r, g, b, a = 'f'] = m[1].split('');
    return { r: parseInt(r + r, 16), g: parseInt(g + g, 16), b: parseInt(b + b, 16), a: parseInt(a + a, 16) / 255 };
  }
  m = /^#([0-9a-f]{6})([0-9a-f]{2})?$/.exec(s);
  if (m) {
    const n = parseInt(m[1], 16);
    return { r: (n >> 16) & 255, g: (n >> 8) & 255, b: n & 255, a: m[2] ? parseInt(m[2], 16) / 255 : 1 };
  }
  m = /^rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*(?:,\s*([\d.]+)\s*)?\)$/.exec(s);
  if (m) return { r: +m[1], g: +m[2], b: +m[3], a: m[4] === undefined ? 1 : +m[4] };
  return null;
}

export function toHex({ r, g, b }) {
  return '#' + [r, g, b].map((c) => Math.round(c).toString(16).padStart(2, '0')).join('');
}

export function withAlpha(hex, alpha) {
  const c = parseColor(hex);
  if (!c) return hex;
  return `rgba(${c.r}, ${c.g}, ${c.b}, ${alpha})`;
}

/** Composite a (possibly translucent) colour over an opaque ground. */
export function over(fg, ground) {
  const a = fg.a ?? 1;
  return { r: fg.r * a + ground.r * (1 - a), g: fg.g * a + ground.g * (1 - a), b: fg.b * a + ground.b * (1 - a), a: 1 };
}

function lum({ r, g, b }) {
  const f = (c) => {
    c /= 255;
    return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
  };
  return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
}

export function contrast(a, b) {
  const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p);
  return Math.round(((x + 0.05) / (y + 0.05)) * 100) / 100;
}

/** Resolve every colour token to a literal per theme ({alias} → value; missing theme → first theme). */
export function resolveColors(colorFamily) {
  const themes = colorFamily.themes.map((t) => t.id);
  const byName = new Map(colorFamily.tokens.map((t) => [t.name, t]));
  const out = {};
  for (const theme of themes) {
    out[theme] = {};
    const resolve = (name, depth = 0) => {
      if (depth > 16) throw new Error(`alias chain too deep at ${name}`);
      const tok = byName.get(name);
      if (!tok) throw new Error(`unknown colour token "${name}"`);
      let v = typeof tok.value === 'string' ? tok.value : tok.value[theme] ?? tok.value[themes[0]];
      const alias = /^\{([^}]+)\}$/.exec(v ?? '');
      if (alias) return resolve(alias[1], depth + 1);
      if (!parseColor(v)) throw new Error(`colour token "${name}" (${theme}) has an unreadable value: ${v}`);
      return v;
    };
    for (const name of byName.keys()) out[theme][name] = resolve(name);
  }
  return out;
}
