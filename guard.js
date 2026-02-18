(function () {
    const allowedHost = "https://loganisawesome.github.io/TAC";
    const sessionKey = "tac_active_session";

    try {
        // 1. Check if file is embedded
        const isEmbedded = window.top !== window.self;

        // 2. Check if running on the official URL
        const correctHost = window.location.origin === allowedHost;

        // 3. Check if user already has an active session
        const activeSession = localStorage.getItem(sessionKey);

        // 4. Redirect if any checks fail
        if (!isEmbedded || !correctHost) {
            alert("This file can only be used from the official TAC site!");
            window.location.replace("https://www.google.com/");
            return;
        }

        if (activeSession) {
            alert("Another session is active. Only 1 session allowed per user!");
            window.location.replace("https://www.google.com/");
            return;
        }

        // 5. Mark this session as active
        localStorage.setItem(sessionKey, "true");

        // 6. Remove session flag when window/tab closes
        window.addEventListener("beforeunload", () => {
            localStorage.removeItem(sessionKey);
        });

        console.log("TAC guard passed! Continue loading...");
    } catch (e) {
        window.location.replace("https://www.google.com/");
    }
})();