import socket
import time
import json

from services import identify_service, grab_banner


def scan_port(target, port, timeout=0.5):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    start = time.time()

    try:
        result = sock.connect_ex((target, port))
        elapsed = round((time.time() - start) * 1000, 2)

        if result == 0:
            return {
                "port": port,
                "state": "open",
                "latency_ms": elapsed
            }

        return {
            "port": port,
            "state": "closed",
            "latency_ms": elapsed
        }

    except socket.timeout:
        return {
            "port": port,
            "state": "filtered"
        }

    except Exception as error:
        return {
            "port": port,
            "state": "error",
            "error": str(error)
        }

    finally:
        sock.close()


def scan_host(target, ports):
    results = []

    print(f"\nScanning {target}...\n")

    for port in ports:
        result = scan_port(target, port)

        if result["state"] == "open":
            service = identify_service(port)
            banner = grab_banner(target, port)

            result["service"] = service
            result["banner"] = banner

            print(
                f"[+] {port}/tcp OPEN "
                f"| Service: {service} "
                f"| {result['latency_ms']} ms"
            )

            if banner:
                print(f"    Banner: {banner}")

            results.append(result)

    return results


if __name__ == "__main__":
    target = input("Target IP: ")

    ports = [
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

    results = scan_host(target, ports)

    with open("scan_results.json", "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4)

    print("\nScan complete.")
    print(f"Open ports: {len(results)}")
    print("Results saved to scan_results.json")