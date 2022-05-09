chrome.runtime.onInstalled.addListener(openTab);
// chrome.action.onClicked.addListener(openTab)

function openTab() {
  chrome.tabs.create({ url: "popup.html" });
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log("message called");
  if (request.message === "login") {
    chrome.tabs.update({ url: "/pages/user.html" });
    return true;
  } else if (request.message === "signup") {
    chrome.tabs.update({ url: "/pages/user.html" });
    return true;
  } else if (request.message === "logout") {
    chrome.tabs.update({ url: "/popup.html" });
    return true;
  } else if (request.message === "userStatus") {
    is_user_signed_in()
      .then((res) => {
        sendResponse({
          message: "success",
        });
      })
      .catch((err) => console.log(err));
    return true;
  }
});

function isUserSignedIn() {
  return new Promise((resolve) => {
    chrome.storage.local.get(["userStatus", "user_info"], function (response) {
      if (chrome.runtime.lastError)
        resolve({ userStatus: false, user_info: {} });
      resolve(
        response.userStatus === undefined
          ? { userStatus: false, user_info: {} }
          : { userStatus: response.userStatus, user_info: response.user_info }
      );
    });
  });
}
