import datetime
from ipaddress import ip_address
import re
from collections import Counter,defaultdict
import json


# log_explorer.py
# This script is part of a class assignment for log analysis. It provides functions to analyze web server logs for:
# 1. Counting requests per IP in a 10-second window after the first request (rate-limiting scenario).
# 2. Counting requests from each user agent type.
# 3. Counting the number of times each endpoint was accessed.
# Each function is documented with comments for clarity.

import datetime
from ipaddress import ip_address
import re
from collections import Counter, defaultdict
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
                print(f"Invalid IP address: {line.split(' ')[1]}")
    return logs


def unique_ip(logs: list[str]) -> list[str]:
    """
    Returns a list of unique IP addresses found in the logs.
    """
    ip_addresses = []
    for log in logs:
        ip_addresses.append(log.split(' ')[1])
    return list(set(ip_addresses))


def unique_user_agents(logs: list[str], pattern: re.Pattern) -> list[str]:
    """
    Returns a list of unique user agent strings using a regex pattern.
    The pattern should match the user agent portion of the log line (typically the last quoted string).
    """
    user_agents = []
    for log in logs:
        match = pattern.search(log)
        if match:
            user_agents.append(match.group(1))
    return list(set(user_agents))


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


def requests_per_user_agent(logs: list[str], pattern: re.Pattern):
    """
    Returns a dictionary mapping each user agent to the number of requests made by that user agent.
    The user agent is extracted using the provided regex pattern.
    """
    user_agent_counts = {}
    for log in logs:
        match = pattern.search(log)
        if match:
            user_agent = match.group(1)
            user_agent_counts[user_agent] = user_agent_counts.get(user_agent, 0) + 1
    return user_agent_counts


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
            print(f"Invalid timestamp: {timestr}")
            continue
        ip_timestamps[ip].append(timestamp)

    # Sort timestamps for each IP for accurate windowing
    for ip in ip_timestamps:
        ip_timestamps[ip].sort()

    # Count requests per IP in the first 10-second window after the first request
    result = {}
    for ip, timestamps in ip_timestamps.items():
        window_start = timestamps[0]
        window_end = window_start + datetime.timedelta(seconds=10)
        # Count requests within the window (including the first request)
        requests_within_window_count = sum(1 for timestamp in timestamps if timestamp <= window_end)
        result[ip] = {
            "window_start": window_start.isoformat(),
            "requests_within_window": requests_within_window_count,
            "window_end": window_end.isoformat()
        }
    return result


def requests_per_user_agent(logs: list[str], pattern: re.Pattern):
    """
    Returns a Counter of requests per user agent using the provided regex pattern.
    Useful for quick stats in one line.
    """
    user_agents = []
    for log in logs:
        match = pattern.search(log)
        if match:
            user_agents.append(match.group(1))
    return Counter(user_agents)

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

def analyze_logs(log_file: str):
    user_agent_pattern = re.compile(r'"([^"]*)"$')
    print("\n--- Log Analysis Report ---\n")
    logs = prepare_log(log_file)
    print("\nTotal Number of Requests:", len(logs))
    
    print("\nList of unique IP addresses:")
    print(unique_ip(logs))
    
    print("\nNumber of requests per unique IP:")
    print(json.dumps(requests_per_ip(logs),indent=4))
    
    print("\nNumber of requests per unique IP - 10 seconds after initial recorded request:")
    print(json.dumps(requests_per_ip_10sec_window(logs),indent=4))

    print("\nList of unique user agents:")
    print(json.dumps(unique_user_agents(logs,user_agent_pattern),indent=4))
    
    print("\nNumber of requests per user agent:")
    print(json.dumps(requests_per_user_agent(logs,user_agent_pattern),indent=4))
    
    print("\nNumber of times endpoints called:")
    print(json.dumps(number_of_times_endpoints_called(logs),indent=4))


if __name__ == "__main__":
    log_file = "NodeJsApp.log"
    analyze_logs(log_file) 
        