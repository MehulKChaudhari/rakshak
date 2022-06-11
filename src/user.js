const protectButton = document.querySelector("button");

protectButton.addEventListener("click", () => {
  chrome.runtime.sendMessage({ message: "logout" }, function (response) {
    if (response === "success") {
      chrome.action.setPopup({ popup: "/popup.html" });
    }
  });
});

// function myFunction(safetyLevel) {
//   console.log("safetyMethod", safetyLevel);
// }
document.safetyMethod.onClick = function () {
  console.log("dsadsd", document.safetyMethod.safetyMethod.value);
};
