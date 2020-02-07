// Query for the toggle that is used to change between themes
const toggle = document.querySelector("#toggle-darkmode");

// Listen for the toggle check/uncheck to toggle the dark class on the <body>
toggle.addEventListener("ionChange", ev => {
  document.body.classList.toggle("dark", ev.detail.checked);
});

const prefersDark = window.matchMedia("(prefers-color-scheme: dark)");

// Listen for changes to the prefers-color-scheme media query
prefersDark.addListener(e => checkToggle(e.matches));

// Called when the app loads
function loadApp() {
  checkToggle(prefersDark.matches);
}

// Called by the media query to check/uncheck the toggle
function checkToggle(shouldCheck) {
  toggle.checked = shouldCheck;
}

// alert IP
const changeIP = document.querySelector("#btn-ip");
const alertCtrl = document.querySelector("ion-alert-controller");

changeIP.addEventListener("click", presentIPPrompt);

function presentIPPrompt() {
  const alert = document.createElement("ion-alert");
  alert.header = "Enter IP";
  alert.inputs = [
    {
      name: "IP",
      id: "input-ip",
      type: "url"
    }
  ];
  alert.buttons = [
    {
      text: "Cancel",
      role: "cancel",
      color: "danger"
    },
    {
      text: "Ok",
      color: "primary",
      handler: () => {
        const ipInput = document.querySelector("#input-ip");
        ip = ipInput.value;
        localStorage.setItem("ip", ipInput.value);
        connectWebsocket();
      }
    }
  ];

  document.body.appendChild(alert);
  return alert.present();
}

let ip = localStorage.getItem("ip");
let ws;
document.addEventListener("DOMContentLoaded", connectWebsocket);

function connectWebsocket() {
  try {
    let ip = localStorage.getItem("ip");
    if(ip.trim().length<7){
      presentIPPrompt();
    }else{
      ip = localStorage.getItem("ip");
      ws = new WebSocket("ws://" + ip + ":6789");
    }
  } catch (e) {
    console.log(e);
  } finally {
    console.log(ws.readyState);
  }
}

// preview
const redRange = document.querySelector("#input-red");
const greenRange = document.querySelector("#input-green");
const blueRange = document.querySelector("#input-blue");
const brightnessRange = document.querySelector("#input-brightness");
const previewCanvas = document.querySelector("#canvas-preview");

redRange.addEventListener("ionChange", changePreview);
greenRange.addEventListener("ionChange", changePreview);
blueRange.addEventListener("ionChange", changePreview);
brightnessRange.addEventListener("ionChange", changePreview);

document.addEventListener("DOMContentLoaded", changePreview);

function getManualColor() {
  const rgb = [
    Math.floor(redRange.value * brightnessRange.value),
    Math.floor(greenRange.value * brightnessRange.value),
    Math.floor(blueRange.value * brightnessRange.value)
  ];
  return rgbToHex(rgb);
}

function changePreview() {
  previewCanvas.style.background = getManualColor();
}

function rgbToHex(rgb) {
  let ret = "#";
  for (let i = 0; i < 3; i++) {
    let hex = Number(rgb[i]).toString(16);
    if (hex.length < 2) {
      hex = "0" + hex;
    }
    ret += hex;
  }
  return ret;
}

// addFav, send static color
const addFavBtn = document.querySelector("#btn-addfav");
const applyBtn = document.querySelector("#btn-apply");
const favList = document.querySelector("#list-fav");

addFavBtn.addEventListener("click", addFav);
applyBtn.addEventListener("click", applyPreview);
previewCanvas.addEventListener("click", applyPreview);

function addFav(){
  const item = document.createElement("ion-item");
  item.textContent = getManualColor();
  item.button = true;
  item.addEventListener("click",() =>{
    sendStaticColor(item.textContent);
  });

  favList.appendChild(item);
  console.log(item);
}

function applyPreview() {
  sendStaticColor(getManualColor());
}

function sendStaticColor(color) {
  ws.send(
    JSON.stringify({
      name: "bed",
      type: "static",
      color: getManualColor().substring(1, 7)
    })
  );
}

// animation

const randomBtn = document.querySelector("#btn-random");
const breathBtn = document.querySelector("#btn-breath");
const circleBtn = document.querySelector("#btn-circle");
const rndBreathBtn = document.querySelector("#btn-rndbreath");
const circleBreathBtn = document.querySelector("#btn-circlebreath");
const stopBtn = document.querySelector("#btn-stop");
const speedInput = document.querySelector("#input-speed");

randomBtn.addEventListener("click",() =>{sendAnimation("random");});
breathBtn.addEventListener("click",() =>{sendAnimation("breathing");});
circleBtn.addEventListener("click",() =>{sendAnimation("colorcircle");});
rndBreathBtn.addEventListener("click",() =>{sendAnimation("randombreathing");});
circleBreathBtn.addEventListener("click",() =>{sendAnimation("colorcirclebreathing");});
stopBtn.addEventListener("click",() =>{sendAnimation("stop");});

function sendAnimation(animationType){
	const speed = speedInput.value;
	const led = "bed" //document.getElementById("selectLed").value;
	ws.send(JSON.stringify({"name":led,
							"type":"animation",
							"animationType":animationType,
							"animationSpeed":speed}));
}
