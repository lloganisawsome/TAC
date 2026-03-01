// timeTracker.js

function pad(num) {
    return num.toString().padStart(2, '0');
}

// Convert HH:MM:SS to total seconds
function timeToSeconds(hms) {
    const [h, m, s] = hms.split(':').map(Number);
    return h * 3600 + m * 60 + s;
}

// Convert seconds to HH:MM:SS
function secondsToTime(sec) {
    const hours = pad(Math.floor(sec / 3600));
    sec %= 3600;
    const minutes = pad(Math.floor(sec / 60));
    const seconds = pad(sec % 60);
    return `${hours}:${minutes}:${seconds}`;
}

// Load existing time or start at 0
let storedTime = localStorage.getItem('timeon') || "00:00:00";
let previousSeconds = timeToSeconds(storedTime);

// Track session time
let startTime = new Date();

function updateTime() {
    const now = new Date();
    const sessionSeconds = Math.floor((now - startTime) / 1000);
    const totalSeconds = previousSeconds + sessionSeconds;

    // Store back in localStorage as HH:MM:SS
    localStorage.setItem('timeon', secondsToTime(totalSeconds));
}

// Update every second
setInterval(updateTime, 1000);

// Run immediately
updateTime();