import pytest
import network_tool
import socket
from unittest.mock import patch, MagicMock
import io

@pytest.fixture
def mock_subprocess_popen():
    mock_process = MagicMock()
    mock_process.stdout.readline.side_effect = ["test output\n", ""]
    mock_process.communicate.return_value = ('output', 'error message')
    mock_process.returncode = 0
    with patch('subprocess.Popen', return_value=mock_process) as mock_test:
        yield mock_test

@pytest.fixture
def mock_socket():
    with patch('socket.gethostbyname') as mock_socket:
        yield mock_socket

def test_ping(mock_subprocess_popen):
    network_tool.ping("8.8.8.8")
    mock_subprocess_popen.assert_called_with(["ping", "-c", "4", "8.8.8.8"], stdout=-1, stderr=-1, text=True)

def test_traceroute(mock_subprocess_popen):
    network_tool.traceroute("8.8.8.8")
    mock_subprocess_popen.assert_called_with(["traceroute", "8.8.8.8"], stdout=-1, stderr=-1, text=True)

def test_show_ip_addr(mock_subprocess_popen):
    network_tool.show_ip_addr()
    expected_command = ["ifconfig"] if network_tool.platform.system() == "Darwin" else ["ip", "addr"]
    mock_subprocess_popen.assert_called_with(expected_command, stdout=-1, stderr=-1, text=True)

def test_show_ip_route(mock_subprocess_popen):
    network_tool.show_ip_route()
    expected_command = ["netstat", "-nr"] if network_tool.platform.system() == "Darwin" else ["ip", "route", "show"]
    mock_subprocess_popen.assert_called_with(expected_command, stdout=-1, stderr=-1, text=True)

def test_run_tcpdump(mock_subprocess_popen):
    interface = 'eth0'
    network_tool.run_tcpdump(interface)
    mock_subprocess_popen.assert_called_with(['tcpdump', '-i', interface], stdout=-1, stderr=-1, text=True)

def test_run_speedtest(mock_subprocess_popen):
    network_tool.run_speedtest()
    mock_subprocess_popen.assert_called_with(['speedtest-cli'], stdout=-1, stderr=-1, text=True)

def test_dns_lookup_success(mock_socket):
    mock_socket.return_value = "93.184.216.34"
    assert network_tool.dns_lookup("example.com") == "93.184.216.34"

def test_dns_lookup_failure(mock_socket):
    mock_socket.side_effect = socket.gaierror
    with pytest.raises(socket.gaierror):
        network_tool.dns_lookup("invalid_domain")
