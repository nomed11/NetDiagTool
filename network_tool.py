import subprocess
import socket
import argparse
import platform

def print_info(message):
    print(f"[INFO] {message}")

def print_error(message):
    print(f"[ERROR] {message}")

def print_success(message):
    print(f"[SUCCESS] {message}")

def run_command_live_output(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())

    _, stderr = process.communicate()
    if process.returncode != 0:
        print_error(stderr)


def ping(host):
    print_info(f"Pinging {host}")
    run_command_live_output(["ping", "-c", "4", host])

def traceroute(host):
    print_info(f"Tracerouting to {host}")
    run_command_live_output(["traceroute", host])

def show_ip_addr():
    print_info("Showing IP addresses")
    if platform.system() == "Darwin":
        run_command_live_output(["ifconfig"])
    else:
        run_command_live_output(["ip", "addr"])

def show_ip_route():
    print_info("Showing IP routing table")
    if platform.system() == "Darwin":
        run_command_live_output(["netstat", "-nr"])
    else:
        run_command_live_output(["ip", "route", "show"])

def run_tcpdump(interface="any", count=5, use_flags=False):
    print_info(f"\nRunning tcpdump on interface {interface} for {count} packets")
    command = ["sudo", "tcpdump", "-c", str(count), "-i", interface]

    if use_flags:
        command.extend(["-enx"])

    try:
        run_command_live_output(command)
    except KeyboardInterrupt:
        print("\nTcpdump interrupted by user")

def dns_lookup(hostname):
    try:
        print_info(f"\nResolving DNS for {hostname}")
        ip_address = socket.gethostbyname(hostname)
        print_success(f"{hostname} resolved to {ip_address}")
        return ip_address  # return the resolved IP address
    except socket.gaierror:
        print_error(f"Failed to resolve {hostname}")
        raise  # re-raise the exception so it can be caught by test_dns_lookup


def run_speedtest():
    try:
        print_info("\nRunning speed test. This may take a while...")
        st = subprocess.Popen(['speedtest-cli'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        while True:
            output = st.stdout.readline()
            if output == '' and st.poll() is not None:
                break
            if output:
                print(output.strip())

    except Exception as e:
        print_error(f"Speed test failed: {e}")

def main():
    parser = argparse.ArgumentParser(description="Network Diagnostic Tool")
    parser.add_argument("-p", "--ping", help="Ping a host", type=str)
    parser.add_argument("-t", "--traceroute", help="Perform a traceroute to a host", type=str)
    parser.add_argument("--ipaddr", help="Display IP addresses", action="store_true")
    parser.add_argument("--iproute", help="Show IP routing table", action="store_true")
    parser.add_argument("-d", "--tcpdump", help="Run tcpdump on a specified interface", type=str, nargs='?', const="any")
    parser.add_argument("-c", "--count", help="Number of packets for tcpdump", default=5, type=int)
    parser.add_argument("--flags", help="Use -enx flags with tcpdump", action="store_true")
    parser.add_argument("-l", "--lookup", help="DNS lookup for a specified hostname", type=str)
    parser.add_argument("-s", "--speedtest", help="Run internet speed test", action="store_true")

    args = parser.parse_args()

    if args.ping:
        ping(args.ping)
    elif args.traceroute:
        traceroute(args.traceroute)
    elif args.ipaddr:
        show_ip_addr()
    elif args.iproute:
        show_ip_route()
    elif args.tcpdump:
        run_tcpdump(args.tcpdump, args.count, args.flags)
    elif args.lookup:
        dns_lookup(args.lookup)
    elif args.speedtest:
        run_speedtest()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
