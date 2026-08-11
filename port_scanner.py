import socket
import time
from datetime import datetime


def resolve_target(target):
    """Resolve a hostname or IP address."""
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        return None


def get_port_range():
    """Ask the user for a valid port range."""
    while True:
        try:
            start = int(input("Enter starting port (1-65535): "))
            end = int(input("Enter ending port (1-65535): "))

            if not 1 <= start <= 65535 or not 1 <= end <= 65535:
                print("Error: Ports must be between 1 and 65535.")
                continue

            if start > end:
                print("Error: Starting port must not exceed ending port.")
                continue

            return start, end

        except ValueError:
            print("Error: Please enter valid numbers.")


def scan_port(target_ip, port, timeout=0.5):
    """Check whether a TCP port is open and identify its service."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)

            if sock.connect_ex((target_ip, port)) == 0:
                try:
                    service = socket.getservbyport(port, "tcp")
                except OSError:
                    service = "Unknown"

                return True, service

    except socket.error:
        pass

    return False, None


def save_results(filename, target, target_ip, start, end, open_ports, duration):
    """Save scan results to a text file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write("PYTHON TCP PORT SCANNER\n")
        file.write("=" * 50 + "\n")
        file.write(f"Scan date: {datetime.now()}\n")
        file.write(f"Target: {target}\n")
        file.write(f"Resolved IP: {target_ip}\n")
        file.write(f"Port range: {start}-{end}\n")
        file.write(f"Scan duration: {duration:.2f} seconds\n")
        file.write(f"Open ports: {len(open_ports)}\n")
        file.write("=" * 50 + "\n\n")

        if open_ports:
            file.write("OPEN PORTS\n")
            file.write("-" * 50 + "\n")

            for port, service in open_ports:
                file.write(f"Port {port:<6} Service: {service}\n")
        else:
            file.write("No open TCP ports were found.\n")


def main():
    print("=" * 50)
    print("          PYTHON TCP PORT SCANNER")
    print("=" * 50)

    target = input("Enter IP address or hostname: ").strip()

    if not target:
        print("Error: Target cannot be empty.")
        return

    target_ip = resolve_target(target)

    if target_ip is None:
        print("Error: Could not resolve the target.")
        return

    start_port, end_port = get_port_range()

    print("\n" + "-" * 50)
    print(f"Target: {target}")
    print(f"IP address: {target_ip}")
    print(f"Scanning TCP ports {start_port}-{end_port}...")
    print("-" * 50)

    start_time = time.time()
    open_ports = []

    for port in range(start_port, end_port + 1):
        is_open, service = scan_port(target_ip, port)

        if is_open:
            open_ports.append((port, service))
            print(f"[OPEN] Port {port:<6} Service: {service}")

    duration = time.time() - start_time

    print("\n" + "=" * 50)
    print("SCAN COMPLETE")
    print("=" * 50)
    print(f"Target: {target}")
    print(f"Ports scanned: {start_port}-{end_port}")
    print(f"Open ports found: {len(open_ports)}")
    print(f"Scan duration: {duration:.2f} seconds")

    filename = "scan_results.txt"

    try:
        save_results(
            filename,
            target,
            target_ip,
            start_port,
            end_port,
            open_ports,
            duration
        )
        print(f"Results saved to: {filename}")

    except OSError as error:
        print(f"Warning: Could not save results: {error}")


if __name__ == "__main__":
    main()
