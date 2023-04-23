import {Browser} from "./browserInfo.js";

export function detectBrowserDuckTyping() {
    let browser;
    if (!isNaN(screen.logicalXDPI) && !isNaN(screen.systemXDPI)) {
        browser = Browser.IE;
    }
    else if (window.navigator.msMaxTouchPoints) {
        browser = Browser.IE;
    }
    else if (!!window.chrome && !(!!window.opera || navigator.userAgent.indexOf(' Opera') >= 0)) {
        browser = Browser.CHROME;
    }
    else if (Object.prototype.toString.call(window.HTMLElement).indexOf('Constructor') > 0) {
        browser = Browser.SAFARI;
    }
    else if ('orientation' in window && 'webkitRequestAnimationFrame' in window) {
        browser = Browser.WEBKIT_MOBILE;
    }
    else if ('webkitRequestAnimationFrame' in window) {
        browser = Browser.WEBKIT;
    }
    else if (navigator.userAgent.indexOf('Opera') >= 0) {
        browser = Browser.OPERA;
    }
    else if (window.devicePixelRatio) {
        browser = Browser.FIREFOX;
    }
    return browser.description;
}