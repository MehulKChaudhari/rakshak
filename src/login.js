document.querySelector("form").addEventListener("submit", (event) => {
  event.preventDefault();

  const email = document.querySelector("#email").value;
  const pass = document.querySelector("#password").value;

  chrome.runtime.sendMessage(
    { message: "login", payload: { email, pass } },
    function (response) {
      if (response === "success") window.location.replace("./popup.html");
    }
  );
});
