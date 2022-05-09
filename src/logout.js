const protectButton = document.getElementById("Logout");

protectButton.addEventListener("click", () => {
    chrome.tabs.create({ active: true, url: "/pages/login.html" });
  });