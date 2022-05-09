const protectButton = document.getElementById("Logout");

protectButton.addEventListener("click", () => {
  chrome.runtime.sendMessage({ message: "logout" }, function (response) {
    if (response === "success") window.location.replace("./popup.html");
  });
});
