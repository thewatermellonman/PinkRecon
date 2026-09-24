COMMON_SERVICES = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    139: "NetBIOS",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3389: "RDP",
    8080: "HTTP-Proxy"
}

def identify_service(port):
    return COMMON_SERVICES.get(port, "Unknown")

def grab_banner(target, port, timeout=2):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        sock.connect((target, port))

        if port in (80, 8080):
            request = (
                "HEAD / HTTP/1.1\r\n"
                f"Host: {target}\r\n"
                "Connection: close\r\n"
                "\r\n"                
            )

            sock.sendall(request.encode())

        data = sock.recv(1024)
        sock.close()

        if not data:
            return None

        banner = data.decode("utf-8", errors="replace")

        banner = banner.replace("\r", " ").replace("\n", " ").strip()

        return banner [:300]

    except Exception:
        return None