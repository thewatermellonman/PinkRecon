import socket
import time


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

    print(f"\nScanning {target}...")

    for port in ports:
        result = scan_port(target, port)

        if result["state"] == "open":
            print(
                f"[+] {port}/tcp OPEN "
                f"({result['latency_ms']} ms)"
            )

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

    print("\nScan complete.")
    print(f"Open ports: {len(results)}")