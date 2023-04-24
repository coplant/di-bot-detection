export function getPluginData() {
    let length = navigator.plugins.length;
    let result = [];
    for (let i = 0; i < length; i++) {
        result.push(navigator.plugins[i].name);
    }
    return result;
}

