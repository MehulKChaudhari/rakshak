chrome.runtime.onInstalled.addListener(openTab);
// chrome.action.onClicked.addListener(openTab)

function openTab() {
  chrome.tabs.create({ url: "popup.html" });
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log("message called");
  if (request.message === "login") {
    authenticateUser("login", request.payload)
      .then((res) => {
        console.log("login valo",res);
        sendResponse(res);
      })
      .catch((err) => console.log(err));
    return true;
  } else if (request.message === "signup") {
    authenticateUser("signUp", request.payload)
      .then((res) => {
        console.log(res);
        sendResponse(res);
      })
      .catch((err) => console.log(err));
    return true;
  } else if (request.message === "logout") {
    authenticateUser("logout", request.payload)
      .then((res) => {
        console.log(res);
        sendResponse(res);
      })
      .catch((err) => console.log(err));
    return true;
  } else if (request.message === "userStatus") {
    isUserSignedIn()
      .then((res) => {
        sendResponse({
          message: "success",
          userStatus: { user_info: res.user_info.email },
        });
      })
      .catch((err) => console.log(err));
    return true;
  }
});

function isUserSignedIn() {
  return new Promise((resolve) => {
    chrome.storage.sync.get(["token", "user_info"], function (response) {
      if (chrome.runtime.lastError) resolve({ token: "", user_info: {} });
      resolve(
        response.token === ""
          ? { token: "", user_info: {} }
          : { token: response.token, user_info: response.user_info }
      );
    });
  });
}

function authenticateUser(type, user_info) {
  if (type === "signUp") {
    return fetch("http://localhost:8000/accounts/register/", {
      method: "POST",
      body: JSON.stringify(user_info),
      headers: { "Content-type": "application/json" },
    })
      .then((res) => {
        return new Promise((resolve) => {
          if (res.status !== 201) resolve("fail");
          resolve("success");
        });
      })
      .catch((err) => console.log(err));
  } else if (type === "login") {
    return fetch("http://localhost:8000/accounts/login/", {
      method: "POST",
      body: JSON.stringify(user_info),
      headers: {
        "Content-type": "application/json",
      },
    })
      .then((res) => {
        return new Promise((resolve) => {
          if (res.status !== 200) resolve("fail");

          chrome.storage.local.set(
            { token: res.message.token, name: res.message.profile.name },
            function (response) {
              if (chrome.runtime.lastError) {
                resolve("fail");
              }
              console.log("Value is set to " + response);
              resolve("success");
            }
          );
        });
      })
      .catch((err) => console.log(err));
  } else if (type === "logout") {
    return new Promise((resolve) => {
      chrome.storage.local.clear(function (response) {
        if (chrome.runtime.lastError) {
          resolve("fail");
        }

        resolve("success");
      });
    });
  }
}
