document.querySelector("form").addEventListener("submit", (event) => {
  event.preventDefault();

  const email = document.querySelector("#email").value;
  const pass = document.querySelector("#password").value;
  const errorDiv = document.querySelector("#error");

  chrome.runtime.sendMessage(
    { message: "login", payload: { email, password: pass } },
    function (response) {
      if (response === "success") {
        chrome.action.setPopup({ popup: "/pages/user.html" });
      } else {
        const errorMessage = `<p style="font-size: 16px;color: red;text-align: center;">${response}</p>`;
        errorDiv.insertAdjacentHTML("afterbegin", errorMessage);
      }
    }
  );
});
