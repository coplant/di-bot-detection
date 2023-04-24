import {BotType} from "./browserInfo";

export function getWebGL() {
    const gl = document.createElement("canvas").getContext("webgl");
    return [gl.getParameter(gl.VERSION), gl.getParameter(gl.SHADING_LANGUAGE_VERSION),
        gl.getParameter(gl.VENDOR), gl.getParameter(gl.RENDERER)];
}

export function detectWebGL() {
    let webGL = getWebGL();
    if (webGL) {
        const vendor = webGL[2];
        const renderer = webGL[3];
        if (vendor === 'Brian Paul' && renderer === 'Mesa OffScreen') {
            return BotType.HEADLESS;
        }
    }
}
