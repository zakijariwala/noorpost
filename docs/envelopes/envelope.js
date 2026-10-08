/* Lays out each envelope once its fonts have loaded, in the same Chromium that
   prints it.

   1. The letter flows: every line starts on face 1 and whole lines move to
      face 2 until face 1 fits. If face 2 then overflows, the letter steps down
      a quarter point and flows again — never below 9pt.
   2. Anything marked data-fit (fact panel, dense cards) shrinks in small steps
      until it fits, never below 82%.
   3. Whatever still overflows is outlined on screen, and window.__overflows
      lists it, so the build can fail instead of printing clipped text. */
(function () {
  function over(el) { return el.scrollHeight > el.clientHeight + 1; }

  function flow() {
    document.querySelectorAll('[data-flow]').forEach(function (src) {
      var face1 = src.closest('.face');
      var dst = document.getElementById(src.getAttribute('data-flow'));
      var face2 = dst.closest('.face');
      var sheets = [src.closest('.page'), dst.closest('.page')];
      var pt = parseFloat(getComputedStyle(sheets[0]).getPropertyValue('--letter-pt')) || 10.5;
      for (var guard = 0; guard < 12; guard++) {
        while (dst.firstChild) src.appendChild(dst.firstChild);
        sheets.forEach(function (p) { p.style.setProperty('--letter-pt', pt + 'pt'); });
        while (over(face1) && src.children.length > 1) dst.insertBefore(src.lastElementChild, dst.firstChild);
        if (!over(face2) || pt <= 9) break;
        pt -= 0.25;
      }
    });
  }

  function fit() {
    document.querySelectorAll('[data-fit]').forEach(function (el) {
      var box = el.closest('.face') || el.closest('.page');
      var z = 1;
      while (over(box) && z > 0.82) { z -= 0.02; el.style.zoom = z; }
    });
  }

  function flag() {
    var bad = [];
    document.querySelectorAll('.page, .face').forEach(function (el, i) {
      if (el.classList.contains('p-spread')) return;
      if (over(el)) { el.classList.add('overflows'); bad.push((el.id || el.className) + ' #' + i); }
    });
    window.__overflows = bad;
    window.__laidOut = true;
  }

  (document.fonts ? document.fonts.ready : Promise.resolve()).then(function () { flow(); fit(); flag(); });
})();
