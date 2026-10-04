const scanButton = document.getElementById("scanButton");
const networkInput = document.getElementById("networkInput");

const hostCount = document.getElementById("hostCount");
const portCount = document.getElementById("portCount");
const status = document.getElementById("status");

const hostList = document.getElementById("hostList");


scanButton.addEventListener("click", () => {

    const network = networkInput.value.trim();

    if (!network) {
        status.textContent = "ENTER NETWORK";
        return;
    }

    scanButton.disabled = true;
    status.textContent = "SCANNING...";

    hostList.innerHTML = `
        <div class="empty">
            Discovering hosts...
        </div>
    `;

    // Fake a little delay so it feels like a scan
    setTimeout(() => {

        const demoResults = [
            {
                ip: "192.168.0.1",
                status: "up",
                open_ports: [
                    {
                        port: 53,
                        state: "open",
                        service: "DNS",
                        latency_ms: 30.59
                    },
                    {
                        port: 80,
                        state: "open",
                        service: "HTTP",
                        latency_ms: 4.36
                    },
                    {
                        port: 443,
                        state: "open",
                        service: "HTTPS",
                        latency_ms: 30.29
                    }
                ]
            },
            {
                ip: "192.168.0.29",
                status: "up",
                open_ports: [
                    {
                        port: 445,
                        state: "open",
                        service: "SMB",
                        latency_ms: 12.41
                    }
                ]
            },
            {
                ip: "192.168.0.248",
                status: "up",
                open_ports: []
            }
        ];

        displayResults(demoResults);

        status.textContent = "COMPLETE";
        scanButton.disabled = false;

    }, 1200);
});


function displayResults(hosts) {

    hostCount.textContent = hosts.length;

    let totalPorts = 0;

    hostList.innerHTML = "";

    hosts.forEach(host => {

        const ports = host.open_ports || [];

        totalPorts += ports.length;

        const hostElement = document.createElement("div");

        hostElement.className = "host";

        let portHTML = "";

        if (ports.length === 0) {

            portHTML = `
                <div class="no-ports">
                    No open ports detected.
                </div>
            `;

        } else {

            portHTML = ports.map(port => `
                <div class="port">

                    <div class="port-main">

                        <span class="port-number">
                            ${port.port}/tcp
                        </span>

                        <span class="port-state">
                            ${port.state}
                        </span>

                        <span class="port-service">
                            ${port.service}
                        </span>

                    </div>

                    <div class="latency">
                        ${port.latency_ms} ms
                    </div>

                </div>
            `).join("");

        }

        hostElement.innerHTML = `

            <div class="host-header">

                <div>
                    <div class="host-ip">
                        ${host.ip}
                    </div>

                    <div class="host-status">
                        ${host.status}
                    </div>
                </div>

                <div class="port-count">
                    ${ports.length} open port${ports.length === 1 ? "" : "s"}
                </div>

            </div>

            <div class="port-list">
                ${portHTML}
            </div>

        `;

        hostList.appendChild(hostElement);
    });
    portCount.textContent = totalPorts;
}