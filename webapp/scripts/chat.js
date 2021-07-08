function watsonChat(string, numButtons) {
    let chatbox = document.getElementByClass("chatbox");
    let bubble = document.createElement("div");
    bubble.classList.add("robart")
    bubble.textContent(string)
    if (numButtons > 0) {
        let options = string.split(",");
        let buttons = document.createElement("div");
        for (i = 0; i < numBubbles; i++) {
            let button = document.createElement("");
        }
        chatbox.append(buttons)
    }
    chatbox.append(bubble)
}



function userChat(string) {
    let chatbox = document.getElementByClass("chatbox");
    let bubble = document.createElement("div");
    bubble.classList.add("user")
    bubble.textContent(string)
    chatbox.append(bubble)
}