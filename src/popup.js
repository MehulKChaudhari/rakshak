const protectButton = document.getElementById("protectMe");

protectButton.addEventListener("click", () => {
  chrome.tabs.create({ active: true, url: "/pages/login.html" });
});

document.addEventListener("DOMContentLoaded", () => {
  var y = document.getElementById("login");
  y.addEventListener("click", openIndex);
});

function openIndex() {
  chrome.tabs.create({ active: true, url: "/pages/login.html" });
}
