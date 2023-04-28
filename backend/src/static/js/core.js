"use strict";
import * as fingerprints from "./lib/imports.js"


// console.log(detectBrowserDuckTyping());
// console.log(getBrowser());
// console.log(document.referrer);
// console.log(getPluginData());
// console.log(getEvalLength());
// let canvas = sha256(fingerprints.canvasValue);
let canvas = fingerprints.sha256(fingerprints.canvas.getCanvasValue);
console.log(canvas)
//Test: Print the IP addresses into the console

// getIPs(function (ip) {
//     console.log(ip);
// });


// console.log(getTimeOffset());
// console.log(getTimeZone());


/*
// log to server
const url = 'http://127.0.0.1:8000/';
const data = {
    username: 'myuser',
    password: 'mypassword'
};

fetch(url, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
})
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error(error);
    });



 */