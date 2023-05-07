export let config = {
    connection: {
        protocol: "http",
        host: "localhost",
        port: 8888,
        path: "api",
        method: "POST"
    },
    collect: {
        browser: true,
        timezone: true,
        fonts: true,
        canvas: true,
        UA: true,
        screen: true,
        webRTC: true,
        webGL: true,
        language: true
    }
};