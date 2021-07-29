/**
 * Presents what the server and Watson said to the user.
 * @param {string} message      The message to show the user.
 * @param {*} item              A List of strings that are options.
 * @param {number} numButtons   The number of options to show.
 */
function watsonChat(message, items, numButtons) {
    var chatbox = document.getElementById("conversation");
    var bubble = document.createElement("div");

    bubble.classList.add("robart");

    var msg = document.createElement('p');
    msg.innerHTML = message;
    
    bubble.appendChild(msg)

    if (items.length > 1) {
        console.log("in the vague block")
        var buttons = document.createElement("div");
        buttons.setAttribute("id", "options")
        buttons.setAttribute("type", "button")

        for (i = 0; i < numButtons; i++) {
            let button = document.createElement("input");
            button.type
            button.value = items[i]
            buttons.appendChild(button)
        }

        bubble.appendChild(buttons)
    }
    chatbox.appendChild(bubble)
    chatbox.scrollTo(0, chatbox.scrollHeight)
}

/**
 * Displays the message sent by the user to Watson.
 * @param {string} msg The messages sent to Watson.
 */
function userChat(msg) {
    var chatbox = document.getElementById("conversation");
    var bubble = document.createElement("div");
    bubble.classList.add("user")
    var message = document.createElement('p');
    message.innerHTML = msg;
    bubble.appendChild(message);
    chatbox.appendChild(bubble)
    chatbox.scrollTo(0, chatbox.scrollHeight)
}

// Exports the functions.
module.exports = { watsonChat, userChat }