// Main business logic
let authToken;
chrome.storage.local.get("token", function (items) {
  if (items.token) {
    authToken = items.token;
  }
});

/**logic to find true values in server response */
function getTrueValues(object, value) {
  return Object.keys(object).find((key) => object[key] === value);
}

/** Event to scrap and send data to server */

window.addEventListener("click", (event) => {
  console.log("cleickedede");
  console.log("href", window.location);
  let data;
  if (window.location.host === "www.instagram.com") {
    data = document.querySelectorAll("div._acqu > div._ac1n");
  } else if (window.location.host === "twitter.com") {
    data = document.querySelectorAll('[data-testid="tweetText"]');
  } else if (window.location.host === "www.youtube.com") {
    data = document.querySelectorAll("#content");
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
          //** logic to hide and show messages to user based server response */
          .then((res) => {
            if (Object.values(res.data).indexOf(true) > -1) {
              /** creating wrapper  */
              const text = document.createElement("p");

              /** add rakshak test ID */
              text.setAttribute("data-id", "Rakshak_comment");

              /**Logic to add blur effect to backgorund div */

              if (window.location.host === "www.instagram.com") {
                const child = element.children;
                console.log("child", child);
                child[0].style.cssText =
                  "filter:blur(8px);background-color :red; padding:20px";
                element.appendChild(text);
              } else if (window.location.host === "twitter.com") {
                const parent = element.parentNode;
                parent.appendChild(text);
                element.style.cssText =
                  "filter:blur(8px);background-color :red; padding:10px";
              } else {
                element.style.cssText =
                  "filter:blur(8px);background-color :red; padding:10px";
                element.appendChild(text);
              }

              /** adding css to to created wrapper  */

              text.style.cssText =
                "display: block; position: absolute; color:black; width:inherit; z-index:1; border-radius: 5px; padding:12px";
              text.style.color = "black";
              const serverData = Object.keys(res.data).find(
                (key) => res.data[key] === true
              );
              console.log("server true", serverData);
              /**adding text to created wrapper */
              text.innerText = "This content has hate language";
            }
          })
      )
      .catch((err) => console.log(err));
  });
});
