import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_host(ip, timeout=0.5):

    common_ports = [80, 443, 445, 22]

    for port in common_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        try:
            result = sock.connect_ex((str(ip), port))

            if result == 0:
                return {
                    "ip": str(ip),
                    "status": "up"
                }

        except Exception:
            pass

        finally:
            sock.close()

    return {
        "ip": str(ip),
        "status": "down"
    }

def discover_hosts(network):
    network = ipaddress.ip_network(network, strict=False)

    hosts = list(network.hosts())
    discovered = []

    print(f"\nDiscovering hosts on {network}...")
    print(f"Checking {len(hosts)} addresses...\n")

    with ThreadPoolExecutor(max_workers=50) as excecutor:

        futures = {
            excecutor.submit(check_host, ip): ip
            for ip in hosts
        }

        for future in as_completed(futures):
            result = future.result()

            if result["status"] == "up":
                discovered.append(result)

                print(
                    f"[+] {result['ip']} ONLINE"
                )
    discovered.sort(
        key=lambda host: ipaddress.ip_address(host["ip"])
    )

    return discovered


if __name__ == "__main__":
    import json
    
    network = input(
        "Network: "
    )

    hosts = discover_hosts(network)

    with open("discovered_hosts.json", "w", encoding="utf-8") as file:
        json.dump(hosts, file, indent=4)

    print("\nDiscovery complete.")
    print(f"Hosts found: {len(hosts)}")
    print("Results saved to discovered_hosts.json")