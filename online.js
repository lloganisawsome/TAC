import { 
  getDatabase, 
  ref, 
  set, 
  remove, 
  onValue, 
  onDisconnect,
  serverTimestamp
} from "firebase/database";

const db = getDatabase(app);

const username = localStorage.getItem("lastLoggedInUser");

if (username) {
  const activeUserRef = ref(db, "activeusers/" + username);
  const lastOnlineRef = ref(db, "users/" + username + "/lastOnline");
  const connectedRef = ref(db, ".info/connected");

  onValue(connectedRef, (snapshot) => {
    if (snapshot.val() === true) {

      // 🔴 When user disconnects:
      onDisconnect(activeUserRef).remove();
      onDisconnect(lastOnlineRef).set(serverTimestamp());

      // 🟢 When user connects:
      set(activeUserRef, true);
    }
  });
}