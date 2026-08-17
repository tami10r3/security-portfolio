// ─────────────────────────────────────────────
// Click-to-copy email, with a brief "copied" indicator.
// Applies to any element with a data-copy-email attribute.
// Falls back to normal mailto: behavior if the Clipboard API
// is unavailable or the copy fails.
// ─────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('[data-copy-email]').forEach((el) => {
    const originalText = el.textContent;
    let resetTimer = null;

    el.addEventListener('click', (e) => {
      const email = el.getAttribute('data-copy-email');

      if (!navigator.clipboard) return; // no Clipboard API: let mailto: proceed normally

      e.preventDefault();

      navigator.clipboard.writeText(email).then(() => {
        clearTimeout(resetTimer);
        el.textContent = 'copied ✓';
        el.classList.add('copied');

        resetTimer = setTimeout(() => {
          el.textContent = originalText;
          el.classList.remove('copied');
        }, 1600);
      }).catch(() => {
        // Clipboard write failed (e.g. permissions) — fall back to mailto:
        window.location.href = el.getAttribute('href');
      });
    });
  });
});
