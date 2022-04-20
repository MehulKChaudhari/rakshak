const protectButton = document.getElementById('protectMe');
protectButton.addEventListener('click', () => {
    chrome.runtime.sendMessage({type:'auth'}, (res) =>{
        console.log(res)
    })
})