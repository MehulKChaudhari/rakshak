document.querySelector("form").addEventListener("submit", (event) => {
  event.preventDefault();

  const email = document.querySelector("#email").value;
  const pass = document.querySelector("#password").value;

  chrome.runtime.sendMessage(
    { message: "login", payload: { email, password: pass } },
    function (response) {
      if (response === "success")
        chrome.tabs.update({ url: "/pages/user.html" });
    }
  );
});
