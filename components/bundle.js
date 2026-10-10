/* @ds-bundle: {"format":4,"namespace":"Cofferdam","components":[{"name":"Button"},{"name":"StatusChip"},{"name":"Avatar"},{"name":"ChainLogo"},{"name":"BottomChip"},{"name":"GlassSurface"},{"name":"CofferdamMark"},{"name":"Splash"}]} */
/* Web reference renditions of cofferdam-app's React Native UI kit (src/components/ui/*) and
   cofferdam-pages' CofferdamMark. Hand-written from those sources: same variants, sizes and
   tokens, rendered with DOM + bundle.css. The mark and Splash use the v5 geometry from motion/splash/cofferdamMark.ts. React 18 globals (window.React). */
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

  /* CofferdamMark — the v5 mark (interlocking brackets), geometry from cofferdam-branding/motion/splash/cofferdamMark.ts
     (1024 viewBox, four pieces). tone="tones" fills each piece from the mark-* tokens (dark palette in the dark
     theme, the Cerulean-ground palette in light); tone="ink" draws all four in one colour (currentColor). */
  var MARK = [{"id":"a-stem","pts":[[205.6,344.0],[210.0,322.2],[215.3,302.1],[221.4,283.6],[228.5,266.7],[236.5,251.4],[245.6,237.7],[255.8,225.4],[267.1,214.6],[269.1,213.1],[385.0,353.8],[383.0,355.3],[379.6,358.5],[376.7,362.1],[374.0,366.1],[371.6,370.6],[369.6,375.6],[367.8,381.0],[366.2,386.9],[364.9,393.3],[335.7,559.0],[333.6,569.5],[331.1,579.2],[328.1,588.0],[324.7,596.1],[320.9,603.5],[316.5,610.1],[311.6,616.0],[306.2,621.1],[300.2,625.6],[293.7,629.5],[286.5,632.7],[278.7,635.2],[270.3,637.2],[261.2,638.6],[251.4,639.4],[240.8,639.7],[234.1,639.7],[223.7,639.4],[214.2,638.6],[205.6,637.2],[197.8,635.2],[190.9,632.7],[184.9,629.5],[179.7,625.6],[175.3,621.1],[171.7,616.0],[168.9,610.1],[166.9,603.5],[165.6,596.1],[165.1,588.0],[165.2,579.2],[166.1,569.5],[167.7,559.0]],"axis":1,"keepGreater":true,"from":639.7,"to":211.1},{"id":"a-arm","pts":[[267.1,214.6],[267.1,214.6],[279.5,205.3],[293.2,197.3],[308.1,190.6],[324.3,185.2],[341.9,181.1],[360.9,178.3],[381.3,176.6],[403.2,176.0],[826.6,176.0],[837.0,176.3],[846.5,177.1],[855.2,178.5],[862.9,180.4],[869.8,183.0],[875.8,186.2],[881.0,190.0],[885.4,194.5],[889.0,199.7],[891.8,205.6],[893.9,212.2],[895.1,219.5],[895.7,227.6],[895.5,236.5],[894.6,246.2],[893.0,256.6],[891.8,263.4],[889.7,273.8],[887.2,283.5],[884.3,292.4],[880.9,300.5],[877.0,307.8],[872.6,314.4],[867.8,320.3],[862.3,325.5],[856.4,330.0],[849.8,333.8],[842.6,337.0],[834.9,339.6],[826.4,341.5],[817.3,342.9],[807.5,343.7],[797.0,344.0],[422.9,344.0],[416.5,344.2],[410.5,344.7],[404.9,345.5],[399.8,346.7],[395.0,348.3],[390.6,350.2],[386.6,352.6],[383.0,355.3],[383.0,355.3]],"axis":0,"keepGreater":false,"from":267.1,"to":897.7},{"id":"b-stem","pts":[[818.4,680.0],[814.0,701.8],[808.7,721.9],[802.6,740.4],[795.5,757.3],[787.5,772.6],[778.4,786.3],[768.2,798.6],[756.9,809.4],[754.9,810.9],[639.0,670.2],[641.0,668.7],[644.4,665.5],[647.3,661.9],[650.0,657.9],[652.4,653.4],[654.4,648.4],[656.2,643.0],[657.8,637.1],[659.1,630.7],[688.3,465.0],[690.4,454.5],[692.9,444.8],[695.9,436.0],[699.3,427.9],[703.1,420.5],[707.5,413.9],[712.4,408.0],[717.8,402.9],[723.8,398.4],[730.3,394.5],[737.5,391.3],[745.3,388.8],[753.7,386.8],[762.8,385.4],[772.6,384.6],[783.2,384.3],[789.9,384.3],[800.3,384.6],[809.8,385.4],[818.4,386.8],[826.2,388.8],[833.1,391.3],[839.1,394.5],[844.3,398.4],[848.7,402.9],[852.3,408.0],[855.1,413.9],[857.1,420.5],[858.4,427.9],[858.9,436.0],[858.8,444.8],[857.9,454.5],[856.3,465.0]],"axis":1,"keepGreater":false,"from":384.3,"to":812.9},{"id":"b-arm","pts":[[756.9,809.4],[756.9,809.4],[744.5,818.7],[730.8,826.7],[715.9,833.4],[699.7,838.8],[682.1,842.9],[663.1,845.7],[642.7,847.4],[620.8,848.0],[197.4,848.0],[187.0,847.7],[177.5,846.9],[168.8,845.5],[161.1,843.6],[154.2,841.0],[148.2,837.8],[143.0,834.0],[138.6,829.5],[135.0,824.3],[132.2,818.4],[130.1,811.8],[128.9,804.5],[128.3,796.4],[128.5,787.5],[129.4,777.8],[131.0,767.4],[132.2,760.6],[134.3,750.2],[136.8,740.5],[139.7,731.6],[143.1,723.5],[147.0,716.2],[151.4,709.6],[156.2,703.7],[161.7,698.5],[167.6,694.0],[174.2,690.2],[181.4,687.0],[189.1,684.4],[197.6,682.5],[206.7,681.1],[216.5,680.3],[227.0,680.0],[601.1,680.0],[607.5,679.8],[613.5,679.3],[619.1,678.5],[624.2,677.3],[629.0,675.7],[633.4,673.8],[637.4,671.4],[641.0,668.7],[641.0,668.7]],"axis":0,"keepGreater":true,"from":756.9,"to":126.3}];
  function pts(p) { return p.map(function (q) { return q[0] + ',' + q[1]; }).join(' '); }
  function CofferdamMark(props) {
    var size = props.size || 32;
    var ink = props.tone === 'ink';
    return h(
      'svg',
      { viewBox: '0 0 1024 1024', width: size, height: size, role: 'img', 'aria-label': 'Cofferdam', className: props.className, style: props.color ? { color: props.color } : undefined },
      MARK.map(function (m) {
        return h('polygon', { key: m.id, points: pts(m.pts), style: { fill: ink ? 'currentColor' : 'var(--mark-' + m.id + ')' } });
      }),
    );
  }

  /* Splash — web replay of cofferdam-app's launch splash (motion/splash/CofferdamSplash.tsx): pieces wipe in one at a
     time (A stem → A arm → B stem → B arm, 340ms each, 40ms apart, ease-out cubic), settle bump, hold, fade + scale out.
     Same timeline and wipe clipping as splashMath.ts; requestAnimationFrame instead of Reanimated. */
  var T = { start: 120, dur: 340, gap: 40, bumpDur: 350, hold: 120, exitDur: 300 };
  var BUMP_AT = T.start + 4 * T.dur + 3 * T.gap;
  var HOLD_END = BUMP_AT + T.bumpDur + T.hold;
  function clamp01(x) { return x < 0 ? 0 : x > 1 ? 1 : x; }
  function easeOutCubic(x) { var k = 1 - x; return 1 - k * k * k; }
  function easeInOut(x) { return 3 * x * x - 2 * x * x * x; }
  function wipe(p, axis, edge, keepGreater) {
    var s = '', n = p.length, prev = p[n - 1], prevIn = keepGreater ? prev[axis] >= edge : prev[axis] <= edge;
    for (var i = 0; i < n; i++) {
      var cur = p[i], curIn = keepGreater ? cur[axis] >= edge : cur[axis] <= edge;
      if (curIn !== prevIn) {
        var t = (edge - prev[axis]) / (cur[axis] - prev[axis]);
        s += prev[0] + t * (cur[0] - prev[0]) + ',' + (prev[1] + t * (cur[1] - prev[1])) + ' ';
      }
      if (curIn) s += cur[0] + ',' + cur[1] + ' ';
      prev = cur; prevIn = curIn;
    }
    return s === '' ? '0,0 0,0 0,0' : s;
  }
  function Splash(props) {
    var width = props.width || 220;
    var height = props.height || Math.round(width * 2.16);
    var markScale = props.markScale || 0.74;
    var size = width * markScale;
    var st = React.useState(0), tMs = st[0], setT = st[1];
    var run = React.useState(0), runId = run[0], setRun = run[1];
    React.useEffect(function () {
      var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      if (reduced) { setT(HOLD_END); return; }
      var raf, t0 = null, total = HOLD_END + 500 + T.exitDur;
      function tick(now) {
        if (t0 === null) t0 = now;
        var t = now - t0;
        setT(Math.min(t, total));
        if (t < total) raf = requestAnimationFrame(tick);
        else if (props.loop !== false) setTimeout(function () { setRun(function (r) { return r + 1; }); }, 700);
      }
      raf = requestAnimationFrame(tick);
      return function () { cancelAnimationFrame(raf); };
    }, [runId]);
    var exitStart = HOLD_END + 500;
    var exit = easeInOut(clamp01((tMs - exitStart) / T.exitDur));
    var bump = tMs < BUMP_AT ? 0 : 0.035 * Math.sin(Math.PI * easeInOut(clamp01((tMs - BUMP_AT) / T.bumpDur)));
    var gid = 'cd-splash-g-' + (props.id || 'a');
    return h(
      'div',
      { className: 'cd-splash', style: { width: width, height: height }, role: 'img', 'aria-label': 'Cofferdam launch splash' },
      h('div', { className: 'cd-splash__app', style: { opacity: exit } }, props.children),
      h(
        'svg',
        { className: 'cd-splash__ground', width: width, height: height, style: { opacity: 1 - exit } },
        h('defs', null, h('linearGradient', { id: gid, x1: 0, y1: 0, x2: 1, y2: 1 },
          h('stop', { offset: 0, style: { stopColor: 'var(--splash-gradient-from)' } }),
          h('stop', { offset: 1, style: { stopColor: 'var(--splash-gradient-to)' } }))),
        h('rect', { width: width, height: height, style: { fill: 'var(--splash-bg)' } }),
        h('rect', { width: width, height: height, fill: 'url(#' + gid + ')', style: { opacity: clamp01(tMs / 700) } }),
        h(
          'svg',
          { x: (width - size) / 2, y: (height - size) / 2, width: size, height: size, viewBox: '0 0 1024 1024', overflow: 'visible' },
          h(
            'g',
            { transform: 'translate(512 512) scale(' + (1 + bump + 0.08 * exit) + ') translate(-512 -512)' },
            MARK.map(function (m, i) {
              var start = T.start + i * (T.dur + T.gap);
              var p = easeOutCubic(clamp01((tMs - start) / T.dur));
              var edge = m.from + (m.to - m.from) * p;
              return h('polygon', { key: m.id, points: wipe(m.pts, m.axis, edge, m.keepGreater), style: { fill: 'var(--mark-' + m.id + ')' } });
            }),
          ),
        ),
      ),
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
    Splash: Splash,
  };
})();
