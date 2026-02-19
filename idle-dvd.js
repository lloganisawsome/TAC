let idleTimer;
let isIdle = false;

// DVD screensaver state
let dvdX = 0;
let dvdY = 0;
let dvdDX = 2 + Math.random() * 3; // random speed
let dvdDY = 2 + Math.random() * 3;

// Save last real mouse position
let lastMouseX = 0;
let lastMouseY = 0;

function startIdleTimer() {
  clearTimeout(idleTimer);
  idleTimer = setTimeout(goIdle, 30000); // 30 seconds
}

// Trigger idle DVD animation
function goIdle() {
  isIdle = true;

  // Start from current cursor position
  dvdX = lastMouseX;
  dvdY = lastMouseY;

  // Use existing global cursor from custom-cursor.js
  cursor.style.backgroundImage = "url('dvd-logo.png')";

  animateDVD();
}

function animateDVD() {
  if (!isIdle) return;

  dvdX += dvdDX;
  dvdY += dvdDY;

  // Bounce off edges
  if (dvdX < 0 || dvdX > window.innerWidth - 32) dvdDX *= -1;
  if (dvdY < 0 || dvdY > window.innerHeight - 32) dvdDY *= -1;

  cursor.style.left = dvdX + "px";
  cursor.style.top = dvdY + "px";

  requestAnimationFrame(animateDVD);
}

// Any activity cancels idle
function resetIdle(e) {
  lastMouseX = e.clientX;
  lastMouseY = e.clientY;

  if (isIdle) {
    isIdle = false;
    cursor.style.backgroundImage = "url('normal.png')";
  }

  startIdleTimer();
}

// Track user activity
document.addEventListener("mousemove", resetIdle);
document.addEventListener("keydown", resetIdle);

startIdleTimer();