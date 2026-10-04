const canvas = document.getElementById("matrix");
const ctx = canvas.getContext("2d");

function drawMatrix() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    ctx.font = "16px monospace";

    const columnWidth = 18;
    const rowHeight = 18;

    const columns = Math.floor(canvas.width / columnWidth);
    const rows = Math.floor(canvas.height / rowHeight);

    for (let column = 0; column < columns; column++) {

        const startRow = Math.floor(Math.random() * 8);

        const streamLength =
            Math.floor(Math.random() * 15) + 8;

        for (
            let row = startRow;
            row < Math.min(startRow + streamLength, rows);
            row++
        ) {

            if (Math.random() > 0.8) {
                continue;
            }

            const character = Math.random() > 0.5 ? "0" : "1";

            const x = column * columnWidth;
            const y = row * rowHeight;

            const position =
                (row - startRow) / streamLength;

            const opacity =
                0.55 - position * 0.35;

            ctx.fillStyle =
                `rgba(255, 105, 180, ${opacity})`;

            ctx.fillText(character, x, y);
        }
    }
}

drawMatrix();

window.addEventListener("resize", drawMatrix);

const scanButton = document.getElementById("scanButton");
const networkInput = document.getElementById("networkInput");

const hostCount = document.getElementById("hostCount");
const portCount = document.getElementById("portCount");
const status = document.getElementById("status");

const hostList = document.getElementById("hostList");

console.log("scanButton:", scanButton);
console.log("networkInput:", networkInput);
console.log("hostCount:", hostCount);
console.log("portCount:", portCount);
console.log("status:", status);
console.log("hostList:", hostList);


scanButton.addEventListener("click", async () => {

    const network = networkInput.value.trim();

    if (!network) {
        status.textContent = "ENTER NETWORK";
        return;
    }

    status.textContent = "SCANNING...";
    scanButton.disabled = true;

    hostList.innerHTML = `
        <div class="empty">
            Scanning ${network}...
        </div>
    `;

    try {

        const response = await fetch("/scan", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                network: network
            })
        });

        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error);
        }

        displayResults(data.hosts);

        status.textContent = "COMPLETE";

    } catch (error) {

        console.error(error);

        status.textContent = "ERROR";

        hostList.innerHTML = `
            <div class="empty">
                ${error.message}
            </div>
        `;

    } finally {

        scanButton.disabled = false;

    }
});

function displayResults(hosts) {

    hostCount.textContent = hosts.length;

    let totalPorts = 0;

    hostList.innerHTML = "";

    if (hosts.length === 0) {

        hostList.innerHTML = `
            <div class="empty">
                No hosts discovered.
            </div>
        `;

        portCount.textContent = "0";

        return;
    }

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
                            ${port.service || "Unknown"}
                        </span>
                    </div>

                    ${
                        port.banner
                        ? `<div class="banner">
                            ${port.banner}
                        </div>`
                        : ""
                    }

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
                    ${ports.length}
                    open port${ports.length === 1 ? "" : "s"}
                </div>

            </div>

            <div class="port-list">
                ${portHTML}
            </div>

        `;

        hostList.appendChild(hostElement);
    });

    portCount.textContent = String(totalPorts);
}