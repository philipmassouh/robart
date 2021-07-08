const fs = require('fs')
const { contextBridge } = require("electron");
const { IamAuthenticator } = require('ibm-watson/auth');
const AssistantV2 = require('ibm-watson/assistant/v2');
const SpeechToTextV1 = require('ibm-watson/speech-to-text/v1');
const https = require('http');
const auth = require('../../restAuth.json');
//const chat = require('./chat.js');
const assistant_id = auth.assistant.assistantId;

// Authenticats stt. Note: only last for 60mins.
const speechToText = new SpeechToTextV1({
    authenticator: new IamAuthenticator({
      apikey: auth.speechToText.apikey,
    }),
    serviceUrl: auth.speechToText.serviceUrl
});

// Authenticats wa. Note: only last for 60mins.
const assistant = new AssistantV2({
    version: '2020-04-01',
    authenticator: new IamAuthenticator({
        apikey: auth.assistant.apikey,
    }),
    serviceUrl: auth.assistant.serviceUrl
});

//Sets up speech to text.
const params = {
    objectMode: true,
    contentType: 'audio/webm;codecs=opus',
    model: 'en-US_BroadbandModel'
};

// Create the stream.
var recognizeStream = speechToText.recognizeUsingWebSocket(params), assistant_session = null;

// Listen for events.
recognizeStream.on('data', function(event) { onEvent('data', event); });
recognizeStream.on('error', function(event) { onEvent('Error:', event); });
recognizeStream.on('close', function(event) { onEvent('Close:', event); });


function watsonChat(message, item, numButtons) {
    var chatbox = document.getElementById("chatbox");
    var bubble = document.createElement("div");
    bubble.classList.add("robart")
    bubble.innerText = message

    if (item.length > 1) {
        var buttons = document.createElement("div");

        for (i = 0; i < numButtons; i++) {
            let button = document.createElement("input");
            button.id = "TextToSend"
            button.classList.add("btn")
            //TODO one of these is redundant
            button.innerText = item[i]
            button.value = "Get" + item[i]
            buttons.appendChild(button)
        }

        chatbox.appendChild(buttons)
    }
    chatbox.appendChild(bubble)
}

function userChat(msg) {
    var chatbox = document.getElementById("chatbox");
    var bubble = document.createElement("div");
    bubble.classList.add("user")
    bubble.innerText = msg
    chatbox.appendChild(bubble)
}

// Display events on the console.
function onEvent(name, event) {
    if (name == "data") {
        var text = document.getElementById("TextToSend");
        if (text) {
            max = [0, 0];
            for (var i = 0; i < event.results[0].alternatives.length; i++) {
                e = event.results[0].alternatives[i];
                if(e.confidence > max[0]) {
                    max[0] = e.confidence;
                    max[1] = i;
                }
            }
            text.value = event.results[0].alternatives[max[1]].transcript;
        }
    }
};

function watson_assistant(text, hostname) {
    // Sends user message to watson.
    assistant.message({
        assistantId: assistant_id,
        sessionId: assistant_session,
        input: {
          'message_type': 'text',
          'text': text
          }
        })
    .then(res => {
        data = JSON.stringify(res.result)
        
        // Post options.
        var options = {
            hostname: hostname,
            port: 8000,
            path: '',
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': data.length
            }
        }

        // Makes the https request to update the robot.
        var req = https.request(options, res => {
            res.on('data', d => {
                if (res.statusCode == '409') {
                    if (d.includes('No object found.')) {
                        watsonChat("Sorry I couldn't determind the item you were looking for, try rephrasing your statment.", [], -1)
                    }
                    else if (d.includes('Could not determind object.')) {
                        text_d = new TextDecoder().decode(d)
                        options = text_d.split('\r\n')
                        watsonChat("Hmm, that search returned multiple results. Which is it?", options.slice(1, options.length - 1), 3)
                    }
                } else if (res.statusCode == '200') {
                    watsonChat(new TextDecoder().decode(d), [], 0)
                }
            });
        });

        // Error log.
        req.on('error', err => {
            console.log(err)
        });

        // Write data.
        req.write(data);
        req.end();
    }).catch(err => {
        // Creates the session
        assistant.createSession({
            assistantId: assistant_id
        })
        .then((res) => {
            assistant_session = res.result.session_id;
            watson_assistant(text, hostname);
        })
        .catch((err) => {
            console.log(err);
        });
    });
}

// Allows program to only use some prebuilt functions.
contextBridge.exposeInMainWorld(
    "watson",
    {
        stt: (array) => {
            // Toggles listening.
            recognizeStream.listening = !recognizeStream.listening;

            if (!recognizeStream.listening) {
                //Send audio to stream.
                fs.writeFileSync('./assets/audio', array);
                fs.createReadStream('./assets/audio').pipe(recognizeStream);
            } else {
                recognizeStream = speechToText.recognizeUsingWebSocket(params);
                recognizeStream.listening = true;

                recognizeStream.on('data', function(event) { onEvent('data', event); });
                recognizeStream.on('error', function(event) { onEvent('Error:', event); });
                recognizeStream.on('close', function(event) { onEvent('Close:', event); });
            }
        },
        wa: (text, hostname) => {
            userChat(text)
            watson_assistant(text, hostname);
        },
        restart_server: (hostname) => {
            fetch('http://' + hostname + ':8000')
        }
    }
);