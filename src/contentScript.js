window.addEventListener("click", (event) => {
  const targetNode = event.target;
  console.log("cleickedede");
  const data = document.querySelectorAll("div.JdNBm");

  data.forEach((element) => {
    console.log(element.innerText);

    if ((element.textContent || element.innerText).indexOf("Sale") > -1) {
      element.style.filter = "blur(5px)";
      element.style.backgroundColor = "red";
    }
  });
});
