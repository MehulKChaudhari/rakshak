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
  console.log("href", window.location);
  let data;
  if (window.location.host === "www.instagram.com") {
    data = document.querySelectorAll("div.JdNBm");
  } else if (window.location.host === "twitter.com") {
    data = document.querySelectorAll('[data-testid="tweetText"]');
  }

  data.forEach((element) => {
    console.log(element.innerText);
    fetch("http://localhost:8000/api/parse-string-social/", {
      method: "POST",
      body: JSON.stringify(element.innerText),
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
            console.log(
              "res",
              res.data,
              Object.values(res.data).indexOf(true) > -1
            );
            if (Object.values(res.data).indexOf(true) > -1) {
              element.style.filter = "blur(8px)";
              element.style.backgroundColor = "red";
            }
          })
      )
      .catch((err) => console.log(err));
  });
});
