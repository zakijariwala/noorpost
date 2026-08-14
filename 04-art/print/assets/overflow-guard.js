/* Overflow guard — diagnostic only, screen only.
 *
 * .page uses `overflow: hidden`, which is correct for a trimmed page but means
 * content that does not fit is silently clipped. A clipped page still prints as
 * a clean, correct-looking PDF with text missing off the bottom, so the defect
 * is invisible in exactly the artifact you would check it in.
 *
 * This flags any page whose content is taller than the page itself, so the
 * problem shows up the moment the template is opened. It never runs in print
 * and changes no geometry.
 */
(function () {
  function mark() {
    document.querySelectorAll('.page').forEach(function (page) {
      var overflows = page.scrollHeight > page.clientHeight + 2;
      page.classList.toggle('overflows', overflows);
      if (overflows && !page.dataset.reported) {
        page.dataset.reported = '1';
        console.warn(
          'Page overflows by ' + (page.scrollHeight - page.clientHeight) + 'px ' +
          '(' + Math.round((page.scrollHeight - page.clientHeight) / page.clientHeight * 100) + '%): ' +
          document.title
        );
      }
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      if (document.fonts && document.fonts.ready) document.fonts.ready.then(mark);
      else mark();
    });
  } else {
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(mark);
    else mark();
  }
  window.addEventListener('resize', mark);
})();
