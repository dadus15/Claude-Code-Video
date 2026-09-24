/*
 * Graphite & Bronze — cinematic photo slider.
 *
 * One playback clock drives everything: each visible photo layer records the
 * clock time it was revealed ("born"), and its crossfade opacity, Ken Burns
 * transform and the progress bar are all pure functions of that clock. Pausing
 * simply stops the clock, so resuming continues from the same frame.
 *
 * Crossfades stack a new layer on top of the old one and fade it from 0 to 1,
 * so the result is always a linear blend of two moving photos. Layers that end
 * up fully covered are recycled, which keeps rapid navigation seamless.
 */
(() => {
  'use strict';

  const SLIDE_MS = 5000;              // time per slide, including the fade in
  const FADE_MS = 900;                // crossfade into the next slide
  const LIFE_MS = SLIDE_MS + FADE_MS; // a photo keeps moving while it fades out
  const BLEND_MS = 700;               // easing motion on/off (Full photo, reduced motion)
  const IDLE_MS = 2600;               // desktop controls fade after this much stillness
  const LAYER_COUNT = 4;
  // Bottom edge of the GT Turismo watermark as a fraction of photo height. The
  // motion clamp keeps this band inside the frame.
  const WATERMARK_BOTTOM = 0.975;
  const PHOTO_DIRS = ['photos/', './'];
  const NAME_RE = /(?:^|[^0-9])9024([1-8])\.jpe?g$/i;

  // Motion keyframes: s = uniform scale, x/y = translation as a fraction of the
  // stage (positive x moves the photo right, positive y moves it down). Values
  // are clamped at runtime so the photo always covers the frame.
  const SLIDES = [
    {
      id: '90241',
      title: 'Front three-quarter',
      sub: 'Graphite bodywork · bronze forged wheel',
      alt: 'Front three-quarter view of a graphite-grey Ferrari parked in front of a white house, with a bronze forged wheel, yellow brake caliper and slim LED headlight.',
      motion: { from: { s: 1.0, x: 0, y: 0 }, to: { s: 1.045, x: 0.006, y: -0.008 } },
    },
    {
      id: '90248',
      title: 'Low front profile',
      sub: 'From the nose to the mirror',
      alt: 'Low front side profile of the graphite Ferrari, showing a bronze forged wheel and yellow brake caliper.',
      motion: { from: { s: 1.035, x: -0.01, y: -0.002 }, to: { s: 1.035, x: 0.01, y: -0.002 } },
    },
    {
      id: '90243',
      title: 'Fender & shield',
      sub: 'Shield badge above the front arch',
      alt: 'High-angle view over the graphite front fender, with the yellow prancing-horse shield badge, a bronze forged wheel and yellow brake caliper on paving stones.',
      motion: { from: { s: 1.03, x: 0.005, y: -0.004 }, to: { s: 1.045, x: -0.008, y: 0.003 } },
    },
    {
      id: '90242',
      title: 'Centre cap',
      sub: 'Bronze spokes · yellow caliper · carbon-ceramic disc',
      alt: 'Close-up of a bronze forged wheel centre with a yellow prancing-horse centre cap, a yellow brake caliper and a carbon-ceramic disc behind the spokes.',
      motion: { from: { s: 1.04, x: 0.004, y: -0.002 }, to: { s: 1.04, x: -0.006, y: -0.002 } },
    },
    {
      id: '90244',
      title: 'Forged rim engraving',
      sub: 'Turismo Forged, cut into the lip',
      alt: 'Macro of the bronze rim lip engraved with the words Turismo Forged, beside the tyre sidewall and a yellow brake caliper.',
      motion: { from: { s: 1.035, x: 0.006, y: 0.004 }, to: { s: 1.045, x: 0.002, y: -0.008 } },
    },
    {
      id: '90247',
      title: 'Rear wheel',
      sub: 'The complete forged face',
      alt: 'The complete rear bronze forged wheel of the graphite Ferrari, with its yellow brake caliper.',
      motion: { from: { s: 1.0, x: 0, y: 0 }, to: { s: 1.045, x: 0, y: -0.002 } },
    },
    {
      id: '90246',
      title: 'Rear profile',
      sub: 'Along the rear haunch',
      alt: 'Rear side profile of the graphite Ferrari, following the curve of the rear haunch above a bronze forged wheel.',
      motion: { from: { s: 1.035, x: 0.01, y: -0.002 }, to: { s: 1.035, x: -0.01, y: -0.002 } },
    },
    {
      id: '90245',
      title: 'Rear three-quarter',
      sub: 'The complete car',
      alt: 'Rear three-quarter view of the whole graphite Ferrari parked in front of a dark garage door, with bronze forged wheels and yellow brake calipers.',
      motion: { from: { s: 1.05, x: -0.006, y: -0.006 }, to: { s: 1.0, x: 0, y: 0 } },
    },
  ];
  const N = SLIDES.length;
  const INDEX_BY_ID = new Map(SLIDES.map((s, i) => [s.id, i]));

  // ---------- DOM ----------

  const $ = (id) => document.getElementById(id);
  const ui = {
    root: $('player'),
    stage: $('stage'),
    loader: $('loader'),
    loaderText: $('loader-text'),
    empty: $('empty'),
    progress: $('progress-fill'),
    countCurrent: $('count-current'),
    countTotal: $('count-total'),
    caption: $('caption'),
    captionTitle: $('caption-title'),
    captionSub: $('caption-sub'),
    prev: $('btn-prev'),
    play: $('btn-play'),
    next: $('btn-next'),
    full: $('btn-full'),
    thumbsBtn: $('btn-thumbs'),
    fullscreen: $('btn-fullscreen'),
    thumbs: $('thumbs'),
    thumbList: $('thumb-list'),
    notice: $('notice'),
    noticeText: $('notice-text'),
    input: $('import-input'),
  };

  const reducedMQ = window.matchMedia('(prefers-reduced-motion: reduce)');
  const fineMQ = window.matchMedia('(hover: hover) and (pointer: fine)');

  // ---------- State ----------

  const photos = SLIDES.map(() => ({
    src: null, status: 'pending', promise: Promise.resolve(false),
    token: 0, img: null, w: 0, h: 0, objectUrl: null,
  }));

  const state = {
    clock: 0,          // the single playback clock, in ms
    playing: false,
    current: -1,       // slide currently on top
    target: -1,        // slide being navigated to (may still be decoding)
    slideStart: 0,     // clock time the current slide began its fade in
    navToken: 0,
    navPending: false,
    fullPhoto: false,
    reduced: reducedMQ.matches,
    motionWeight: reducedMQ.matches ? 0 : 1,
    started: false,
    resumeOnVisible: false,
    stageW: 0,
    stageH: 0,
  };

  let zTop = 1;
  const layers = [];
  let active = []; // visible layers, bottom → top

  for (let i = 0; i < LAYER_COUNT; i++) {
    const img = document.createElement('img');
    img.className = 'layer';
    img.alt = '';
    img.decoding = 'async';
    img.draggable = false;
    img.setAttribute('aria-hidden', 'true');
    ui.stage.insertBefore(img, ui.loader);
    layers.push({ img, slide: -1, born: 0, active: false, claim: 0, lastT: '', lastO: '' });
  }

  // ---------- Helpers ----------

  const clamp = (v, lo, hi) => Math.min(hi, Math.max(lo, v));
  const lerp = (a, b, t) => a + (b - a) * t;
  const pad = (n) => String(n).padStart(2, '0');
  const smoothstep = (t) => t * t * (3 - 2 * t);
  // Mostly linear drift with softened ends: calm but never visibly stopped.
  const drift = (t) => 0.55 * t + 0.45 * (0.5 - 0.5 * Math.cos(Math.PI * t));

  function usable(i) { return photos[i].status !== 'missing' && photos[i].src !== null; }

  function nextUsable(from, dir) {
    for (let k = 1; k <= N; k++) {
      const i = (((from + dir * k) % N) + N) % N;
      if (usable(i)) return i;
    }
    return -1;
  }

  // ---------- Photo discovery and loading ----------

  function matchName(name) {
    const m = NAME_RE.exec(name);
    return m ? INDEX_BY_ID.get('9024' + m[1]) : undefined;
  }

  /** Look for the photos in directory listings (works with most static servers). */
  async function discover() {
    const found = new Array(N).fill(null);
    if (location.protocol === 'http:' || location.protocol === 'https:') {
      for (const dir of PHOTO_DIRS) {
        try {
          const base = new URL(dir, location.href);
          const res = await fetch(base, { cache: 'no-store' });
          if (!res.ok || !(res.headers.get('content-type') || '').includes('html')) continue;
          const doc = new DOMParser().parseFromString(await res.text(), 'text/html');
          for (const a of doc.querySelectorAll('a[href]')) {
            const href = a.getAttribute('href');
            let name = href.split(/[?#]/)[0].split('/').pop() || '';
            try { name = decodeURIComponent(name); } catch (_) { /* keep raw */ }
            const i = matchName(name);
            if (i !== undefined && !found[i]) found[i] = new URL(href, base).href;
          }
        } catch (_) { /* no listing available; fall back below */ }
      }
    }
    // Fallback (also used for file://): the canonical names in photos/.
    return found.map((url, i) => url || `photos/${SLIDES[i].id}.jpg`);
  }

  function loadPhoto(i, src) {
    const p = photos[i];
    const token = ++p.token;
    p.src = src;
    p.status = 'loading';
    renderThumb(i);
    const img = new Image();
    img.decoding = 'async';
    img.src = src;
    p.promise = img.decode()
      .then(() => true, () => img.complete && img.naturalWidth > 0)
      .then((ok) => {
        if (token !== p.token) return photos[i].promise; // superseded by an import
        p.status = ok ? 'ready' : 'missing';
        if (ok) {
          p.img = img; // keep a reference so the decoded bitmap stays warm
          p.w = img.naturalWidth;
          p.h = img.naturalHeight;
          setAspect(p.w, p.h);
        }
        renderThumb(i);
        updateLoader();
        updateNotice();
        return ok;
      });
    return p.promise;
  }

  let aspectSet = false;
  function setAspect(w, h) {
    if (aspectSet || !w || !h) return;
    aspectSet = true;
    ui.root.style.setProperty('--ar', `${w} / ${h}`);
    ui.root.style.setProperty('--ar-num', (w / h).toFixed(4));
  }

  function importFiles(fileList) {
    const ignored = [];
    let matched = 0;
    for (const file of fileList) {
      const i = matchName(file.name);
      if (i === undefined || !/^image\//.test(file.type || 'image/jpeg')) { ignored.push(file.name); continue; }
      const p = photos[i];
      const inUse = layers.some((l) => l.active && l.slide === i);
      if (p.objectUrl && !inUse) URL.revokeObjectURL(p.objectUrl);
      p.objectUrl = URL.createObjectURL(file);
      loadPhoto(i, p.objectUrl);
      matched++;
    }
    const msg = [];
    if (matched) msg.push(`Imported ${matched} photo${matched === 1 ? '' : 's'}.`);
    if (ignored.length) msg.push(`Ignored ${ignored.join(', ')} — names must end in 90241.jpg to 90248.jpg.`);
    updateNotice(msg.join(' '));
    if (!state.started) start();
  }

  // ---------- Navigation ----------

  async function show(index, opts = {}) {
    if (index < 0) return;
    const token = ++state.navToken;
    state.navPending = true;
    state.target = index;
    updateUI();

    const waitTimer = setTimeout(() => {
      if (token === state.navToken) ui.stage.classList.add('is-waiting');
    }, 160);

    let ok = await photos[index].promise;
    let layer = null;
    if (ok && token === state.navToken) {
      layer = acquireLayer(token);
      if (layer.img.getAttribute('src') !== photos[index].src) layer.img.src = photos[index].src;
      // Decode the layer itself before revealing it, so the fade never starts on a blank frame.
      try { await layer.img.decode(); } catch (_) { ok = layer.img.naturalWidth > 0; }
    }
    clearTimeout(waitTimer);
    if (token !== state.navToken) return; // superseded by newer navigation
    ui.stage.classList.remove('is-waiting');
    state.navPending = false;

    if (!ok) {
      photos[index].status = 'missing';
      renderThumb(index);
      updateNotice();
      const alt = nextUsable(index, opts.dir || 1);
      if (alt >= 0 && alt !== state.current) { show(alt, opts); return; }
      state.target = state.current;
      updateUI();
      return;
    }
    activate(layer, index, opts);
  }

  function acquireLayer(token) {
    // Free = not visible, and not being prepared for the live navigation.
    let layer = layers.find((l) => !l.active && l.claim !== token);
    if (!layer) {
      layer = active.shift();
      deactivate(layer);
    }
    layer.claim = token;
    return layer;
  }

  function activate(layer, index, opts) {
    layer.claim = 0;
    layer.active = true;
    layer.slide = index;
    layer.born = state.clock;
    layer.lastO = '';
    layer.lastT = '';
    layer.img.style.opacity = '0';
    if (zTop > 1000) { // keep z-indices small and below the status overlays
      zTop = 1;
      for (const l of active) l.img.style.zIndex = String(++zTop);
    }
    layer.img.style.zIndex = String(++zTop);
    layer.img.alt = SLIDES[index].alt;
    layer.img.removeAttribute('aria-hidden');
    for (const l of active) l.img.setAttribute('aria-hidden', 'true');
    active.push(layer);
    while (active.length > LAYER_COUNT - 1) deactivate(active.shift());

    state.current = index;
    state.target = index;
    state.slideStart = state.clock;
    updateUI();
    if (opts.manual) scrollThumbIntoView(index);
    kick();
  }

  function deactivate(layer) {
    if (!layer) return;
    layer.active = false;
    layer.img.style.opacity = '0';
    layer.img.setAttribute('aria-hidden', 'true');
    layer.lastO = '0';
  }

  function go(dir) {
    const from = state.target >= 0 ? state.target : state.current;
    const i = nextUsable(from, dir);
    if (i >= 0 && (i !== state.current || state.navPending)) show(i, { dir, manual: true });
  }

  function goTo(i) {
    if (!usable(i)) { openImport(); return; }
    if (i === state.current && !state.navPending) return;
    show(i, { dir: i > state.current ? 1 : -1, manual: true });
  }

  function setPlaying(on) {
    on = !!on && state.started && state.current >= 0;
    if (state.playing === on) return;
    state.playing = on;
    state.resumeOnVisible = false;
    updateUI();
    kick();
    wake();
  }

  // ---------- Playback loop ----------

  let rafId = 0;
  let lastNow = null;

  function kick() {
    if (!rafId) rafId = requestAnimationFrame(frame);
  }

  function isFading() {
    const top = active[active.length - 1];
    return !!top && state.clock - top.born < FADE_MS;
  }

  function frame(now) {
    rafId = 0;
    const dt = lastNow === null ? 0 : Math.min(now - lastNow, 50);
    lastNow = now;

    // Advance the playback clock. A fade that was already under way completes
    // even when paused, so a manual step while paused still crossfades.
    const fading = isFading();
    if (state.playing || fading) {
      let next = state.clock + dt;
      // While the next photo is still decoding, hold at the end of this slide.
      if (state.navPending && !fading) next = Math.min(next, Math.max(state.clock, state.slideStart + SLIDE_MS));
      state.clock = next;
    }

    const target = state.fullPhoto || state.reduced ? 0 : 1;
    if (state.motionWeight !== target) {
      const step = dt / BLEND_MS;
      state.motionWeight = target > state.motionWeight
        ? Math.min(target, state.motionWeight + step)
        : Math.max(target, state.motionWeight - step);
    }

    if (state.playing && !state.navPending && state.current >= 0 &&
        state.clock - state.slideStart >= SLIDE_MS) {
      const i = nextUsable(state.current, 1);
      if (i >= 0 && i !== state.current) show(i, { dir: 1 });
      else state.slideStart = state.clock; // only one photo available
    }

    render();

    if (state.playing || isFading() || state.motionWeight !== target) {
      rafId = requestAnimationFrame(frame);
    } else {
      lastNow = null;
    }
  }

  function transformFor(layer) {
    const W = state.stageW;
    const H = state.stageH;
    const m = SLIDES[layer.slide].motion;
    const photo = photos[layer.slide];
    const e = drift(clamp((state.clock - layer.born) / LIFE_MS, 0, 1));
    const k = state.motionWeight;

    const s = Math.max(1, 1 + (lerp(m.from.s, m.to.s, e) - 1) * k);
    let x = lerp(m.from.x, m.to.x, e) * k * W;
    let y = lerp(m.from.y, m.to.y, e) * k * H;

    // Size of the photo as drawn before scaling: cover fills the stage,
    // contain (Full photo) fits inside it.
    const r = photo.w && photo.h ? photo.w / photo.h : W / H;
    const cover = !state.fullPhoto;
    let bw;
    let bh;
    if ((W / H > r) === cover) { bw = W; bh = W / r; } else { bh = H; bw = H * r; }

    // Never let an edge of the photo enter the frame.
    const maxX = Math.max(0, (s * bw - W) / 2);
    const maxY = Math.max(0, (s * bh - H) / 2);
    x = clamp(x, -maxX, maxX);
    y = clamp(y, -maxY, maxY);
    // Keep the photographer's watermark band inside the frame where possible.
    const yMax = H / 2 - (WATERMARK_BOTTOM - 0.5) * s * bh;
    if (y > yMax) y = Math.max(yMax, -maxY);

    return `translate3d(${x.toFixed(2)}px, ${y.toFixed(2)}px, 0) scale(${s.toFixed(5)})`;
  }

  function render() {
    if (!state.stageW) measure();

    // Layers fully covered by an opaque layer above them can be released.
    let opaqueFrom = -1;
    for (let j = active.length - 1; j >= 0; j--) {
      if (state.clock - active[j].born >= FADE_MS) { opaqueFrom = j; break; }
    }
    if (opaqueFrom > 0) active.splice(0, opaqueFrom).forEach(deactivate);

    for (const layer of active) {
      const o = smoothstep(clamp((state.clock - layer.born) / FADE_MS, 0, 1));
      const oStr = o >= 1 ? '1' : o.toFixed(4);
      const tStr = transformFor(layer);
      if (oStr !== layer.lastO) { layer.img.style.opacity = oStr; layer.lastO = oStr; }
      if (tStr !== layer.lastT) { layer.img.style.transform = tStr; layer.lastT = tStr; }
    }

    const p = state.current >= 0 ? clamp((state.clock - state.slideStart) / SLIDE_MS, 0, 1) : 0;
    ui.progress.style.setProperty('--p', p.toFixed(4));
  }

  function measure() {
    const r = ui.stage.getBoundingClientRect();
    state.stageW = r.width || 1;
    state.stageH = r.height || 1;
  }

  // ---------- UI ----------

  function updateUI() {
    const shown = state.target >= 0 ? state.target : state.current;
    if (shown >= 0) {
      const slide = SLIDES[shown];
      ui.countCurrent.textContent = pad(shown + 1);
      if (ui.captionTitle.textContent !== slide.title) {
        ui.captionTitle.textContent = slide.title;
        ui.captionSub.textContent = slide.sub;
      }
    }
    ui.countTotal.textContent = pad(N);
    // Announce slide changes to screen readers only when not auto-advancing.
    ui.caption.setAttribute('aria-live', state.playing ? 'off' : 'polite');

    ui.root.classList.toggle('is-playing', state.playing);
    ui.play.setAttribute('aria-label', state.playing ? 'Pause slideshow' : 'Play slideshow');
    const canNav = state.started && SLIDES.some((_, i) => usable(i));
    ui.play.disabled = !canNav;
    ui.prev.disabled = !canNav;
    ui.next.disabled = !canNav;

    ui.full.setAttribute('aria-pressed', String(state.fullPhoto));
    ui.stage.classList.toggle('is-full', state.fullPhoto);

    for (const [i, btn] of thumbButtons.entries()) {
      if (i === shown) btn.setAttribute('aria-current', 'true');
      else btn.removeAttribute('aria-current');
    }
  }

  const thumbButtons = [];

  function buildThumbs() {
    SLIDES.forEach((slide, i) => {
      const li = document.createElement('li');
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'thumb is-pending';
      const img = document.createElement('img');
      img.alt = '';
      img.loading = 'lazy';
      img.decoding = 'async';
      img.draggable = false;
      img.hidden = true;
      const num = document.createElement('span');
      num.className = 'thumb-num';
      num.textContent = pad(i + 1);
      btn.append(img, num);
      btn.addEventListener('click', () => { goTo(i); wake(); });
      li.append(btn);
      ui.thumbList.append(li);
      thumbButtons.push(btn);
      renderThumb(i);
    });
  }

  function renderThumb(i) {
    const btn = thumbButtons[i];
    if (!btn) return;
    const p = photos[i];
    const slide = SLIDES[i];
    const img = btn.querySelector('img');
    const num = btn.querySelector('.thumb-num');
    btn.classList.toggle('is-missing', p.status === 'missing');
    btn.classList.toggle('is-pending', p.status === 'pending' || p.status === 'loading');
    if (p.status === 'ready') {
      if (img.getAttribute('src') !== p.src) img.src = p.src;
      img.hidden = false;
      num.textContent = pad(i + 1);
      btn.setAttribute('aria-label', `Photo ${i + 1} of ${N}: ${slide.title}`);
    } else if (p.status === 'missing') {
      img.hidden = true;
      num.textContent = slide.id;
      btn.setAttribute('aria-label', `Photo ${i + 1} of ${N}, ${slide.id}.jpg, not found. Import photos`);
    } else {
      btn.setAttribute('aria-label', `Photo ${i + 1} of ${N}: ${slide.title} (loading)`);
    }
  }

  function scrollThumbIntoView(i) {
    if (ui.thumbs.hidden) return;
    const btn = thumbButtons[i];
    const list = ui.thumbList;
    const left = btn.offsetLeft - (list.clientWidth - btn.offsetWidth) / 2;
    list.scrollTo({ left, behavior: state.reduced ? 'auto' : 'smooth' });
  }

  function setThumbsOpen(open) {
    ui.thumbs.hidden = !open;
    ui.thumbsBtn.setAttribute('aria-expanded', String(open));
    ui.thumbsBtn.setAttribute('title', open ? 'Hide thumbnails' : 'Show thumbnails');
    ui.root.classList.toggle('thumbs-open', open);
    try { localStorage.setItem('gb-thumbs', open ? '1' : '0'); } catch (_) { /* storage unavailable */ }
    requestAnimationFrame(() => { measure(); render(); if (open) scrollThumbIntoView(Math.max(0, state.current)); });
  }

  function updateLoader() {
    const done = photos.filter((p) => p.status === 'ready' || p.status === 'missing').length;
    ui.loaderText.textContent = `Loading photographs · ${done} / ${N}`;
  }

  let noticeExtra = '';
  function updateNotice(extra) {
    if (extra !== undefined) noticeExtra = extra;
    const missing = SLIDES.filter((_, i) => photos[i].status === 'missing').map((s) => s.id);
    const parts = [];
    if (missing.length && state.started) {
      parts.push(`${N - missing.length} of ${N} photos loaded. Missing: ${missing.map((id) => id + '.jpg').join(', ')}.`);
    }
    if (noticeExtra) parts.push(noticeExtra);
    ui.noticeText.textContent = parts.join(' ');
    ui.notice.hidden = parts.length === 0;
    const importBtn = ui.notice.querySelector('[data-import]');
    importBtn.hidden = missing.length === 0;
    updateUI();
  }

  function openImport() { ui.input.click(); }

  // ---------- Idle controls (desktop pointer only) ----------

  let idleTimer = 0;
  function wake() {
    ui.root.classList.remove('is-idle');
    clearTimeout(idleTimer);
    if (!fineMQ.matches || !state.playing) return;
    idleTimer = setTimeout(() => {
      const a = document.activeElement;
      const keyboardFocus = a && a !== document.body && a.matches && a.matches(':focus-visible');
      if (state.playing && !keyboardFocus) ui.root.classList.add('is-idle');
    }, IDLE_MS);
  }

  // ---------- Fullscreen ----------

  const fsEnabled = !!(document.fullscreenEnabled || document.webkitFullscreenEnabled);
  const fsElement = () => document.fullscreenElement || document.webkitFullscreenElement || null;

  function toggleFullscreen() {
    if (fsElement()) {
      (document.exitFullscreen || document.webkitExitFullscreen).call(document);
    } else {
      const el = ui.root;
      const req = el.requestFullscreen || el.webkitRequestFullscreen;
      const r = req && req.call(el);
      if (r && r.catch) r.catch(() => {});
    }
  }

  function onFullscreenChange() {
    const on = fsElement() === ui.root;
    ui.fullscreen.setAttribute('aria-pressed', String(on));
    ui.fullscreen.setAttribute('aria-label', on ? 'Exit full screen' : 'Full screen');
    ui.fullscreen.querySelector('.mode-label').textContent = on ? 'Exit full screen' : 'Full screen';
  }

  // ---------- Events ----------

  function bind() {
    ui.prev.addEventListener('click', () => { go(-1); wake(); });
    ui.next.addEventListener('click', () => { go(1); wake(); });
    ui.play.addEventListener('click', () => setPlaying(!state.playing));
    ui.full.addEventListener('click', () => {
      state.fullPhoto = !state.fullPhoto;
      updateUI();
      kick();
    });
    ui.thumbsBtn.addEventListener('click', () => setThumbsOpen(ui.thumbs.hidden));

    if (fsEnabled) {
      ui.fullscreen.hidden = false;
      ui.fullscreen.setAttribute('aria-label', 'Full screen');
      ui.fullscreen.addEventListener('click', toggleFullscreen);
      document.addEventListener('fullscreenchange', onFullscreenChange);
      document.addEventListener('webkitfullscreenchange', onFullscreenChange);
    }

    document.querySelectorAll('[data-import]').forEach((b) => b.addEventListener('click', openImport));
    ui.input.addEventListener('change', () => {
      if (ui.input.files && ui.input.files.length) importFiles(ui.input.files);
      ui.input.value = '';
    });
    // Drag and drop photos anywhere on the page.
    window.addEventListener('dragover', (e) => {
      if (e.dataTransfer && [...e.dataTransfer.types].includes('Files')) e.preventDefault();
    });
    window.addEventListener('drop', (e) => {
      if (!e.dataTransfer || !e.dataTransfer.files.length) return;
      e.preventDefault();
      importFiles(e.dataTransfer.files);
    });

    document.addEventListener('keydown', (e) => {
      if (e.defaultPrevented || e.altKey || e.ctrlKey || e.metaKey) return;
      const t = e.target instanceof Element ? e.target : null;
      if (t && (t.closest('input, textarea, select') || t.isContentEditable)) return;
      if (e.key === 'ArrowRight') { e.preventDefault(); go(1); wake(); }
      else if (e.key === 'ArrowLeft') { e.preventDefault(); go(-1); wake(); }
      else if (e.key === ' ' || e.key === 'Spacebar') {
        // A focused button already activates on Space; don't double-handle it.
        if (t && t.closest('button, a[href], summary, [role="button"]')) return;
        e.preventDefault();
        setPlaying(!state.playing);
      }
    });

    // Swipe: touch-action: pan-y leaves vertical scrolling to the browser,
    // which cancels the pointer when it takes over the gesture.
    let swipe = null;
    ui.stage.addEventListener('pointerdown', (e) => {
      if (e.pointerType === 'mouse' || !e.isPrimary) return;
      swipe = { id: e.pointerId, x: e.clientX, y: e.clientY, t: performance.now() };
    });
    ui.stage.addEventListener('pointerup', (e) => {
      if (!swipe || e.pointerId !== swipe.id) return;
      const dx = e.clientX - swipe.x;
      const dy = e.clientY - swipe.y;
      const dt = performance.now() - swipe.t;
      swipe = null;
      if (Math.abs(dx) > 40 && Math.abs(dx) > 1.5 * Math.abs(dy) && dt < 900) go(dx < 0 ? 1 : -1);
    });
    ui.stage.addEventListener('pointercancel', () => { swipe = null; });

    ['pointermove', 'pointerdown', 'focusin'].forEach((type) =>
      document.addEventListener(type, wake, { passive: true }));
    document.addEventListener('keydown', wake);

    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        if (state.playing) { setPlaying(false); state.resumeOnVisible = true; }
      } else if (state.resumeOnVisible) {
        setPlaying(true);
      }
    });

    const onReducedChange = () => {
      state.reduced = reducedMQ.matches;
      if (state.reduced) setPlaying(false);
      kick();
    };
    if (reducedMQ.addEventListener) reducedMQ.addEventListener('change', onReducedChange);
    else if (reducedMQ.addListener) reducedMQ.addListener(onReducedChange);

    if ('ResizeObserver' in window) {
      new ResizeObserver(() => { measure(); render(); }).observe(ui.stage);
    } else {
      window.addEventListener('resize', () => { measure(); render(); });
    }
  }

  // ---------- Boot ----------

  async function start() {
    for (let i = 0; i < N; i++) {
      if (!photos[i].src) continue;
      const ok = await photos[i].promise;
      if (state.started) return; // an import already started playback
      if (ok) {
        state.started = true;
        ui.empty.hidden = true;
        ui.loader.classList.add('is-done');
        ui.loader.setAttribute('aria-hidden', 'true');
        await show(i, { dir: 1 });
        setPlaying(!state.reduced); // reduced motion: no autoplay by default
        updateNotice();
        return;
      }
    }
    ui.loader.classList.add('is-done');
    ui.empty.hidden = false;
    updateNotice();
  }

  async function boot() {
    buildThumbs();
    bind();
    let open = window.innerWidth >= 900;
    try { const saved = localStorage.getItem('gb-thumbs'); if (saved !== null) open = saved === '1'; } catch (_) { /* ignore */ }
    setThumbsOpen(open);
    updateUI();
    updateLoader();
    const urls = await discover();
    urls.forEach((url, i) => { if (!photos[i].src) loadPhoto(i, url); });
    start();
  }

  // Read-only hook for automated checks.
  Object.defineProperty(window, 'photoSlider', {
    value: Object.freeze({
      snapshot: () => ({
        clock: state.clock,
        playing: state.playing,
        current: state.current,
        target: state.target,
        navPending: state.navPending,
        fullPhoto: state.fullPhoto,
        motionWeight: state.motionWeight,
        progress: state.current >= 0 ? clamp((state.clock - state.slideStart) / SLIDE_MS, 0, 1) : 0,
        status: photos.map((p) => p.status),
        active: active.map((l) => ({ slide: l.slide, opacity: l.img.style.opacity, transform: l.img.style.transform })),
      }),
    }),
  });

  boot();
})();
