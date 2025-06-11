#!/usr/bin/env python3
"""
Script to count the number of requests per unique IP address from a log file.
Usage: python requests_per_ip.py <log_file>
"""
import sys
import os
from collections import Counter
from ipaddress import ip_address
import json

def prepare_log(log_file: str) -> list[str]:
    """
    Reads the log file and returns a list of valid log lines.
    Only lines with a valid IP address in the second field are included.
    """
    logs = []
    with open(log_file, 'r') as f:
        for line in f:
            line = line.strip()
            try:
                # Check if the second field is a valid IP address
                if ip_address(line.split(' ')[1]):
                    logs.append(line)
            except ValueError:
                pass  # Ignore invalid IP lines
    return logs

def unique_ip(logs: list[str]) -> list[str]:
    """
    Returns a list of unique IP addresses found in the logs.
    """
    ip_addresses = []
    for log in logs:
        ip_addresses.append(log.split(' ')[1])
    return list(set(ip_addresses))

def requests_per_ip(logs: list[str]):
    """
    Returns a dictionary mapping each unique IP address to the number of requests from that IP.
    """
    ip_addresses = unique_ip(logs)
    ip_counts = {}
    for ip in ip_addresses:
        ip_logs = [log for log in logs if log.split(' ')[1] == ip]
        ip_counts[ip] = len(ip_logs)
    return ip_counts

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {os.path.basename(__file__)} <log_file>")
        sys.exit(1)
    log_file = sys.argv[1]
    logs = prepare_log(log_file)
    ip_counts = requests_per_ip(logs)
    print("Requests per IP:")
    print(json.dumps(ip_counts,indent=4))
