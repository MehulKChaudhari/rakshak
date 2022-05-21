// Main business logic
let authToken;
chrome.storage.local.get("token", function (items) {
  if (items.token) {
    authToken = items.token;
  }
});

window.addEventListener("click", (event) => {
  const targetNode = event.target;
  console.log("cleickedede");
  const data = document.querySelectorAll("div.JdNBm");

  const messages = [];
  data.forEach((element) => {
    console.log(element.innerText);
    messages.push(element.innerText);
  });
  console.log("token", `Token ${authToken}`);

  fetch("http://localhost:8000/api/parse-string-social/", {
    method: "POST",
    body: JSON.stringify(messages),
    headers: {
      "Content-type": "application/json",
      Authorization: `Token ${authToken}`,
    },
  })
    .then((response) =>
      response
        .json()
        .then((data) => ({
          data: data,
          status: response.status,
        }))
        .then((res) => {
          console.log("res", data);+.
        })
    )
    .catch((err) => console.log(err));
  console.log("messages", messages);
});
