import json
from discovery import discover_hosts
from scanner import scan_host

PORTS = [
    21,
    22,
    23,
    25,
    53,
    80,
    110,
    139,
    143,
    443,
    445,
    3389,
    8080
]

def scan_network(network):
    print("\n" + "=" * 50)
    print("PINKRECON NETWORK SCAN")
    print("=" *50)

    hosts = discover_hosts(network)

    print(f"\nDiscovered {len(hosts)} host(s).")

    results = []

    for host in hosts:
        ip = host["ip"]

        print("\n" + "-" * 50)
        print(f"Scanning host: {ip}")
        print("-" * 50)

        open_ports = scan_host(ip, PORTS)

        results.append({
            "ip": ip,
            "mac": host.get("mac", "Unknown"),
            "status": host.get("status", "up"),
            "open_ports": open_ports
        })

    return results

if __name__ == "__main__":
    network = input(
        "\nNetwork: "
    )

    results = scan_network(network)

    with open(
        "network_scan_results.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(results, file, indent=4)

    print("\n" + "=" * 50)
    print("NETWORK SCAN COMPLETE")
    print("=" * 50)

    print(f"Hosts discovered: {len(results)}")
    print("Results saved to network_scan_results.json")