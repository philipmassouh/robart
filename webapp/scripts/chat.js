function watsonChat(message, item, numButtons) {
    let chatbox = document.getElementByClass("chatbox");
    let bubble = document.createElement("div");
    bubble.classList.add("robart")
    bubble.textContent(string[0])
    if (numButtons > 1) {
        let options = string.split(",");
        let buttons = document.createElement("div");
        for (i = 0; i < numBubbles; i++) {
            let button = document.createElement("input");
            button.classList.add("btn")
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