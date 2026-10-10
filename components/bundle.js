/* @ds-bundle: {"format":4,"namespace":"Cofferdam","components":[{"name":"Button"},{"name":"StatusChip"},{"name":"Avatar"},{"name":"ChainLogo"},{"name":"BottomChip"},{"name":"GlassSurface"},{"name":"CofferdamMark"}]} */
/* Web reference renditions of cofferdam-app's React Native UI kit (src/components/ui/*) and
   cofferdam-pages' CofferdamMark. Hand-written from those sources: same variants, sizes and
   tokens, rendered with DOM + bundle.css. React 18 globals (window.React). */
(function () {
  var React = window.React;
  var h = React.createElement;
  function cx() {
    return Array.prototype.filter.call(arguments, Boolean).join(' ');
  }

  /* Button — src/components/ui/Button.tsx. primary = solid fg-on-bg, secondary = outline,
     ghost = text only. lg 56px / md 44px, pill radius, label type style. */
  function Button(props) {
    var variant = props.variant || 'primary';
    var size = props.size || 'lg';
    var disabled = props.disabled || props.loading;
    return h(
      'button',
      {
        type: 'button',
        className: cx('cd-btn', 'cd-btn--' + variant, 'cd-btn--' + size, props.fullWidth === false ? null : 'cd-btn--full'),
        disabled: disabled,
        'aria-busy': props.loading ? 'true' : undefined,
        'aria-label': props.accessibilityLabel || undefined,
        onClick: disabled ? undefined : props.onPress,
      },
      props.loading
        ? h('span', { className: 'cd-spinner', 'aria-hidden': 'true' })
        : [
            props.leadingIcon ? h('span', { key: 'l', className: 'cd-btn__icon' }, props.leadingIcon) : null,
            h('span', { key: 't' }, props.label),
            props.trailingIcon ? h('span', { key: 'r', className: 'cd-btn__icon' }, props.trailingIcon) : null,
          ],
    );
  }

  /* StatusChip — src/components/ui/StatusChip.tsx. Reserving / Deploying pulse in neutral,
     Ready takes the accent (text + dim fill + border), Failed takes danger. */
  var STATUS_LABEL = { reserving: 'Reserving address', deploying: 'Deploying', ready: 'Ready', failed: 'Failed' };
  function StatusChip(props) {
    var status = props.status || 'reserving';
    return h(
      'span',
      { className: cx('cd-chip', 'cd-chip--' + status), role: 'status' },
      h('span', { className: 'cd-chip__dot', 'aria-hidden': 'true' }),
      h('span', { className: 'cd-chip__label' }, props.label || STATUS_LABEL[status]),
    );
  }

  /* Avatar — src/components/ui/Avatar.tsx. Circle, monochrome initials fallback, accent ✓ badge
     when verified, optional chain badge. sm 28 · md 40 · lg 64 · xl 96. */
  var AVATAR = { sm: 28, md: 40, lg: 64, xl: 96 };
  function initialsOf(name) {
    var t = name ? String(name).trim() : '';
    if (!t) return '·';
    return t.split(/\s+/).slice(0, 2).map(function (p) { return (p[0] || '').toUpperCase(); }).join('') || t[0].toUpperCase();
  }
  function Avatar(props) {
    var d = AVATAR[props.size || 'md'];
    var ring = Math.max(1.5, d * 0.04);
    return h(
      'span',
      { className: 'cd-avatar', style: { width: d, height: d } },
      props.source
        ? h('img', { className: 'cd-avatar__img', src: props.source, alt: props.name || '' })
        : h('span', { className: 'cd-avatar__initials', style: { fontSize: d * 0.4, lineHeight: d + 'px' } }, props.initials || initialsOf(props.name)),
      props.verified
        ? h(
            'span',
            { className: 'cd-avatar__badge', 'aria-label': 'Verified', style: { width: d * 0.32, height: d * 0.32, right: -d * 0.02, bottom: -d * 0.02, borderWidth: ring } },
            h('svg', { viewBox: '0 0 24 24', width: Math.max(8, d * 0.18), height: Math.max(8, d * 0.18), fill: 'none', stroke: 'currentColor', strokeWidth: 3, strokeLinecap: 'round', strokeLinejoin: 'round' }, h('path', { d: 'M20 6 9 17l-5-5' })),
          )
        : null,
      props.chainId != null
        ? h(
            'span',
            { className: 'cd-avatar__chain', style: { width: d * 0.36, height: d * 0.36, left: -d * 0.02, bottom: -d * 0.02, borderWidth: ring } },
            h(ChainLogo, { chainId: props.chainId, size: Math.max(10, d * 0.28) }),
          )
        : null,
    );
  }

  /* ChainLogo — src/components/ui/ChainLogo.tsx. The official Base Square path (1280 viewBox),
     white on dark / #0000FF on light; Sepolia gets a muted bordered tile and a testnet dot. */
  var SQUARE_D =
    'M0,101.12c0-34.64,0-51.95,6.53-65.28,6.25-12.76,16.56-23.07,29.32-29.32C49.17,0,66.48,0,101.12,0h1077.76c34.63,0,51.96,0,65.28,6.53,12.75,6.25,23.06,16.56,29.32,29.32,6.52,13.32,6.52,30.64,6.52,65.28v1077.76c0,34.63,0,51.96-6.52,65.28-6.26,12.75-16.57,23.06-29.32,29.32-13.32,6.52-30.65,6.52-65.28,6.52H101.12c-34.64,0-51.95,0-65.28-6.52-12.76-6.26-23.07-16.57-29.32-29.32-6.53-13.32-6.53-30.65-6.53-65.28V101.12Z';
  function ChainLogo(props) {
    var size = props.size || 24;
    var mainnet = props.chainId === 8453;
    return h(
      'svg',
      {
        className: cx('cd-chain', mainnet ? 'cd-chain--mainnet' : 'cd-chain--sepolia'),
        viewBox: '0 0 48 48',
        width: size,
        height: size,
        role: 'img',
        'aria-label': mainnet ? 'Base Mainnet' : 'Base Sepolia',
      },
      h('rect', { className: 'cd-chain__tile', width: 48, height: 48, rx: 14 }),
      mainnet ? null : h('rect', { className: 'cd-chain__edge', x: 0.75, y: 0.75, width: 46.5, height: 46.5, rx: 13.25, fill: 'none', strokeWidth: 1.5 }),
      h('g', { transform: 'translate(11 11) scale(0.0203)' }, h('path', { className: 'cd-chain__square', d: SQUARE_D })),
      mainnet ? null : h('circle', { className: 'cd-chain__dot', cx: 39, cy: 9, r: 5, strokeWidth: 2.5 }),
    );
  }

  /* BottomChip — src/components/ui/BottomChip.tsx. Low-emphasis footer chip (language, theme). */
  function BottomChip(props) {
    return h(
      'button',
      { type: 'button', className: 'cd-bottomchip', onClick: props.onPress, 'aria-label': props.accessibilityLabel || undefined },
      props.icon ? h('span', { className: 'cd-btn__icon' }, props.icon) : null,
      h('span', null, props.label),
    );
  }

  /* GlassSurface — src/components/ui/GlassSurface.tsx. The web/Android fallback path:
     backdrop blur + translucent scrim (light rgba(255,255,255,.65), dark rgba(20,21,24,.55)). */
  function GlassSurface(props) {
    return h(
      'div',
      { className: 'cd-glass', style: Object.assign({ borderRadius: props.radius != null ? props.radius : 0 }, props.style || {}) },
      props.children,
    );
  }

  /* CofferdamMark — cofferdam-pages/src/components/landing/CofferdamMark.tsx (interim mark).
     Outer rounded-square frame (the coffer) + offset solid inset (the seal), currentColor. */
  function CofferdamMark(props) {
    var size = props.size || 32;
    return h(
      'svg',
      { viewBox: '0 0 32 32', width: size, height: size, fill: 'none', role: 'img', 'aria-label': 'Cofferdam', className: props.className, style: props.color ? { color: props.color } : undefined },
      h('rect', { x: 2.5, y: 2.5, width: 27, height: 27, rx: 8, stroke: 'currentColor', strokeWidth: 2.5 }),
      h('rect', { x: 11, y: 11, width: 14, height: 14, rx: 3.5, fill: 'currentColor' }),
    );
  }

  window.Cofferdam = {
    Button: Button,
    StatusChip: StatusChip,
    Avatar: Avatar,
    ChainLogo: ChainLogo,
    BottomChip: BottomChip,
    GlassSurface: GlassSurface,
    CofferdamMark: CofferdamMark,
  };
})();
