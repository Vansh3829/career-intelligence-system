document.addEventListener('DOMContentLoaded', function () {
  const copyBtn = document.getElementById('copyBtn');
  if (copyBtn) {
    copyBtn.addEventListener('click', function () {
      const a = document.getElementById('shortLink');
      if (!a) return;
      const text = a.href;
      navigator.clipboard.writeText(text).then(() => {
        copyBtn.innerText = 'Copied!';
        setTimeout(() => copyBtn.innerText = 'Copy', 2000);
      }).catch(() => {
        copyBtn.innerText = 'Press Ctrl+C to copy';
      });
    });
  }
});
