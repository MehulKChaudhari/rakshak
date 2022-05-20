// Main business logic

window.addEventListener("click", (event) => {
  const targetNode = event.target;
  console.log("cleickedede");
  const data = document.querySelectorAll("div.JdNBm");

  const messages = [];
  data.forEach((element) => {
    console.log(element.innerText);
    messages.push(element.innerText);
  });

  fetch("http://localhost:8000/api/parse-string-social/", {
    method: "POST",
    body: messages,
    headers: {
      "Content-type": "application/json",
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
          console.log("res", data);
        })
    )
    .catch((err) => console.log(err));
  console.log("messages", messages);
});
