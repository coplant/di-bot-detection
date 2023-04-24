import {getScreenHeight, getScreenWidth} from "./screen.js";
import {BotType, Browser} from "./browserInfo.js";

export function getUserAgent() {
    return navigator.userAgent;
}

export function getBotTypeByUserAgent() {
    let userAgent = getUserAgent();
    if (!userAgent) {
        return Browser.NO_USERAGENT;
    }
    if (/PhantomJS/i.test(userAgent)) {
        return BotType.PHANTOMJS;
    }
    if (/Headless/i.test(userAgent)) {
        return BotType.HEADLESS;
    }
    if (/Electron/i.test(userAgent)) {
        return BotType.ELECTRON;
    }
    if (/slimerjs/i.test(userAgent)) {
        return BotType.SLIMER_JS;
    }
    if (/CefSharp/i.test(userAgent)) {
        return BotType.CEFSHARP;
    }
    if (/CEF/i.test(userAgent)) {
        return BotType.CEF;
    }
    if (/Awesomium/i.test(userAgent)) {
        return BotType.AWESOMIUM;
    }
    if (/Rhino/i.test(userAgent)) {
        return BotType.RHINO;
    }
    if (/WebdriverIO/i.test(userAgent)) {
        return BotType.WEBDRIVER_IO;
    }
    return false;
}

export function getBrowser() {
    const userAgent = getUserAgent();
    if (!userAgent) {
        return Browser.NO_USERAGENT;
    }
    let browser = "unknown";
    let version = "unknown";

    const match = (regex) => userAgent.match(regex);
    const test = (regex) => regex.test(userAgent);

    if (test(/ucbrowser/i)) {
        browser = Browser.UC;
        version = `${getBrowserVersion(match(/(ucbrowser)\/([\d\.]+)/i))}`;
    } else if (test(/edg/i)) {
        browser = Browser.EDGE;
        version = `${getBrowserVersion(match(/(edge|edga|edgios|edg)\/([\d\.]+)/i))}`;
    } else if (test(/googlebot/i)) {
        browser = Browser.GOOGLEBOT;
        version = `${getBrowserVersion(match(/(googlebot)\/([\d\.]+)/i))}`;
    } else if (test(/chromium/i)) {
        browser = Browser.CHROMIUM;
        version = `${getBrowserVersion(match(/(chromium)\/([\d\.]+)/i))}`;
    } else if (test(/firefox|fxios/i) && !test(/seamonkey/i)) {
        browser = Browser.FIREFOX;
        version = `${getBrowserVersion(match(/(firefox|fxios)\/([\d\.]+)/i))}`;
    } else if (test(/; msie|trident/i) && !test(/ucbrowser/i)) {
        const ie_version = getBrowserVersion(match(/(trident)\/([\d\.]+)/i));
        browser = Browser.IE;
        version = ie_version ? `${parseFloat(ie_version) + 4.0}` : "7.0";
    } else if (test(/chrome|crios/i) && !test(/opr|opera|chromium|edg|ucbrowser|googlebot/i)) {
        browser = Browser.CHROME;
        version = `${getBrowserVersion(match(/(chrome|crios)\/([\d\.]+)/i))}`;
    } else if (test(/safari/i) && !test(/chromium|edg|ucbrowser|chrome|crios|opr|opera|fxios|firefox/i)) {
        browser = Browser.SAFARI;
        version = `${getBrowserVersion(match(/(safari)\/([\d\.]+)/i))}`;
    } else if (test(/opr|opera/i)) {
        browser = Browser.OPERA;
        version = `${getBrowserVersion(match(/(opera|opr)\/([\d\.]+)/i))}`;
    }
    return [browser, version];
}

function getBrowserVersion(match) {
    return match ? match[2] : "0.0.0.0";
}


export function isMobileDevice(userAgent) {
    let width = getScreenWidth();
    let height = getScreenHeight();
    if (userAgent.includes("mobi") || userAgent.includes("tablet")) {
        return true;
    }
    if (userAgent.includes("android")) {
        if (height > width && width < 800) {
            return true;
        }
        if (width > height && height < 800) {
            return true;
        }
    }
    return false;
}