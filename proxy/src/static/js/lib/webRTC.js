export function getIPs() {
    return new Promise((resolve, reject) => {
        let ip_dups = {};
        let RTCPeerConnection = window.RTCPeerConnection || window.mozRTCPeerConnection || window.webkitRTCPeerConnection;
        let useWebKit = !!window.webkitRTCPeerConnection;
        if (!RTCPeerConnection) {
            let win = iframe.contentWindow;
            RTCPeerConnection = win.RTCPeerConnection || win.mozRTCPeerConnection || win.webkitRTCPeerConnection;
            useWebKit = !!win.webkitRTCPeerConnection;
        }
        let mediaConstraints = {
            optional: [{RtpDataChannels: true}]
        };

        let servers = {iceServers: [{urls: "stun:stun.l.google.com:19302"}]};

        let pc = new RTCPeerConnection(servers, mediaConstraints);

        function handleCandidate(candidate) {
            try {
                let ip_regex = /([0-9]{1,3}(\.[0-9]{1,3}){3}|[a-f0-9]{1,4}(:[a-f0-9]{1,4}){7})/
                let ip_addr = ip_regex.exec(candidate).at(1);
                if (ip_dups[ip_addr] === undefined)
                    resolve(ip_addr);
                ip_dups[ip_addr] = true;
            } catch (e) {
            }
        }

        pc.onicecandidate = function (ice) {
            if (ice.candidate)
                handleCandidate(ice.candidate.candidate);
        };

        pc.createDataChannel("");
        pc.createOffer(function (result) {
            pc.setLocalDescription(result, function () {
            }, function () {
            });
        }, function () {
        });

        setTimeout(function () {
            let lines = pc.localDescription.sdp.split('\n');
            lines.forEach(function (line) {
                if (line.indexOf('a=candidate:') === 0)
                    handleCandidate(line);
            });
        }, 1000);
    });
}