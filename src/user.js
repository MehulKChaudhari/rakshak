const protectButton = document.querySelector("button");

protectButton.addEventListener("click", () => {
  chrome.runtime.sendMessage({ message: "logout" }, function (response) {
    if (response === "success") {
      chrome.tabs.update({ url: "/popup.html" });
    }
  });
});
