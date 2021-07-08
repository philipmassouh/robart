function watsonChat(message, item, numButtons) {
    let chatbox = document.getElementByClass("chatbox");
    let bubble = document.createElement("div");
    bubble.classList.add("robart")
    bubble.textContent(message)

    if (item.length > 1) {
        let options = string.split(",");
        let buttons = document.createElement("div");

        for (i = 0; i < numBubbles; i++) {
            let button = document.createElement("input");
            button.id.add("TextToSend")
            button.classList.add("btn")
            //TODO one of these is redundant
            button.textContent(item[i])
            button.value = "Get" + item[i]
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