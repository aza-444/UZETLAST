// UZEnergo Ta'minlash — Main JavaScript

document.addEventListener('DOMContentLoaded', function () {

  // ============================================================
  //  AOS INIT
  // ============================================================
  if (typeof AOS !== 'undefined') {
    AOS.init({ duration: 700, once: true, offset: 60, easing: 'ease-out-cubic' });
  }

  // ============================================================
  //  NAVBAR SCROLL + ACTIVE LINK
  // ============================================================
  const header   = document.getElementById('header');
  const navbar   = document.getElementById('navbar');
  const navLinks = document.querySelectorAll('.nav-link');
  const sections = document.querySelectorAll('section[id]');

  function updateNavbar() {
    if (window.scrollY > 50) {
      if (header) header.classList.add('scrolled');
      if (navbar) navbar.classList.add('scrolled');
    } else {
      if (header) header.classList.remove('scrolled');
      if (navbar) navbar.classList.remove('scrolled');
    }
    let cur = '';
    sections.forEach(s => {
      if (window.scrollY >= s.offsetTop - 120) cur = s.getAttribute('id');
    });
    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === '#' + cur) link.classList.add('active');
    });
  }
  window.addEventListener('scroll', updateNavbar, { passive: true });
  updateNavbar();

  // ============================================================
  //  MOBILE NAV TOGGLE
  // ============================================================
  const navToggle   = document.getElementById('navToggle');
  const navLinksMenu = document.getElementById('navLinks');

  if (navToggle && navLinksMenu) {
    navToggle.addEventListener('click', function () {
      navLinksMenu.classList.toggle('open');
      this.classList.toggle('open');
    });

    navLinksMenu.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', function (e) {
        const parentItem = this.closest('.nav-item');
        if (window.innerWidth <= 1200 && parentItem && parentItem.classList.contains('has-dropdown')) {
          e.preventDefault();
          parentItem.classList.toggle('open');
          return;
        }
        navLinksMenu.classList.remove('open');
        navToggle.classList.remove('open');
        document.querySelectorAll('.nav-item.has-dropdown').forEach(i => i.classList.remove('open'));
        document.querySelectorAll('.nav-dropdown-item').forEach(i => i.classList.remove('open'));
      });
    });

    navLinksMenu.querySelectorAll('.nav-dropdown-link').forEach(link => {
      link.addEventListener('click', function (e) {
        const pd   = this.closest('.nav-dropdown-item');
        const hasSub = pd && pd.querySelector('.nav-subdropdown');
        if (window.innerWidth <= 1200 && hasSub) {
          if (pd.querySelector('.nav-subdropdown a')) {
            e.preventDefault();
            e.stopPropagation();
            pd.classList.toggle('open');
          }
        }
      });
    });
  }

  // ============================================================
  //  SCROLL TO TOP BUTTON
  // ============================================================
  const scrollTopBtn = document.createElement('button');
  scrollTopBtn.className = 'scroll-top';
  scrollTopBtn.innerHTML = '<i class="bi bi-arrow-up"></i>';
  scrollTopBtn.setAttribute('aria-label', 'Tepaga qaytish');
  document.body.appendChild(scrollTopBtn);
  scrollTopBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  window.addEventListener('scroll', () => {
    scrollTopBtn.classList.toggle('visible', window.scrollY > 400);
  }, { passive: true });

  // ============================================================
  //  COUNTER ANIMATION
  // ============================================================
  function animateCounter(el) {
    const target = parseInt(el.dataset.target) || 0;
    const step   = target / (2000 / 16);
    let   cur    = 0;
    const timer  = setInterval(() => {
      cur += step;
      if (cur >= target) { cur = target; clearInterval(timer); }
      el.textContent = Math.floor(cur).toLocaleString();
    }, 16);
  }
  const counterObs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting && !e.target.dataset.counted) {
        e.target.dataset.counted = 'true';
        animateCounter(e.target);
      }
    });
  }, { threshold: 0.5 });
  document.querySelectorAll('.counter').forEach(c => counterObs.observe(c));

  // ============================================================
  //  CATALOG FILTER TABS
  // ============================================================
  const catTabs     = document.querySelectorAll('.cat-tab');
  const catalogCards = document.querySelectorAll('.catalog-card');
  catTabs.forEach(tab => {
    tab.addEventListener('click', function () {
      catTabs.forEach(t => t.classList.remove('active'));
      this.classList.add('active');
      const f = this.dataset.filter;
      catalogCards.forEach(card => {
        card.style.display = (f === 'all' || card.dataset.category === f) ? '' : 'none';
      });
    });
  });

  // ============================================================
  //  CONTACT FORM AJAX
  // ============================================================
  const contactForm = document.getElementById('contactForm');
  const formSuccess = document.getElementById('formSuccess');
  if (contactForm) {
    contactForm.addEventListener('submit', async function (e) {
      e.preventDefault();
      const btn = this.querySelector('[type="submit"]');
      const orig = btn.innerHTML;
      btn.innerHTML = '<i class="bi bi-hourglass-split"></i> Yuborilmoqda...';
      btn.disabled = true;
      try {
        const res  = await fetch(this.action, { method: 'POST', body: new FormData(this), headers: { 'X-Requested-With': 'XMLHttpRequest' } });
        const data = await res.json();
        if (data.success) {
          contactForm.style.display = 'none';
          if (formSuccess) formSuccess.style.display = 'flex';
          btn.innerHTML = orig;
          btn.disabled = false;
          setTimeout(() => {
            contactForm.reset();
            contactForm.style.display = 'flex';
            if (formSuccess) formSuccess.style.display = 'none';
          }, 5000);
        } else {
          showMessage(data.error || 'Xatolik yuz berdi', 'error');
          btn.innerHTML = orig; btn.disabled = false;
        }
      } catch {
        btn.innerHTML = orig; btn.disabled = false;
        showMessage('Server bilan bog\'liq muammo', 'error');
      }
    });
  }

  // ============================================================
  //  HERO — lightweight power-grid canvas + lazy video
  // ============================================================
  (function initHeroEnergy() {
    const hero = document.getElementById('bosh-sahifa');
    const canvas = document.getElementById('heroCanvas');
    const video = document.getElementById('heroVideo');
    if (!hero) return;

    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const saveData = !!(navigator.connection && navigator.connection.saveData);
    const slowNet = !!(navigator.connection && /2g/.test(navigator.connection.effectiveType || ''));

    // Floating particles
    const particlesEl = document.getElementById('particles');
    if (particlesEl && !reduceMotion) {
      const count = window.innerWidth < 768 ? 18 : 36;
      for (let i = 0; i < count; i++) {
        const p = document.createElement('span');
        p.className = 'particle';
        p.style.left = Math.random() * 100 + '%';
        p.style.animationDuration = (6 + Math.random() * 10) + 's';
        p.style.animationDelay = (Math.random() * 8) + 's';
        p.style.width = p.style.height = (1.5 + Math.random() * 2.5) + 'px';
        particlesEl.appendChild(p);
      }
    }

    // --- Canvas energy plexus (zero download, wind-farm / smart-grid style) ---
    if (canvas && !reduceMotion) {
      const ctx = canvas.getContext('2d', { alpha: true });
      let w = 0, h = 0, dpr = 1, raf = 0, running = false, t = 0;
      let nodes = [], edges = [], sparks = [];

      function themeColors() {
        const light = document.documentElement.getAttribute('data-theme') === 'light';
        const styles = getComputedStyle(document.documentElement);
        const primary = (styles.getPropertyValue('--primary') || '#e8910c').trim() || '#e8910c';
        const accent = (styles.getPropertyValue('--accent') || '#0284c7').trim() || '#0284c7';
        const hexToRgba = (hex, a) => {
          const h = hex.replace('#', '');
          if (h.length !== 6) return light ? `rgba(245,158,11,${a})` : `rgba(245,158,11,${a})`;
          const n = parseInt(h, 16);
          return `rgba(${(n >> 16) & 255},${(n >> 8) & 255},${n & 255},${a})`;
        };
        return light
          ? {
              line: hexToRgba(primary, 0.55),
              lineHi: hexToRgba(accent, 0.48),
              node: hexToRgba(primary, 1),
              nodeGlow: hexToRgba(primary, 0.55),
              spark: primary,
              spark2: accent,
              scan: hexToRgba(accent, 0.1),
              glowMul: 6,
              ambScale: 0.55,
              nodeAlpha: 1,
              sparkR: 16,
            }
          : {
              line: hexToRgba(primary, 0.5),
              lineHi: hexToRgba(accent, 0.42),
              node: hexToRgba(primary, 1),
              nodeGlow: hexToRgba(primary, 0.55),
              spark: primary,
              spark2: accent,
              scan: hexToRgba(accent, 0.09),
              glowMul: 6.5,
              ambScale: 0.7,
              nodeAlpha: 1,
              sparkR: 16,
            };
      }

      function dist(a, b) {
        const dx = a.x - b.x, dy = a.y - b.y;
        return Math.sqrt(dx * dx + dy * dy);
      }

      function rebuild() {
        dpr = Math.min(window.devicePixelRatio || 1, 1.5);
        w = hero.clientWidth;
        h = hero.clientHeight;
        canvas.width = Math.floor(w * dpr);
        canvas.height = Math.floor(h * dpr);
        canvas.style.width = w + 'px';
        canvas.style.height = h + 'px';
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

        const count = w < 480 ? 28 : w < 768 ? 42 : w < 1200 ? 58 : 72;
        const pad = Math.min(w, h) * 0.06;
        nodes = [];
        for (let i = 0; i < count; i++) {
          const biasY = Math.pow(Math.random(), 0.7);
          nodes.push({
            x: pad + Math.random() * (w - pad * 2),
            y: pad + biasY * (h - pad * 2),
            vx: (Math.random() - 0.5) * 0.18,
            vy: (Math.random() - 0.5) * 0.12,
            r: 1.4 + Math.random() * 1.8,
            phase: Math.random() * Math.PI * 2,
            bright: 0.4 + Math.random() * 0.6,
          });
        }

        const maxDist = w < 768 ? w * 0.22 : w * 0.18;
        edges = [];
        for (let i = 0; i < nodes.length; i++) {
          const near = [];
          for (let j = i + 1; j < nodes.length; j++) {
            const d = dist(nodes[i], nodes[j]);
            if (d < maxDist) near.push({ j, d });
          }
          near.sort((a, b) => a.d - b.d);
          near.slice(0, 3).forEach(({ j, d }) => edges.push({ a: i, b: j, d, maxD: maxDist }));
        }

        const sparkCount = edges.length ? (w < 768 ? 6 : 10) : 0;
        sparks = Array.from({ length: sparkCount }, (_, i) => ({
          e: i % edges.length,
          p: Math.random(),
          speed: 0.003 + Math.random() * 0.004,
          alt: i % 4 === 0,
        }));
      }

      function tickNodes() {
        const pad = 12;
        nodes.forEach((n) => {
          n.x += n.vx;
          n.y += n.vy;
          if (n.x < pad) { n.x = pad; n.vx *= -1; }
          if (n.x > w - pad) { n.x = w - pad; n.vx *= -1; }
          if (n.y < pad) { n.y = pad; n.vy *= -1; }
          if (n.y > h - pad) { n.y = h - pad; n.vy *= -1; }
        });
      }

      function draw() {
        if (!running) return;
        t += 1;
        tickNodes();
        const c = themeColors();
        ctx.clearRect(0, 0, w, h);

        // horizon scan sweep (substation monitor feel)
        const scanY = ((t * 0.6) % (h + 120)) - 60;
        const scan = ctx.createLinearGradient(0, scanY - 40, 0, scanY + 40);
        scan.addColorStop(0, 'transparent');
        scan.addColorStop(0.5, c.scan);
        scan.addColorStop(1, 'transparent');
        ctx.fillStyle = scan;
        ctx.fillRect(0, 0, w, h);

        // ambient center glow
        if (c.ambScale > 0) {
          const amb = ctx.createRadialGradient(w * 0.55, h * 0.42, 0, w * 0.55, h * 0.42, w * 0.6);
          amb.addColorStop(0, c.nodeGlow);
          amb.addColorStop(1, 'transparent');
          ctx.globalAlpha = c.ambScale;
          ctx.fillStyle = amb;
          ctx.fillRect(0, 0, w, h);
          ctx.globalAlpha = 1;
        }

        // connection mesh
        edges.forEach(({ a, b, d, maxD }) => {
          const n1 = nodes[a], n2 = nodes[b];
          const alpha = 0.15 + (1 - d / maxD) * 0.55;
          ctx.beginPath();
          ctx.moveTo(n1.x, n1.y);
          ctx.lineTo(n2.x, n2.y);
          ctx.strokeStyle = (a + b) % 5 === 0 ? c.lineHi : c.line;
          ctx.globalAlpha = alpha;
          ctx.lineWidth = 0.8;
          ctx.stroke();
          ctx.globalAlpha = 1;
        });

        // energy sparks along lines
        sparks.forEach((sp) => {
          if (!edges.length || !edges[sp.e]) return;
          sp.p += sp.speed;
          if (sp.p > 1) {
            sp.p = 0;
            sp.e = (sp.e + 1 + Math.floor(Math.random() * 4)) % edges.length;
          }
          const { a, b } = edges[sp.e];
          const n1 = nodes[a], n2 = nodes[b];
          const x = n1.x + (n2.x - n1.x) * sp.p;
          const y = n1.y + (n2.y - n1.y) * sp.p;
          const col = sp.alt ? c.spark2 : c.spark;
          const sparkR = c.sparkR;
          const glow = ctx.createRadialGradient(x, y, 0, x, y, sparkR);
          glow.addColorStop(0, col);
          glow.addColorStop(1, 'transparent');
          ctx.fillStyle = glow;
          ctx.beginPath();
          ctx.arc(x, y, sparkR, 0, Math.PI * 2);
          ctx.fill();
          ctx.beginPath();
          ctx.arc(x, y, 2.2, 0, Math.PI * 2);
          ctx.fillStyle = col;
          ctx.fill();
        });

        // glowing nodes
        nodes.forEach((n) => {
          const pulse = 0.5 + 0.5 * Math.sin(t * 0.04 + n.phase);
          const radius = n.r + pulse * 1.6;
          const glowR = radius * c.glowMul;
          const glow = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, glowR);
          glow.addColorStop(0, c.node);
          glow.addColorStop(0.4, c.nodeGlow);
          glow.addColorStop(1, 'transparent');
          ctx.fillStyle = glow;
          ctx.globalAlpha = n.bright * (0.5 + pulse * 0.5) * c.nodeAlpha;
          ctx.beginPath();
          ctx.arc(n.x, n.y, glowR, 0, Math.PI * 2);
          ctx.fill();
          ctx.beginPath();
          ctx.arc(n.x, n.y, radius, 0, Math.PI * 2);
          ctx.fillStyle = c.node;
          ctx.fill();
          ctx.globalAlpha = 1;
        });

        raf = requestAnimationFrame(draw);
      }

      function start() {
        if (running) return;
        running = true;
        draw();
      }
      function stop() {
        running = false;
        cancelAnimationFrame(raf);
      }

      rebuild();
      let resizeTimer;
      window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(rebuild, 150);
      }, { passive: true });

      const io = new IntersectionObserver((entries) => {
        entries.forEach((e) => { e.isIntersecting ? start() : stop(); });
      }, { threshold: 0.05 });
      io.observe(hero);

      document.addEventListener('visibilitychange', () => {
        if (document.hidden) stop();
        else if (hero.getBoundingClientRect().bottom > 0 && hero.getBoundingClientRect().top < window.innerHeight) start();
      });
    }

    // --- Lazy background video (optional, never blocks load) ---
    if (!video || reduceMotion || saveData || slowNet) return;

    const darkSrc = (video.dataset.srcDark || '').trim();
    const lightSrc = (video.dataset.srcLight || '').trim();
    if (!darkSrc && !lightSrc) return;

    let loaded = false;

    function currentSrc() {
      const light = document.documentElement.getAttribute('data-theme') === 'light';
      return (light ? (lightSrc || darkSrc) : (darkSrc || lightSrc));
    }

    function attachAndPlay(src) {
      if (!src) return;
      if (video.getAttribute('src') !== src) {
        video.setAttribute('src', src);
        video.load();
      }
      const play = () => {
        video.play().then(() => {
          video.classList.add('is-ready');
          hero.classList.add('has-video');
        }).catch(() => {});
      };
      if (video.readyState >= 2) play();
      else video.addEventListener('canplay', play, { once: true });
    }

    function loadVideo() {
      if (loaded) {
        attachAndPlay(currentSrc());
        return;
      }
      loaded = true;
      attachAndPlay(currentSrc());
    }

    const schedule = (fn) => {
      if ('requestIdleCallback' in window) requestIdleCallback(fn, { timeout: 2500 });
      else setTimeout(fn, 1200);
    };

    const vio = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          schedule(loadVideo);
          if (loaded) video.play().catch(() => {});
        } else if (loaded) {
          video.pause();
        }
      });
    }, { threshold: 0.15 });
    vio.observe(hero);

    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
      themeToggle.addEventListener('click', () => {
        if (!loaded) return;
        setTimeout(() => attachAndPlay(currentSrc()), 50);
      });
    }
  })();

  // ============================================================
  //  MESSAGE HELPER
  // ============================================================
  function showMessage(text, type = 'success') {
    let c = document.querySelector('.messages-container');
    if (!c) { c = document.createElement('div'); c.className = 'messages-container'; document.body.appendChild(c); }
    const m = document.createElement('div');
    m.className = `message-item message-${type}`;
    m.innerHTML = `<i class="bi bi-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i> ${text}`;
    c.appendChild(m);
    setTimeout(() => { m.style.cssText = 'opacity:0;transform:translateX(40px);transition:all .3s'; setTimeout(() => m.remove(), 300); }, 4000);
  }

  // ============================================================
  //  SMOOTH SCROLL
  // ============================================================
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', function (e) {
      const h = this.getAttribute('href');
      if (!h || h === '#') return;
      const t = document.querySelector(h);
      if (t) { e.preventDefault(); t.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
    });
  });

  // ============================================================
  //  THEME TOGGLE  (Dark / Light)
  // ============================================================
  const themeToggle = document.getElementById('themeToggle');
  const themeIcon   = document.getElementById('themeIcon');
  const ROOT        = document.documentElement;

  function applyTheme(theme) {
    ROOT.setAttribute('data-theme', theme);
    localStorage.setItem('uzet-theme', theme);
    if (themeIcon) {
      themeIcon.className = theme === 'light' ? 'bi bi-sun-fill' : 'bi bi-moon-stars-fill';
    }
  }

  applyTheme(localStorage.getItem('uzet-theme') || 'dark');

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      applyTheme((ROOT.getAttribute('data-theme') || 'dark') === 'dark' ? 'light' : 'dark');
    });
  }

  // ============================================================
  //  SEARCH SYSTEM
  // ============================================================
  const searchModal    = document.getElementById('searchModal');
  const searchTrigger  = document.getElementById('searchTrigger');
  const searchClose    = document.getElementById('searchClose');
  const searchBackdrop = document.getElementById('searchBackdrop');
  const searchInput    = document.getElementById('searchInput');
  const searchDefault  = document.getElementById('searchDefault');
  const searchResults  = document.getElementById('searchResultsList');
  const searchEmpty    = document.getElementById('searchEmpty');

  if (!searchModal) return;

  // --- Build index ---
  const INDEX = [];

  function getText(el) {
    return (el ? el.textContent.trim() : '').replace(/\s+/g, ' ');
  }

  // Page sections
  [
    { id: 'bosh-sahifa', icon: 'bi-house-fill',         label: 'Bosh sahifa / Главная / Home' },
    { id: 'haqimizda',   icon: 'bi-building-fill-gear', label: 'Kompaniya haqida / О компании / About' },
    { id: 'katalog',     icon: 'bi-grid-fill',          label: 'Katalog / Каталог / Catalog' },
    { id: 'xizmatlar',   icon: 'bi-tools',              label: 'Xizmatlar / Услуги / Services' },
    { id: 'yangiliklar', icon: 'bi-newspaper',          label: 'Yangiliklar / Новости / News' },
    { id: 'aloqa',       icon: 'bi-envelope-fill',      label: 'Aloqa / Контакты / Contact' },
  ].forEach(s => INDEX.push({ type: 'section', icon: s.icon, title: s.label, sub: '', anchor: '#' + s.id, group: 'Sahifalar', gIcon: 'bi-layout-text-sidebar' }));

  // Catalog
  document.querySelectorAll('#katalog .catalog-card').forEach(card => {
    const t = getText(card.querySelector('.catalog-title'));
    if (t) INDEX.push({ type: 'catalog', icon: 'bi-gear-fill', title: t, sub: getText(card.querySelector('.catalog-desc')).slice(0, 80), anchor: '#katalog', group: 'Katalog', gIcon: 'bi-grid-fill', el: card });
  });

  // Services
  document.querySelectorAll('#xizmatlar .catalog-card').forEach(card => {
    const t = getText(card.querySelector('.catalog-title'));
    if (t) INDEX.push({ type: 'service', icon: 'bi-tools', title: t, sub: getText(card.querySelector('.catalog-desc')).slice(0, 80), anchor: '#xizmatlar', group: 'Xizmatlar', gIcon: 'bi-tools', el: card });
  });

  // News
  document.querySelectorAll('#yangiliklar .news-card').forEach(card => {
    const t    = getText(card.querySelector('.news-title'));
    const date = getText(card.querySelector('.news-date'));
    const body = getText(card.querySelector('.news-text'));
    if (t) INDEX.push({ type: 'news', icon: 'bi-newspaper', title: t, sub: (date ? date + ' — ' : '') + body.slice(0, 60), anchor: '#yangiliklar', group: 'Yangiliklar', gIcon: 'bi-newspaper', el: card });
  });

  // --- Scoring ---
  function score(item, q) {
    const lq = q.toLowerCase();
    const t  = item.title.toLowerCase();
    const s  = item.sub.toLowerCase();
    if (t.startsWith(lq)) return 100;
    if (t.includes(lq))   return 80;
    if (s.includes(lq))   return 50;
    if (item.group.toLowerCase().includes(lq)) return 30;
    return 0;
  }

  function hl(text, q) {
    if (!q) return text;
    return text.replace(new RegExp(`(${q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi'), '<mark>$1</mark>');
  }

  let activeIdx    = -1;
  let currentItems = [];

  // --- Render ---
  function renderResults(query) {
    const q = query.trim();
    if (!q) {
      searchDefault.style.display = '';
      searchResults.style.display = 'none';
      searchEmpty.style.display   = 'none';
      activeIdx = -1;
      return;
    }
    searchDefault.style.display = 'none';

    const filtered = INDEX
      .map(item => ({ item, s: score(item, q) }))
      .filter(x => x.s > 0)
      .sort((a, b) => b.s - a.s)
      .map(x => x.item);

    currentItems = filtered;
    activeIdx    = -1;

    if (!filtered.length) {
      searchResults.style.display = 'none';
      searchEmpty.style.display   = '';
      return;
    }
    searchEmpty.style.display   = 'none';
    searchResults.style.display = '';

    // Group
    const groups = {};
    filtered.forEach(item => {
      if (!groups[item.group]) groups[item.group] = { icon: item.gIcon, items: [] };
      groups[item.group].items.push(item);
    });

    let html = '';
    Object.entries(groups).forEach(([name, g], gi) => {
      if (gi) html += '<div class="search-divider"></div>';
      html += `<div class="search-group"><div class="search-group-label"><i class="bi ${g.icon}"></i>${name}</div>`;
      g.items.slice(0, 6).forEach(item => {
        const idx = filtered.indexOf(item);
        html += `<div class="search-result-item" data-idx="${idx}" tabindex="-1">
          <div class="search-result-icon"><i class="bi ${item.icon}"></i></div>
          <div class="search-result-body">
            <div class="search-result-title">${hl(item.title, q)}</div>
            ${item.sub ? `<div class="search-result-sub">${item.sub}</div>` : ''}
          </div>
          <i class="bi bi-arrow-right search-result-arrow"></i>
        </div>`;
      });
      html += '</div>';
    });
    searchResults.innerHTML = html;

    searchResults.querySelectorAll('.search-result-item').forEach(el => {
      el.addEventListener('click', () => goToResult(parseInt(el.dataset.idx)));
    });
  }

  function setActive(idx) {
    const els = searchResults.querySelectorAll('.search-result-item');
    els.forEach(e => e.classList.remove('sr-active'));
    if (idx >= 0 && idx < els.length) {
      els[idx].classList.add('sr-active');
      els[idx].scrollIntoView({ block: 'nearest' });
    }
    activeIdx = idx;
  }

  function goToResult(idx) {
    const item = currentItems[idx];
    if (!item) return;
    closeSearch();
    setTimeout(() => {
      if (item.el) {
        item.el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        item.el.style.outline = '2px solid var(--primary)';
        item.el.style.outlineOffset = '4px';
        setTimeout(() => { item.el.style.outline = ''; item.el.style.outlineOffset = ''; }, 2000);
      } else {
        const t = document.querySelector(item.anchor);
        if (t) t.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }, 200);
  }

  // --- Open / Close ---
  function openSearch() {
    searchModal.classList.add('open');
    document.body.style.overflow = 'hidden';
    setTimeout(() => searchInput && searchInput.focus(), 60);
  }
  function closeSearch() {
    searchModal.classList.remove('open');
    document.body.style.overflow = '';
    if (searchInput) { searchInput.value = ''; renderResults(''); }
    activeIdx = -1;
  }

  if (searchTrigger)  searchTrigger.addEventListener('click', openSearch);
  if (searchClose)    searchClose.addEventListener('click', closeSearch);
  if (searchBackdrop) searchBackdrop.addEventListener('click', closeSearch);

  // Tip cards
  document.querySelectorAll('.search-tip-card').forEach(card => {
    card.addEventListener('click', () => {
      const sec = card.dataset.section;
      closeSearch();
      setTimeout(() => {
        const t = document.getElementById(sec);
        if (t) t.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 200);
    });
  });

  // Keyboard
  document.addEventListener('keydown', e => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      searchModal.classList.contains('open') ? closeSearch() : openSearch();
      return;
    }
    if (e.key === 'Escape' && searchModal.classList.contains('open')) { closeSearch(); return; }
    if (!searchModal.classList.contains('open')) return;
    const els = searchResults.querySelectorAll('.search-result-item');
    if (e.key === 'ArrowDown')  { e.preventDefault(); setActive(Math.min(activeIdx + 1, els.length - 1)); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); setActive(Math.max(activeIdx - 1, 0)); }
    else if (e.key === 'Enter') { e.preventDefault(); goToResult(activeIdx >= 0 ? activeIdx : 0); }
  });

  // Input
  if (searchInput) {
    let timer;
    searchInput.addEventListener('input', () => {
      clearTimeout(timer);
      timer = setTimeout(() => renderResults(searchInput.value), 120);
    });
  }

}); // end DOMContentLoaded
