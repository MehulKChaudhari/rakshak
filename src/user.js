const protectButton = document.querySelector("button");

protectButton.addEventListener("click", () => {
  chrome.runtime.sendMessage({ message: "logout" }, function (response) {
    if (response === "success") {
      chrome.action.setPopup({ popup: "/popup.html" });
    }
  });
});

const KMS = document.querySelector("#keepMeSafe");
const MFN = document.querySelector("#myFriendsAreNice");
const ILE = document.querySelector("#doNotScan");

let authToken;
chrome.storage.local.get("token", function (items) {
  if (items.token) {
    authToken = items.token;
  }
});

var rad = document.safetyForm.safetyMethod;
var prev = null;
for (var i = 0; i < rad.length; i++) {
  rad[i].addEventListener("change", function () {
    prev ? console.log(prev.value) : null;
    if (this !== prev) {
      prev = this;
    }
    updateProtectionLevel(this.value);
  });
}

function updateProtectionLevel(method) {
  fetch("http://localhost:8000/api/update-protection/", {
    method: "POST",
    body: JSON.stringify({ protection_level: method }),
    headers: {
      "Content-type": "application/json",
      Authorization: `Token ${authToken}`,
    },
  });
  console.log("asdhsiauad", method);
}

