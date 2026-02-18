(function () {
  try {
    if (window.self === window.top) {
      window.location.replace("https://www.google.com/");
    }
  } catch (e) {
    window.location.replace("https://www.google.com/");
  }
})();