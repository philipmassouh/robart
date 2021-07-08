var view = null,
  connectButton = null,
  listenButton = null
  overlay = null,
  textArea = null,
  audio = null,
  audioChunks = [],
  playerDiv = null,
  hostname = null;

var mobileDevice = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
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

  } else { alert('getUserMedia not supported in this browser.'); }

  connectButton = document.getElementById('ConnectButton');
  listenButton = document.getElementById('ListenButton');
  textArea = document.getElementById('TextToSend');
  playerDiv = document.getElementById('playerDiv');
  overlay = document.getElementById('prompt');
  hostInput = document.getElementById('hostInput');
}

function show() {
  overlay.style.display = "block";
}

function hide() {
  overlay.style.display = "none";
}

function connect() {
  // This `streaming viewer` setups a broadcast streaming where the simulation is shown but it is not possible to control it.
  // For any other use, please refer to the documentation:
  // https://www.cyberbotics.com/doc/guide/web-simulation#how-to-embed-a-web-scene-in-your-website
  hostname = hostInput.value;
  //hide();

  if (hostname && hostname !='') {
    view = new webots.View(playerDiv, mobileDevice);
    view.broadcast = false;
    view.setTimeout(-1); // disable timeout that stops the simulation after a given time
    view.open('ws://' + hostname + ':1234', 'x3d');
    view.onquit = disconnect;
    connectButton.value = 'Disconnect';
    connectButton.onclick = disconnect;
  }
}

function disconnect() {
  view.close();
  view = null;
  playerDiv.innerHTML = null;
  connectButton.value = 'Connect';
  connectButton.onclick = show;
}

function send() {
  window.watson.wa(textArea.value, hostname);
  textArea.value = "";
}

/**
 * Terminates the server.
 * WARNING DOING THIS WILL REQUIRE A SERVER RESTART BY HOST.
 */
function restart_server() { window.watson.restart_server(hostname); }

function listen() {
  audio.start();
  window.watson.stt();
  listenButton.value = 'Stop';
  listenButton.onclick = stop;
}

function stop() {
  audio.stop();
  listenButton.value = 'Listen';
  listenButton.onclick = listen;
}

window.addEventListener('load', init, false);