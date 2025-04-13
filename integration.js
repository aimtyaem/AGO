// Base URL of the Azure WebApp API
const API_BASE_URL = "https://agochatbot.azurewebsites.net";

// Send sustainability goal choice to the backend
async function setSustainabilityGoal(choice) {
    try {
        const response = await axios.post(`${API_BASE_URL}/sustainability_goal`, { choice });
        appendMessage(response.data.message);
    } catch (error) {
        console.error("Error setting sustainability goal:", error);
    }
}

// Upload energy bill and process it
async function uploadEnergyBill(file) {
    const reader = new FileReader();
    reader.onload = async (e) => {
        const fileContent = e.target.result;
        try {
            const response = await axios.post(`${API_BASE_URL}/energy_bill`, { file_content: fileContent });
            appendMessage(JSON.stringify(response.data, null, 2));
        } catch (error) {
            console.error("Error processing energy bill:", error);
        }
    };
    reader.readAsText(file);
}

// Get recommendations based on analysis
async function getRecommendations(analysis) {
    try {
        const response = await axios.post(`${API_BASE_URL}/recommendations`, { analysis });
        appendMessage(response.data.recommendations);
    } catch (error) {
        console.error("Error getting recommendations:", error);
    }
}

// Fetch vTracker data and display it
async function fetchVTrackerData() {
    try {
        const response = await axios.get(`${API_BASE_URL}/vtracker_data`);
        const data = response.data;
        console.log("vTracker Data:", data); // Process and display as needed
    } catch (error) {
        console.error("Error fetching vTracker data:", error);
    }
}

// Example: Bind actions to UI buttons
document.getElementById('fileInput').addEventListener('change', (e) => {
    uploadEnergyBill(e.target.files[0]);
});