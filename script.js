/* Mobile menu */
const menu = document.querySelector('.menu');
const nav = document.getElementById('nav');
if (menu && nav) {
  menu.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    menu.setAttribute('aria-expanded', open);
  });
  nav.addEventListener('click', e => {
    if (e.target.closest('a')) {
      nav.classList.remove('open');
      menu.setAttribute('aria-expanded', 'false');
    }
  });
}

/* Footer year */
const yearEl = document.getElementById('year');
if (yearEl) yearEl.textContent = new Date().getFullYear();

/* Services dropdown: click/tap on the caret, Esc to close, click outside to close */
document.querySelectorAll('.dd').forEach(dd => {
  const btn = dd.querySelector('.dd-toggle');
  if (!btn) return;
  btn.addEventListener('click', () => {
    const open = dd.classList.toggle('open');
    btn.setAttribute('aria-expanded', open);
  });
  dd.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      dd.classList.remove('open');
      btn.setAttribute('aria-expanded', 'false');
      btn.focus();
    }
  });
});
document.addEventListener('click', e => {
  document.querySelectorAll('.dd.open').forEach(dd => {
    if (!dd.contains(e.target)) {
      dd.classList.remove('open');
      const b = dd.querySelector('.dd-toggle');
      if (b) b.setAttribute('aria-expanded', 'false');
    }
  });
});

/* Before/after sliders */
document.querySelectorAll('.ba-box').forEach(box => {
  const range = box.querySelector('.ba-range');
  const set = () => box.style.setProperty('--pos', range.value + '%');
  range.addEventListener('input', set);
  set();
});

/* Back to top */
const toTop = document.querySelector('.to-top');
if (toTop) {
  const toggle = () => { toTop.hidden = window.scrollY < 700; };
  window.addEventListener('scroll', toggle, { passive: true });
  toggle();
  toTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
}

/* Estimate form: builds a text message on the visitor's own device. Nothing is sent by the site. */
const estimateForm = document.getElementById('estimate-form');
if (estimateForm) {
  const i18n = JSON.parse(document.getElementById('form-i18n').textContent);
  const NL = String.fromCharCode(10);

  const buildMessage = () => {
    const f = new FormData(estimateForm);
    const val = key => (f.get(key) || '').toString().trim() || '-';
    return [
      i18n.hi,
      '',
      i18n.lbl.name + ': ' + val('name'),
      i18n.lbl.phone + ': ' + val('phone'),
      i18n.lbl.email + ': ' + val('email'),
      i18n.lbl.address + ': ' + val('address'),
      i18n.lbl.service + ': ' + val('service'),
      i18n.lbl.pref + ': ' + val('contact_pref'),
      '',
      i18n.lbl.details + ':',
      val('message')
    ].join(NL);
  };

  estimateForm.addEventListener('submit', e => {
    e.preventDefault();
    const text = buildMessage();
    document.getElementById('open-sms').href = 'sms:' + i18n.tel + '?&body=' + encodeURIComponent(text);
    const status = document.getElementById('copy-status');
    status.textContent = '';
    document.getElementById('copy-msg').onclick = async () => {
      try {
        await navigator.clipboard.writeText(text);
        status.textContent = i18n.copied;
      } catch (err) {
        status.textContent = i18n.copyfail;
      }
    };
    const result = document.getElementById('form-result');
    result.hidden = false;
    result.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  });
}
