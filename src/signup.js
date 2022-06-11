document.querySelector("form").addEventListener("submit", (event) => {
  event.preventDefault();

  const name = document.querySelector("#name").value;
  const email = document.querySelector("#email").value;
  const pass = document.querySelector("#password").value;

  chrome.runtime.sendMessage(
    { message: "signup", payload: { name, email, password: pass } },
    function (response) {
      if (response === "success")
        chrome.action.setPopup({ popup: "/pages/login.html" });
    }
  );
});
