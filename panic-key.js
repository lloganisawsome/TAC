// Disable back button by replacing history
window.history.pushState(null, null, window.location.href);
window.onpopstate = function () {
    window.history.go(1);
};

document.addEventListener("keydown", (e) => {
    if (e.key.toLowerCase() === "z") {
        // Instant redirect
        window.location.replace("https://launchpad.classlink.com/wisd");
    }
});