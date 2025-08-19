// Read near-expiry items from body dataset
const alertItemsRaw = document.body.dataset.alertItems || "[]";
let alertItems = [];

try {
  alertItems = JSON.parse(alertItemsRaw);
} catch (e) {
  alertItems = [];
}

// Show popup alert
if (Array.isArray(alertItems) && alertItems.length > 0) {
  alert("⚠️ Near expiry: " + alertItems.join(", "));
}
