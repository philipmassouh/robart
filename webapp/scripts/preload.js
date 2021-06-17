const fs = require('fs')
const { contextBridge } = require("electron");
const { IamAuthenticator } = require('ibm-watson/auth');
const AssistantV2 = require('ibm-watson/assistant/v2');
const SpeechToTextV1 = require('ibm-watson/speech-to-text/v1');
const https = require('http');

const assistant_id = 'b5428c83-d98e-46e5-ad29-8db5cd50ea16';

// Authenticats stt. Note: only last for 60mins.
const speechToText = new SpeechToTextV1({
    authenticator: new IamAuthenticator({
      apikey: 'R9hW3VQy4vgbFAHYoq9WWnzKoI5QioBVH9UAsWovlwVk',
    }),
    serviceUrl: 'https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/1aafab97-84e5-4963-8fdc-8d078b522a15',
});

// Authenticats wa. Note: only last for 60mins.
const assistant = new AssistantV2({
    version: '2020-04-01',
    authenticator: new IamAuthenticator({
        apikey: 'nK1ePaVkS-Vnd9vmVFFr7Y-Pcso0-whbsVPRLqX2e87r',
    }),
    serviceUrl: 'https://api.us-south.assistant.watson.cloud.ibm.com/instances/7e0acc43-e72c-44b6-ae40-3ce992047bd2'
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

//Creates session.
assistant.createSession({
    assistantId: assistant_id
  })
    .then(res => {
      assistant_session = res.result.session_id;
    })
    .catch(err => {
      console.log(err);
    });

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
                // Finds the highest confident intent.
                max = [0, 0];
                for (var i = 0; i < res.result.output.intents.length; i++) {
                    e = res.result.output.intents[i];
                    if(e.confidence > max[0]) {
                        max[0] = e.confidence;
                        max[1] = i;
                    }
                }
                var intent = res.result.output.intents[max[1]].intent;

                // Finds the highest confident entity to get.
                max = [0, 0];
                for (var i = 0; i < res.result.output.entities.length; i++) {
                    e = res.result.output.entities[i];
                    if(e.confidence > max[0]) {
                        max[0] = e.confidence;
                        max[1] = i;
                    }
                }
                var value = res.result.output.entities[max[1]].value;

                // Turns data into json
                var data = JSON.stringify({
                    intent: intent,
                    value: value
                });

                // Post options.
                var options = {
                    hostname: hostname,
                    port: 8000,
                    path: '',
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Content-Length': data.length
                    }
                }

                // Makes the https request to update the robot.
                var req = https.request(options, res => {
                    console.log("Here " + res);
                    console.log(res.statusCode);
                  
                    res.on('data', d => {
                      process.stdout.write(d)
                    });
                });

                // Error log.
                req.on('error', error => {
                    console.error(error)
                });

                // Write data.
                req.write(data);
                req.end();
            })
            .catch(err => {
                console.log(err);
            });
        }
    }
);