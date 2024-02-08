const firebaseConfig = {
    // ... Your Firebase configuration
    apiKey: "AIzaSyB9argUjBuHWnd3P6m2rCWh584Ez8_4v58",
    authDomain: "weather-station-554c2.firebaseapp.com",
    projectId: "weather-station-554c2",
    storageBucket: "weather-station-554c2.appspot.com",
    messagingSenderId: "786960725705",
    appId: "1:786960725705:web:91fd2d209b4173ed80bf18",
    measurementId: "G-7PPXC0YTW3",
};

// Initialize Firebase
const app = firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();

// Function to get data from localStorage
function getDataFromLocalStorage(key) {
    const data = localStorage.getItem(key);
    return data ? JSON.parse(data) : null;
}

// Function to save data to localStorage
function saveDataToLocalStorage(key, data) {
    localStorage.setItem(key, JSON.stringify(data));
}

// Function to initialize the toggle state from localStorage
function initializeToggleState() {
    const toggleState = getDataFromLocalStorage('toggleState');
    const togglingButton = document.getElementById("toggleBtn");
    const statePlacing = document.getElementById("statePlacing");
    const intervalId = document.getElementById("rangeval");

    if (toggleState) {
        if (toggleState.toggle === 1) {
            togglingButton.classList.add("active");
            togglingButton.textContent = "Activate";
            statePlacing.textContent = "Inactive";
            intervalId.textContent = toggleState.interval;
        } else {
            togglingButton.classList.remove("active");
            togglingButton.textContent = "Deactivate";
            statePlacing.textContent = "Active and time was set to " + toggleState.interval + " Minutes";
        }
    }
}

async function toggleButton() {
    const togglingButton = document.getElementById("toggleBtn");
    const statePlacing = document.getElementById("statePlacing");
    const intervalId = document.getElementById("rangeval").textContent;

    if (togglingButton) {
        if (togglingButton.classList.contains("active")) {
            togglingButton.classList.remove("active");
            togglingButton.textContent = "Deactivate";
            statePlacing.textContent = "Active and time was set to " + intervalId + " Minutes";

            // Save data to localStorage
            saveDataToLocalStorage('toggleState', { toggle: 1, interval: parseInt(intervalId) });

            await UpdateToggleState(1);
        } else {
            togglingButton.classList.add("active");
            togglingButton.textContent = "Activate";
            statePlacing.textContent = "Inactive";

            // Save data to localStorage
            saveDataToLocalStorage('toggleState', { toggle: 0, interval: 0 });

            await UpdateToggleState(2);
        }
    } else {
        console.error("Element with ID 'toggleBtn' not found");
    }
}

async function UpdateToggleState(num) {
    console.log("button running?", num);
    const snapshot = await db.collection("toggle-and-interval").get();

    snapshot.forEach((s) => {
        console.log(s.id, s.data());

        const d = s.data();

        if (num === 1) {
            db.collection("toggle-and-interval").doc(s.id).update({
                toggle: 1,
                interval: parseInt(document.getElementById("rangeval").textContent),
            });
        } else if (num === 2) {
            db.collection("toggle-and-interval").doc(s.id).update({
                toggle: 0,
                interval: 0,
            });
        }
    });
}

// Call initializeToggleState at the beginning
initializeToggleState();

// Call toggleButton after initializeToggleState
toggleButton();

function updateRangeValue(newValue) {
    document.getElementById("rangeval").textContent = newValue;
}
