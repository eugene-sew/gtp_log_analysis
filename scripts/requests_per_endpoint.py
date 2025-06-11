#!/usr/bin/env python3
"""
Script to count the number of times each endpoint was called from a log file.
Usage: python requests_per_endpoint.py <log_file>
"""
import sys
import os
import re
from collections import Counter
import json

def prepare_log(log_file: str) -> list[str]:
    """
    Reads the log file and returns a list of valid log lines.
    Only lines with a valid IP address in the second field are included.
    """
    from ipaddress import ip_address
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

def number_of_times_endpoints_called(logs: list[str]):
    """
    Finds the number of unique endpoints and the total number of times each was called.
    For each log line, extracts the endpoint (path) from the HTTP request using regex,
    then counts how many times each endpoint appears in the logs.
    Returns a dictionary mapping endpoint to request count.
    """
    # Compile a regex pattern to match the HTTP request part, e.g. "GET /endpoint HTTP/1.1"
    request_pattern = re.compile(r'"[A-Z]+ ([^ ]+) HTTP/[^\"]+"')
    endpoints = []
    for log in logs:
        # Search for the HTTP request in the log line
        match = request_pattern.search(log)
        if match:
            # Extract the endpoint (second part of the HTTP request)
            endpoint = match.group(1)
            endpoints.append(endpoint)
    # Count how many times each endpoint was accessed
    endpoint_counts = Counter(endpoints)
    return dict(endpoint_counts)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {os.path.basename(__file__)} <log_file>")
        sys.exit(1)
    log_file = sys.argv[1]
    logs = prepare_log(log_file)
    endpoint_counts = number_of_times_endpoints_called(logs)
    print("Requests per Endpoint:")
    print(json.dumps(endpoint_counts,indent=4))

