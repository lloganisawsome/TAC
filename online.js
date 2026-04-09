// online.js — converted from ES module to regular script
// Uses dynamic import() so it works without type="module"

(async function() {

const { initializeApp } = await import("https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js");
const { getDatabase, ref, set } = await import("https://www.gstatic.com/firebasejs/10.8.0/firebase-database.js");

// Your Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyBQslLAFRlIRJqsiJ2WWeTNslO067bzKYM",
  authDomain: "taclogin-ab38e.firebaseapp.com",
  databaseURL: "https://taclogin-ab38e-default-rtdb.firebaseio.com",
  projectId: "taclogin-ab38e",
  storageBucket: "taclogin-ab38e.firebasestorage.app",
  messagingSenderId: "937853298051",
  appId: "1:937853298051:web:119ccc7b5499514bd442b6"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getDatabase(app);

function updateActiveUserStatus() {
  const username = localStorage.getItem('lastLoggedInUser');

  if (username) {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const timeString = `${hours}:${minutes}`;

    set(ref(db, 'activeUsers/' + username), {
      lastSeen: timeString,
      timestamp: now.getTime()
    })
    .then(() => console.log(`Pinged Firebase for: ${username}`))
    .catch((err) => console.error("Firebase Error:", err));
  } else {
    console.warn("No 'lastActiveUser' found in localStorage. Skipping update.");
  }
}

// Run immediately when page loads
updateActiveUserStatus();

// Then run every 60 seconds
setInterval(updateActiveUserStatus, 60000);

})();