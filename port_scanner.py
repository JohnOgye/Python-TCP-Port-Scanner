import socket
import time
from datetime import datetime


DEFAULT_TIMEOUT = 0.5
RESULTS_FILE = "scan_results.txt"
SEPARATOR_WIDTH = 50


def resolve_target(target):
    """Resolve a hostname or IPv4 address."""
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        return None


def get_port_range():
    """Prompt the user until a valid TCP port range is entered."""
    while True:
        try:
            start = int(input("Enter starting port (1-65535): "))
            end = int(input("Enter ending port (1-65535): "))

            if not 1 <= start <= 65535 or not 1 <= end <= 65535:
                print("Error: Ports must be between 1 and 65535.")
                continue

            if start > end:
                print(
                    "Error: Starting port must not exceed ending port."
                )
                continue

            return start, end

        except ValueError:
            print("Error: Please enter valid numeric port values.")


def get_service_name(port):
    """Return the standard TCP service name associated with a port."""
    try:
        return socket.getservbyport(port, "tcp")
    except OSError:
        return "Unknown"


def scan_port(target_ip, port, timeout=DEFAULT_TIMEOUT):
    """Check whether a TCP port accepts a connection."""
    try:
        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as sock:
            sock.settimeout(timeout)

            result = sock.connect_ex((target_ip, port))

            if result == 0:
                service = get_service_name(port)
                return True, service

    except OSError:
        return False, None

    return False, None


def save_results(
    filename,
    target,
    target_ip,
    start_port,
    end_port,
    open_ports,
    duration
):
    """Save scan results to a text report."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write("PYTHON TCP PORT SCANNER\n")
        file.write("=" * SEPARATOR_WIDTH + "\n")

        file.write(
            f"Scan date: "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        )

        file.write(f"Target: {target}\n")
        file.write(f"Resolved IPv4 address: {target_ip}\n")
        file.write(
            f"Port range: {start_port}-{end_port}\n"
        )
        file.write(
            f"Scan duration: {duration:.2f} seconds\n"
        )
        file.write(
            f"Open ports found: {len(open_ports)}\n"
        )

        file.write("=" * SEPARATOR_WIDTH + "\n\n")

        if open_ports:
            file.write("OPEN PORTS\n")
            file.write("-" * SEPARATOR_WIDTH + "\n")

            for port, service in open_ports:
                file.write(
                    f"Port {port:<6} "
                    f"Service name: {service}\n"
                )
        else:
            file.write(
                "No open TCP ports were found.\n"
            )


def main():
    """Run the TCP port scanner."""
    print("=" * SEPARATOR_WIDTH)
    print(" PYTHON TCP PORT SCANNER")
    print("=" * SEPARATOR_WIDTH)

    target = input(
        "Enter IPv4 address or hostname: "
    ).strip()

    if not target:
        print("Error: Target cannot be empty.")
        return

    target_ip = resolve_target(target)

    if target_ip is None:
        print("Error: Could not resolve the target.")
        return

    start_port, end_port = get_port_range()

    print("\n" + "-" * SEPARATOR_WIDTH)
    print(f"Target: {target}")
    print(f"Resolved IPv4 address: {target_ip}")
    print(
        f"Scanning TCP ports "
        f"{start_port}-{end_port}..."
    )
    print("-" * SEPARATOR_WIDTH)

    start_time = time.perf_counter()
    open_ports = []

    try:
        for port in range(
            start_port,
            end_port + 1
        ):
            is_open, service = scan_port(
                target_ip,
                port
            )

            if is_open:
                open_ports.append(
                    (port, service)
                )

                print(
                    f"[OPEN] Port {port:<6} "
                    f"Service name: {service}"
                )

    except KeyboardInterrupt:
        print("\nScan interrupted by user.")
        return

    duration = time.perf_counter() - start_time

    print("\n" + "=" * SEPARATOR_WIDTH)
    print("SCAN COMPLETE")
    print("=" * SEPARATOR_WIDTH)

    print(f"Target: {target}")
    print(
        f"Ports scanned: "
        f"{start_port}-{end_port}"
    )
    print(
        f"Open ports found: "
        f"{len(open_ports)}"
    )
    print(
        f"Scan duration: "
        f"{duration:.2f} seconds"
    )

    try:
        save_results(
            RESULTS_FILE,
            target,
            target_ip,
            start_port,
            end_port,
            open_ports,
            duration
        )

        print(
            f"Results saved to: "
            f"{RESULTS_FILE}"
        )

    except OSError as error:
        print(
            f"Warning: Could not save results: "
            f"{error}"
        )


if __name__ == "__main__":
    main()