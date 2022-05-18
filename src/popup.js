const protectButton = document.getElementById("protectMe");

protectButton.addEventListener("click", () => {
  chrome.tabs.create({ active: true, url: "/pages/login.html" });
});

document.addEventListener("DOMContentLoaded", () => {
  // var y = document.getElementById("login");
  // y.addEventListener("click", openIndex);
  chrome.storage.local.get("token", function (items) {
    if (items.token) {
      chrome.tabs.create({ url: "/pages/user.html" });
      chrome.browserAction.setPopup({ popup: "user.html" });
    }
  });
});

function openIndex() {
  chrome.tabs.create({ active: true, url: "/pages/login.html" });
}

// document.addEventListener("load", () => {});
