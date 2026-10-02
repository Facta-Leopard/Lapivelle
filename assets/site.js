(() => {
  const locales = ['ko', 'en', 'fr', 'zh-Hans', 'zh-Hant', 'ja', 'de', 'es'];
  const resolve = input => {
    if (!input) return null;
    const raw = input.trim().replaceAll('_', '-');
    const exact = locales.find(code => code.toLowerCase() === raw.toLowerCase());
    if (exact) return exact;
    try {
      const locale = new Intl.Locale(raw).maximize();
      const candidate = locale.language === 'zh' ? `zh-${locale.script}` : locale.language;
      return locales.includes(candidate) ? candidate : null;
    } catch { return null; }
  };
  if (document.body.dataset.root === 'true') {
    const legacy = {english: 'en', korean: 'ko', french: 'fr'};
    const requested = new URLSearchParams(location.search).get('lang') || legacy[location.hash.slice(1)];
    const locale = resolve(requested) || (navigator.languages || [navigator.language]).map(resolve).find(Boolean) || 'en';
    const page = document.body.dataset.page;
    if (['index.html', 'privacy.html', 'support.html'].includes(page)) {
      location.replace(new URL(`${locale}/${page}`, location.href).href);
    }
  }
  const menu = document.querySelector('.languages');
  if (menu) {
    document.addEventListener('click', event => {
      if (!menu.contains(event.target)) menu.open = false;
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && menu.open) {
        menu.open = false;
        menu.querySelector('summary').focus();
      }
    });
  }
})();
