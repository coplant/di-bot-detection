import {generalFonts} from "./fontList.js";

const fontCheck = new Set(generalFonts);


function checkAvailableFonts(font) {
    let baseFonts = ["monospace", "sans-serif", "serif"];
    let testString = "mmmmmmmmmmlli";
    let testSize = "72px";
    let body = document.getElementsByTagName("body")[0];
    let span = document.createElement("span");
    span.style.fontSize = testSize;
    span.innerHTML = testString;
    let defaultWidth = {};
    let defaultHeight = {};
    for (let index in baseFonts) {
        span.style.fontFamily = baseFonts[index];
        body.appendChild(span);
        defaultWidth[baseFonts[index]] = span.offsetWidth;
        defaultHeight[baseFonts[index]] = span.offsetHeight;
        body.removeChild(span);
    }

    function detect(font) {
        let detected = false;
        for (let index in baseFonts) {
            span.style.fontFamily = font + ',' + baseFonts[index];
            body.appendChild(span);
            let matched = (span.offsetWidth !== defaultWidth[baseFonts[index]] || span.offsetHeight !== defaultHeight[baseFonts[index]]);
            body.removeChild(span);
            detected = detected || matched;
        }
        return detected;
    }

    return detect(font);
}

export function getAvailableFonts() {
    const fontAvailable = new Set();
    for (const font of fontCheck.values()) {
        if (checkAvailableFonts(font)) {
            fontAvailable.add(font);
        }
    }
    return [...fontAvailable.values()];
}
