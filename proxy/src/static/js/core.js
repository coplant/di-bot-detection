"use strict";
import * as fingerprints from "./lib/imports.js"
import {config} from "./lib/config.js";

let c = config.connection
const url = `${c.protocol}://${c.host}${c.port ? ":" + c.port : ""}/${c.path}`

async function collectRTC() {
    return await fingerprints.webRTC.getIPs().then(ip => {
        return ip;
    });
}

async function collectData() {
    let data = {};
    if (config.collect.browser) {
        data.browser = {
            duck: fingerprints.duckTyping.detectBrowserDuckTyping(),
            eval: fingerprints.eval.getEvalLength(),
            driver: fingerprints.webDriver.getWebDriver(),
            plugin: fingerprints.plugins.getPluginData(),
            webgl: fingerprints.webGL.getWebGL(),
            bot: fingerprints.userAgent.getBotTypeByUserAgent(),
            ua: fingerprints.userAgent.getBrowser()
        };
    }
    if (config.collect.timezone) {
        data.timezone = {
            timezone: fingerprints.timeZone.getTimeZone(), offset: fingerprints.timeZone.getTimeOffset()
        };
    }
    if (config.collect.fonts) {
        let fonts = fingerprints.fonts.getAvailableFonts();
        data.fonts = {
            font_list: fonts, size: fonts.length
        };
    }
    if (config.collect.canvas) {
        data.canvas = {
            hash: fingerprints.sha256(fingerprints.canvas.getCanvasValue)
        };
    }
    if (config.collect.UA) {
        data.UA = {
            value: fingerprints.userAgent.getUserAgent(), mobile: fingerprints.userAgent.isMobileDevice()
        };
    }
    if (config.collect.screen) {
        data.screen = {
            height: fingerprints.screen.getScreenHeight(),
            width: fingerprints.screen.getScreenWidth(),
            inner_height: fingerprints.screen.getWindowInnerHeight(),
            inner_width: fingerprints.screen.getWindowInnerWidth(),
            outer_height: fingerprints.screen.getWindowOuterHeight(),
            outer_width: fingerprints.screen.getWindowOuterWidth()
        };
    }
    if (config.collect.webRTC) {
        let rtc_value = await collectRTC();
        data.webRTC = {
            value: rtc_value
        };
    }
    if (config.collect.webGL) {
        data.webGL = {
            headless: fingerprints.webGL.detectWebGL(), value: fingerprints.webGL.getWebGL()
        };
    }
    if (config.collect.language) {
        data.language = {
            value: fingerprints.language.getLanguage()
        };
    }
    return data
}


let fp = await collectData();
fetch(url, {
    method: config.connection.method, headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(fp),
    redirect: 'follow',
})
    .then(res => {
        if (res.redirected) {
            window.location.href = res.url;
        } else {
            return res.text();
        }
    })
    .then(data => {
        document.getElementById("response").innerHTML = data;
    })
    .catch(error => {
    });
