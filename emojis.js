(function() {
  var count = parseInt(localStorage.getItem('emojis'), 10);
  if (!count || count < 1) return;
  count = Math.min(count, 20);

  var pool = ['😀','🎉','🔥','💎','🚀','⭐','🍕','👾','🦄','💥','🎯','🌈','🍩','👻','🐸','💜','🎸','🌮','🧊','✨'];
  var W = window.innerWidth, H = window.innerHeight, SIZE = 48;

  for (var i = 0; i < count; i++) {
    (function(idx) {
      var el = document.createElement('div');
      el.textContent = pool[idx % pool.length];
      el.style.cssText = 'position:fixed;z-index:999999;font-size:' + SIZE + 'px;line-height:1;pointer-events:none;user-select:none;';
      document.body.appendChild(el);

      var x = Math.random() * (W - SIZE);
      var y = Math.random() * (H - SIZE);
      var dx = (1.5 + Math.random() * 2) * (Math.random() < 0.5 ? 1 : -1);
      var dy = (1.5 + Math.random() * 2) * (Math.random() < 0.5 ? 1 : -1);

      function frame() {
        x += dx; y += dy;
        if (x <= 0 || x >= window.innerWidth - SIZE) dx = -dx;
        if (y <= 0 || y >= window.innerHeight - SIZE) dy = -dy;
        x = Math.max(0, Math.min(x, window.innerWidth - SIZE));
        y = Math.max(0, Math.min(y, window.innerHeight - SIZE));
        el.style.left = x + 'px';
        el.style.top = y + 'px';
        requestAnimationFrame(frame);
      }
      frame();
    })(i);
  }
})();