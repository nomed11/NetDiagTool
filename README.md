# Network Diagnostic Tool

## Introduction

This Network Diagnostic Tool is a Python-based utility designed to automate and streamline the use of various network diagnostic commands. It was created for students in Internet Architecture and Protocols class (ECE-GY 6353) at NYU Tandon, who need to quickly assess and troubleshoot network issues on machines they access via SSH.

## Features

The tool offers a range of functionalities, including:

- **Ping:** Test the reachability of a host on an IP network.
- **Traceroute:** Display the route and measure transit delays of packets.
- **IP Address Display:** Show all network interfaces and their IP addresses.
- **IP Routing Table Display:** View the routing table of the system.
- **TCPDump:** Capture and display network packet data.
- **DNS Lookup:** Resolve domain names to IP addresses.
- **Speed Test:** Check the internet connection speed.

## Installation

1. Ensure Python 3.x is installed on your system.
2. Clone the repository:
   `git clone https://github.com/nomed11/NetDiagTool.git`
3. Navigate to the project directory:
   `cd NetDiagTool`

## Usage

The tool is command-line based and offers various flags and options:

`python network_tool.py [options]`


Options include:
- `-p/--ping [host]`: Ping a specified host.
- `-t/--traceroute [host]`: Perform a traceroute to a specified host.
- `--ipaddr`: Display the IP addresses of network interfaces.
- `--iproute`: Show the IP routing table.
- `-d/--tcpdump [interface]`: Run tcpdump for the specified interface.
- `-c/--count [number]`: Specify the number of packets for tcpdump.
- `--flags`: Include additional flags in tcpdump.
- `-l/--lookup [hostname]`: Perform a DNS lookup.
- `-s/--speedtest`: Run an internet speed test.

## Testing

The tool comes with a suite of tests to ensure each function performs as expected. To run the tests, use the following command from the root directory:

`python -m pytest`


These tests cover various scenarios, including command executions, error handling, and specific network situations.

## Contributions

Contributions and further addition of functionality to this project are welcome. Please make you follow the coding standards and write tests for new functionalities.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
