var view = null,
  connectButton = null,
  listenButton = null
  overlay = null,
  textArea = null,
  audio = null,
  audioChunks = [],
  playerDiv = null,
  hostname = null,
  mobileDevice = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

  
if (mobileDevice) {
  let head = document.getElementsByTagName('head')[0];
  let jqueryTouch = document.createElement('script');
  jqueryTouch.setAttribute('type', 'text/javascript');
  jqueryTouch.setAttribute('src', 'https://www.cyberbotics.com/jquery-ui/1.11.4/jquery.ui.touch-punch.min.js');
  head.appendChild(jqueryTouch);

  var mobileCss = document.createElement('link');
  mobileCss.setAttribute('rel', 'stylesheet');
  mobileCss.setAttribute('type', 'text/css');
  mobileCss.setAttribute('href', 'https://www.cyberbotics.com/wwi/R2021a/wwi_mobile.css');
  head.appendChild(mobileCss);
}

/**
 * Initializes all of the variables.
 */

function init() {
  // TODO: Ensure that user media is set up for the right browser + older browser support.
  if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({audio:true})
    .then((stream) => {
      audio = new MediaRecorder(stream);

      audio.ondataavailable = function(e) {
        audioChunks.push(e.data);

        if (audio.state == 'inactive') {
          var blob = new Blob(audioChunks, { type: e.data.type });
          blob.arrayBuffer()
          .then((results) => {
            window.watson.stt(new Uint8Array(results));
          });
          
          audioChunks = []
        }
      }
    })
    .catch((error) => {
      alert('Error capturing audio. ' + error);
    });

    // Sets up authentication.
    fetch("../restAuth.json")
    .then(response => {
      response.json()
      .then(auth => {
        // Sets the host input to a default IP.
        if(auth.server.local == 'Null') {
          hostInput.value = auth.server.ipv4
        } else {
          hostInput.value = auth.server.local
        }
      });
    }).catch(e => {
      console.log(e)
    });
  } else { alert('getUserMedia not supported in this browser.'); }

  connectButton = document.getElementById('ConnectButton');
  listenButton = document.getElementById('ListenButton');
  textArea = document.getElementById('TextToSend');
  playerDiv = document.getElementById('playerDiv');
  overlay = document.getElementById('prompt');
  hostInput = document.getElementById('hostInput');
//TODO set page default based on os
  const colorButtons = document.querySelectorAll(".btn__color")
  colorButtons.forEach(btn => {
    btn.addEventListener("click", (event) => {
      if (btn.value == "light_mode") {
        btn.value = "dark_mode";
        document.documentElement.className = "dark"
      } else if (btn.value == "dark_mode") {
        btn.value = "light_mode"
        document.documentElement.className = "light"
      }
    });
  });

  document.querySelector("#connectButton").addEventListener("click", connect)
}

/**
 * Connects to Webots and the server.
 */

//TODO toggle_on is the slider right and toggle_off is the slider left.
function connect() {
  hostname = hostInput.value;

  if (hostname && hostname !='') {
    view = new webots.View(playerDiv, mobileDevice);
    view.broadcast = false;
    view.setTimeout(-1); // disable timeout that stops the simulation after a given time
    view.open('ws://' + hostname + ':1234', 'x3d');
    view.onquit = disconnect;
    connectButton.value = 'toggle_on';
    connectButton.onclick = disconnect;
  }
}

/**
 * Disconnects from Webots and the server.
 */
function disconnect() {
  view.close();
  view = null;
  playerDiv.innerHTML = null;
  connectButton.value = 'toggle_off';
  connectButton.onclick = show;
  hostname = '';
}

/**
 * Sends the text to Watson.
 */
function send() {
  window.watson.wa(textArea.value, hostname);
  textArea.value = "";
}

/**
 * Starts listening.
 */
function start_listening() {
  audio.start();
  window.watson.stt();
  listenButton.value = 'Stop';
  listenButton.onclick = stop_listening;
}

/**
 * Stops listening.
 */
function stop_listening() {
  audio.stop();
  listenButton.value = 'Listen';
  listenButton.onclick = start_listening;
}

// Launches mic on window load.
window.addEventListener('load', init, false);