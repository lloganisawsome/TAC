const cursor = document.createElement("div");
cursor.id = "custom-cursor";
document.body.appendChild(cursor);

let isClicking = false;

function updateCursor(e) {
  if (isClicking) return;

  const el = document.elementFromPoint(e.clientX, e.clientY);

  if (!el) return;

  if (el.closest("input, textarea")) {
    cursor.style.backgroundImage = "url('text.png')";
  } 
  else if (
    el.closest("button, a, input[type='button'], input[type='submit'], .clickable")
  ) {
    cursor.style.backgroundImage = "url('hover.png')";
  } 
  else {
    cursor.style.backgroundImage = "url('normal.png')";
  }
}

document.addEventListener("mousemove", (e) => {
  cursor.style.left = e.clientX + "px";
  cursor.style.top = e.clientY + "px";
  updateCursor(e);
});

document.addEventListener("mousedown", () => {
  isClicking = true;
  cursor.style.backgroundImage = "url('click.png')";
  cursor.style.transform = "translate(-50%, -50%) scale(0.9)";
});

document.addEventListener("mouseup", (e) => {
  isClicking = false;
  cursor.style.transform = "translate(-50%, -50%) scale(1)";
  updateCursor(e); // immediately restore correct state
});