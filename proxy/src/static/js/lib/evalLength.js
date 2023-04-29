import {Browser} from "./browserInfo.js";

export function getEvalLength() {
    let length = eval.toString().length;
    if (length === 33) {
        return [Browser.CHROME.description];
    }
    if (length === 37) {
        return [Browser.FIREFOX.description, Browser.SAFARI.description];
    }
    if (length === 39) {
        return [Browser.IE.description];
    }
}
