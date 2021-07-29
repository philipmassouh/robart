// Required modules.
const fs = require('fs')
const { contextBridge } = require("electron");
const { IamAuthenticator } = require('ibm-watson/auth');
const AssistantV2 = require('ibm-watson/assistant/v2');
const SpeechToTextV1 = require('ibm-watson/speech-to-text/v1');
const https = require('http');
const auth = require('../../restAuth.json');
const chat = require('./chat.js');
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
var recognizeStream = speechToText.recognizeUsingWebSocket(params), 
    assistant_session = null;

// Listen for events.
recognizeStream.on('data', function(event) { onEvent('data', event); });
recognizeStream.on('error', function(event) { onEvent('Error:', event); });
recognizeStream.on('close', function(event) { onEvent('Close:', event); });

/**
 * Manages the different events Watson can 
 * experiance after a response is recived.
 * @param {string} name The name of the event that has happened.
 * @param {*} event     The event object from Watson.
 */
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

/**
 * Manages the servers response.
 * @param {Uint8Array} data The data from the server.
 * @param {string} code     The status code sent by the server.
 */
function server_res(data, code) {
    if (code == '409') {
        if (data.includes('No object found.')) {
            console.log("object not found")
            chat.watsonChat("Sorry I couldn't determine the item you were looking for, try rephrasing your statment.", [], -1)
        }
        else if (data.includes('Could not determine object.')) {
            text_d = new TextDecoder().decode(data)
            options = text_d.split('\r\n')
            chat.watsonChat("Hmm, that search returned multiple results. Which is it?", options.slice(1, options.length - 1), 3)
        }
    } else if (code == '200') {
        chat.watsonChat(new TextDecoder().decode(data), [], 0)
    }
    console.log(code)
}

/**
 * Sends a message to Watson and its response to the server.
 * @param {string} text     The message to be sent to Watson.
 * @param {string} hostname The server url or ip.
 */
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
        // Data from Watson.
        data = JSON.stringify(res.result)
        
        // PUT Header.
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
                server_res(d, res.statusCode)
            });
        });

        // Error log.
        req.on('error', err => {
            console.log(err)
        });

        // Write data.
        req.write(data);
        req.end();
    }).catch(() => {
        // Creates the session
        assistant.createSession({
            assistantId: assistant_id
        })
        .then((res) => {
            assistant_session = res.result.session_id;
            watson_assistant(text, hostname);
        })
        .catch(err => {
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
            chat.userChat(text)
            watson_assistant(text, hostname);
        },
        restart_server: (hostname) => {
            fetch('http://' + hostname + ':8000')
        }
    }
);