

var view = null,
  listenButton = null
  sendButton = null,
  overlay = null,
  textArea = null,
  audio = null,
  audioChunks = [],
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

  listenButton = document.getElementById('ListenButton');
  sendButton = document.getElementById('SendButton');
  textArea = document.getElementById('TextToSend');
  overlay = document.getElementById('prompt');
  hostInput = document.getElementById('hostInput');








  /**
   * Sidebar buttons functionality here
   */
  const playerDiv = document.getElementById('playerDiv');
  const inventoryDiv = document.getElementById('inventoryDiv');
  const helpDiv = document.getElementById('helpDiv');

  document.querySelector("#robart").addEventListener("click", () => {
    playerDiv.style.display = "block"
    inventoryDiv.style.display = "none"
    helpDiv.style.display = "none"
  });

  document.querySelector("#inventory").addEventListener("click", () => {
    playerDiv.style.display = "none"
    inventoryDiv.style.display = "block"
    helpDiv.style.display = "none"
  });

  document.querySelector("#help").addEventListener("click", () => {
    playerDiv.style.display = "none"
    inventoryDiv.style.display = "none"
    helpDiv.style.display = "block"
  });

  //TODO close button not working
  document.querySelector("#closeButton").addEventListener("click", () => {
    var window = remote.getCurrentWindow();
    window.close();
  });




  /**
   * Interact window functionality here
   */

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

  //TODO add accessibility stuff

  document.querySelector("#connectButton").addEventListener("click", connect)

  //TODO mic functionality broken 
  listenButton.addEventListener("click", () => {
    if (listenButton.value = "mic") {
      audio.start();
      window.watson.stt();
      listenButton.value = 'mic_off';
    } else {
      audio.stop();
      listenButton.value = 'mic';
    }
  })

  document.addEventListener("keypress", (e) => {
    if (e.key == 'Enter') {
      send()
    }
  })

  sendButton.addEventListener("click", send);


  const suggestions = document.querySelector("#options").childNodes
    suggestions.forEach(suggestion =>
      suggestion.addEventListener("click", () => {
        textArea.value = `Watson please retrieve: ${suggestion.value}`
        send()
      }))
    

  // var table = document.createElement("table");
  // var columns = ["Item", "Count", "SKU"];
  // var tr = table.insertRow(-1);
  // for (var i = 0; i < columns.length; i++) {
  //   var th = document.createElement('th')
  //   th.innerHTML = columns[i]
  //   tr.appendChild(th)
  // }


  //TODO fresh call when the page is pulled up
  fetch("../server/server/database.json")
  .then(response => {
    response.json()
    .then(db => {
      var table = document.getElementById("database")
      for (var i = 1; i < table.rows.length; i++) {
        var row = table.rows[i]

        var item = row.cells[0].innerHTML

        var count = row.insertCell(-1)
        count.innerHTML = db.objects[item].count

        var description = row.insertCell(-1)
        description.innerHTML = db.objects[item].description

        var pos = row.insertCell(-1)
        pos.innerHTML = db.objects[item].entities[0].pos

        var sku = row.insertCell(-1)
        sku.innerHTML = db.objects[item].entities[0].sku
      }
    });
  }).catch(e => {
    console.log(e)
  });



}

/**
 * Connects to Webots and the server.
 */

function connect() {
  hostname = hostInput.value;

  if (hostname && hostname !='') {
    view = new webots.View(playerDiv, mobileDevice);
    view.broadcast = false;
    view.setTimeout(-1); // disable timeout that stops the simulation after a given time
    view.open('ws://' + hostname + ':1234', 'x3d');
    view.onquit = disconnect;
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
  connectButton.onclick = show;
  hostname = '';
}

/**
 * Sends the text to Watson.
 */
function send() {
  console.log(`SEND CALLED: ${textArea.value}`)
  window.watson.wa(textArea.value, hostname);
  textArea.value = "";
}




// Launches mic on window load.
window.addEventListener('load', init, false);