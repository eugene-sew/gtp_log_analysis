#!/usr/bin/env python3
"""
Script to count the number of requests per unique IP address in the 10-second window after the first request.
Usage: python requests_per_ip_10sec_window.py <log_file>
"""
import sys
import os
import json
import datetime
from collections import defaultdict
from ipaddress import ip_address

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
                if ip_address(line.split(' ')[1]):
                    logs.append(line)
            except ValueError:
                pass  # Ignore invalid IP lines
    return logs

def requests_per_ip_10sec_window(logs: list[str]):
    """
    For each IP address, finds how many requests came in after the first request within a 10-second window.
    Returns a dictionary with window start/end and request count for each IP.
    """
    ip_timestamps = defaultdict(list)
    for log in logs:
        ip = log.split(' ')[1]
        timestr = log.split(' ')[0]
        try:
            # Parse the timestamp (ISO format, replace Z with +00:00 for UTC)
            timestamp = datetime.datetime.fromisoformat(timestr.replace('Z', '+00:00'))
        except ValueError:
            continue
        ip_timestamps[ip].append(timestamp)

    for ip in ip_timestamps:
        ip_timestamps[ip].sort()

    result = {}
    # for each ip address, find the number of requests within the 10-second window after the first request
    for ip, timestamps in ip_timestamps.items():
        window_start = timestamps[0]
        window_end = window_start + datetime.timedelta(seconds=10)
        requests_within_window_count = sum(1 for timestamp in timestamps if timestamp <= window_end and timestamp != window_start)
        result[ip] = {
            "window_start": window_start.isoformat(),
            "requests_within_window": requests_within_window_count,
            "window_end": window_end.isoformat()
        }
    return result

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {os.path.basename(__file__)} <log_file>")
        sys.exit(1)
    log_file = sys.argv[1]
    logs = prepare_log(log_file)
    result = requests_per_ip_10sec_window(logs)
    print("Requests per IP in 10-second window after first request:")
    print(json.dumps(result, indent=4))
