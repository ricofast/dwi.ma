/* dwi.ma — Minimal Alpine.js components + toast auto-dismiss */

document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.dw-toast[data-auto-dismiss]').forEach(function (toast) {
    var delay = parseInt(toast.dataset.autoDismiss, 10) || 5000;
    setTimeout(function () { dismissToast(toast); }, delay);
  });
});

function dismissToast(el) {
  el.classList.add('dw-toast-out');
  el.addEventListener('animationend', function () { el.remove(); }, { once: true });
}

function copyToClipboard(text, feedbackEl) {
  navigator.clipboard.writeText(text).then(function () {
    if (feedbackEl) {
      var original = feedbackEl.textContent;
      feedbackEl.textContent = 'تم النسخ';
      setTimeout(function () { feedbackEl.textContent = original; }, 1500);
    }
  });
}
