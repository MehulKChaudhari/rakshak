const protectButton = document.getElementById("protectMe");

protectButton.addEventListener("click", () => {
  chrome.tabs.create({ active: true, url: "/pages/login.html" });
});

// var y = document.getElementById("login");
// y.addEventListener("click", openIndex);

function openIndex() {
  chrome.tabs.create({ active: true, url: "/pages/login.html" });
}

window.addEventListener("DOMContentLoaded", () => {
  chrome.storage.local.get("token", function (items) {
    if (items.token) {
      // chrome.tabs.update({ url: "/pages/user.html" });
      chrome.action.setPopup({ popup: "/pages/user.html" });
    }
  });
});
// document.addEventListener("load", () => {});
