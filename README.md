# Python TCP Port Scanner

A Python-based TCP port scanner developed as a cybersecurity learning project.

The tool scans a user-defined range of TCP ports, identifies open ports, attempts to determine their associated services, measures scan duration, and saves the results to a text report.

## Project Purpose

This project was created to develop practical understanding of:

- TCP/IP networking
- Network ports
- Socket programming
- Network reconnaissance
- Service identification
- Input validation
- Error handling
- Basic cybersecurity assessment

## Features

- IPv4 address scanning
- Hostname support
- Configurable TCP port ranges
- TCP connect scanning
- Open-port detection
- Basic service-name lookup using standard TCP port mappings
- Connection timeout handling
- Input validation
- Error handling
- Scan-duration measurement
- Automatic result reporting
- Results saved to `scan_results.txt`

## Technologies

- Python 3
- Socket programming
- TCP/IP networking
- Python standard library

No external packages are required.

## Project Structure

```text
Python-TCP-Port-Scanner/
│
├── .gitignore
├── LICENSE
├── README.md
└── port_scanner.py
```

## File Overview

- `port_scanner.py` — Main Python script containing the TCP port-scanning functionality.
- `README.md` — Project documentation, installation instructions, usage examples, and development notes.
- `.gitignore` — Prevents unnecessary files from being tracked by Git.
- `LICENSE` — MIT License for the project.

## Installation

```bash
git clone https://github.com/JohnOgye/Python-TCP-Port-Scanner.git
```
```bash
cd Python-TCP-Port-Scanner
```

## Usage

Run the program and enter an IP address or hostname.
Example:
Enter IP address or hostname: 127.0.0.1
Enter starting port (1-65535): 1
Enter ending port (1-65535): 1000
The scanner tests every TCP port in the selected range.
Example output (illustrative):
Target: 127.0.0.1
IP address: 127.0.0.1
Scanning TCP ports 1-1000...

[OPEN] Port 80     Service: http
[OPEN] Port 443    Service: https

==================================================
SCAN COMPLETE
==================================================
Target: 127.0.0.1
Ports scanned: 1-1000
Open ports found: 2
Scan duration: 2.31 seconds
Results saved to: scan_results.txt

1. Accepts an IPv4 address or hostname from the user.
2. Validates the target and requested port range.
3. Resolves hostnames to IPv4 addresses when necessary.
4. Attempts a TCP connection to each port in the selected range.
5. Identifies ports that accept TCP connections.
6. Looks up the standard service name associated with each open port.
7. Measures the total scan duration.
8. Saves the scan results to `scan_results.txt`.


## Security & Ethical Use

This project is intended for cybersecurity education, authorized security testing, and network administration.

Only scan systems and networks that you own or have explicit permission to test.

Unauthorized port scanning may violate organizational policies, terms of service, or applicable laws.

The author is not responsible for misuse of this tool.

## Limitations

- TCP connect scanning only
- IPv4 only
- Sequential port scanning
- Service names are based on standard port mappings and do not confirm the actual remote service
- No UDP scanning
- No operating system detection
- No vulnerability detection or exploitation
- Scan speed depends on the selected port range, network conditions, and timeout settings.

## Future Improvements

- Add concurrent scanning for improved performance
- Add command-line arguments
- Add configurable connection timeouts
- Add CSV and JSON result export
- Add scan progress indicators
- Add IPv6 support
- Improve service identification using banner grabbing
- Add UDP scanning
- Add unit tests.

## Development Progress

This project was developed incrementally as part of my cybersecurity learning journey.

### Phase 1 — Basic Port Scanner
- Implemented TCP socket connections
- Scanned ports 1–100
- Tested against localhost (`127.0.0.1`)

### Phase 2 — Scanner Improvements
- Added hostname support
- Added configurable port ranges
- Added input validation
- Added error handling
- Added service-name identification
- Added scan-duration measurement
- Added result-file generation

### Phase 3 — Local Testing
A local TCP test server was created on `127.0.0.1:5000` to provide a controlled environment for testing.

The scanner successfully detected the test server's open TCP port.

### Phase 4 — Documentation
- Added professional README
- Added MIT License
- Added `.gitignore`
- Documented ethical and authorized use

## Author

Developed by John Ogye as a cybersecurity learning project.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

