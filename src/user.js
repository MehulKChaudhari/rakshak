const protectButton = document.querySelector("button");

protectButton.addEventListener("click", () => {
  chrome.runtime.sendMessage({ message: "logout" }, function (response) {
    if (response === "success") {
      chrome.tabs.update({ url: "/popup.html" });
    }
  });
});

var rad = document.safetyForm.safetyMethod;
var prev = null;
for (var i = 0; i < rad.length; i++) {
  rad[i].addEventListener("change", function () {
    prev ? console.log(prev.value) : null;
    if (this !== prev) {
      prev = this;
    }
    console.log(rad.value);
  });
}
