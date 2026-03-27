// app-presence.js
(function() {
    const currentUser = localStorage.getItem('lastLoggedInUser');
    if (!currentUser || currentUser === 'Unknown') return;

    // Use the document title as the default app name (e.g., "Not Games - TAC" becomes "Not Games")
    let baseApp = document.title.split('-')[0].trim() || 'TAC';
    let currentStatus = baseApp;

    function updatePresence() {
        if (typeof firebase !== 'undefined' && firebase.database) {
            const now = new Date();
            const timeStr = String(now.getHours()).padStart(2, '0') + ':' + String(now.getMinutes()).padStart(2, '0');
            
            // Notice we use .update() instead of .set() so we don't overwrite other data
            firebase.database().ref('activeUsers/' + currentUser).update({
                lastSeen: timeStr,
                timestamp: Date.now(),
                currentApp: currentStatus
            });
        }
    }

    // Delay slightly to ensure Firebase is initialized, then sync every 30 seconds
    setTimeout(updatePresence, 1500);
    setInterval(updatePresence, 30000);

    // Expose globally so games/apps can dynamically change their status without reloading
    window.setAppPresence = function(status) {
        currentStatus = status;
        updatePresence();
    };
})();