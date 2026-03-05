import { initializeApp } from "firebase/app";
import { 
  getDatabase, 
  ref, 
  set, 
  onValue, 
  onDisconnect,
  serverTimestamp 
} from "firebase/database";

// 1. Your Firebase Configuration
const firebaseConfig = {
  apiKey: "AIzaSyBQslLAFRlIRJqsiJ2WWeTNslO067bzKYM",
  authDomain: "taclogin-ab38e.firebaseapp.com",
  databaseURL: "https://taclogin-ab38e-default-rtdb.firebaseio.com",
  projectId: "taclogin-ab38e",
  storageBucket: "taclogin-ab38e.firebasestorage.app",
  messagingSenderId: "937853298051",
  appId: "1:937853298051:web:119ccc7b5499514bd442b6"
};

// 2. Initialize Firebase and Database
const app = initializeApp(firebaseConfig);
const db = getDatabase(app);

// 3. Presence Logic
const username = localStorage.getItem("lastLoggedInUser");

if (username) {
  const activeUserRef = ref(db, "activeusers/" + username);
  const lastOnlineRef = ref(db, "users/" + username + "/lastOnline");
  const connectedRef = ref(db, ".info/connected");

  onValue(connectedRef, (snapshot) => {
    if (snapshot.val() === true) {
      console.log("Connected to Firebase!");

      // Set up instructions for when the user closes the app
      onDisconnect(activeUserRef).remove();
      onDisconnect(lastOnlineRef).set(serverTimestamp());

      // Set the user as active immediately upon connection
      set(activeUserRef, true)
        .then(() => console.log(`User ${username} is now online.`))
        .catch((error) => console.error("Write failed:", error));
    } else {
      console.log("Disconnected from Firebase.");
    }
  });
} else {
  console.warn("No username found in localStorage.");
}