const protectButton = document.querySelector("button");

protectButton.addEventListener("click", () => {
  chrome.runtime.sendMessage({ message: "logout" }, function (response) {
    if (response === "success") {
      chrome.tabs.update({ url: "/popup.html" });
    }
  });
});

var radios = document.getElementsByName('genderS');

for (var i = 0, length = radios.length; i < length; i++) {
  if (radios[i].checked) {
    // do whatever you want with the checked radio
    alert(radios[i].value);

    // only one radio can be logically checked, don't check the rest
    break;
  }
}