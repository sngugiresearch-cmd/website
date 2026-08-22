(function () {
  var ANALYTICS_CODE = '';
  if (ANALYTICS_CODE) {
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://gc.zgo.at/count.js';
    s.setAttribute('data-goatcounter', 'https://' + ANALYTICS_CODE + '.goatcounter.com/count');
    document.body.appendChild(s);
  }

  var btn = document.querySelector('.theme-btn');
  if (btn) {
    btn.addEventListener('click', function () {
      var root = document.documentElement;
      var next = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
      root.setAttribute('data-theme', next);
      try {
        localStorage.setItem('theme', next);
      } catch (e) {}
    });
  }

  var email = document.getElementById('copy-email');
  if (email) {
    var original = email.textContent;
    var resetTimer = null;
    email.addEventListener('click', function () {
      var done = function () {
        email.textContent = 'copied to clipboard';
        clearTimeout(resetTimer);
        resetTimer = setTimeout(function () {
          email.textContent = original;
        }, 1400);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(original).then(done, done);
      } else {
        var ta = document.createElement('textarea');
        ta.value = original;
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand('copy'); } catch (e) {}
        document.body.removeChild(ta);
        done();
      }
    });
  }
})();
