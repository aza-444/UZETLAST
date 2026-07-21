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
    // Hero animations removed as per design requirements
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
