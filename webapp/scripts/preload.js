const fs = require('fs')
const { contextBridge } = require("electron");
const { IamAuthenticator } = require('ibm-watson/auth');
const AssistantV2 = require('ibm-watson/assistant/v2');
const SpeechToTextV1 = require('ibm-watson/speech-to-text/v1');

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
var recognizeStream = speechToText.recognizeUsingWebSocket(params);

// Listen for events.
recognizeStream.on('data', function(event) { onEvent('data', event); });
recognizeStream.on('error', function(event) { onEvent('Error:', event); });
recognizeStream.on('close', function(event) { onEvent('Close:', event); });

// Display events on the console.
function onEvent(name, event) {
    if (name == "data") {
        var text = document.getElementById("TextToSend");
        if (text) {
            text.value = event.results[0].alternatives[0].transcript
        }
    }
};

//Creates session.
assistant.createSession({
    assistantId: 'b5428c83-d98e-46e5-ad29-8db5cd50ea16'
  })
    .then(res => {
      console.log(JSON.stringify(res.result, null, 2));
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
        wa: (text) => {

        }
    }
);