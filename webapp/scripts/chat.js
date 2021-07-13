/**
 * Presents what the server and Watson said to the user.
 * @param {string} message      The message to show the user.
 * @param {*} item              A List of strings that are options.
 * @param {number} numButtons   The number of options to show.
 */
function watsonChat(message, items, numButtons) {
    var chatbox = document.getElementById("chatbox");
    var bubble = document.createElement("div");
    bubble.classList.add("robart")
    bubble.innerText = message

    if (items.length > 1) {
        var buttons = document.createElement("div");

        for (i = 0; i < numButtons; i++) {
            let button = document.createElement("input");
            button.id = "TextToSend"
            button.classList.add("btn")
            //TODO one of these is redundant
            button.innerText = items[i]
            button.value = "Get" + items[i]
            buttons.appendChild(button)
        }

        chatbox.appendChild(buttons)
    }
    chatbox.appendChild(bubble)
}

/**
 * Displays the message sent by the user to Watson.
 * @param {string} msg The messages sent to Watson.
 */
function userChat(msg) {
    var chatbox = document.getElementById("chatbox");
    var bubble = document.createElement("div");
    bubble.classList.add("user")
    bubble.innerText = msg
    chatbox.appendChild(bubble)
    chatbox.scrollTo(0, chatbox.scrollHeight)
}

// Exports the functions.
module.exports = { watsonChat, userChat }