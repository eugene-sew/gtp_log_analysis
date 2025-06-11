#!/usr/bin/env python3
"""
Script to count the number of requests per user agent from a log file.
Usage: python requests_per_user_agent.py <log_file>
"""
import sys
import os
import re
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

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {os.path.basename(__file__)} <log_file>")
        sys.exit(1)
    log_file = sys.argv[1]
    logs = prepare_log(log_file)
    user_agent_pattern = re.compile(r'"([^"]*)"$')
    ua_counts = requests_per_user_agent(logs, user_agent_pattern)
    print("Requests per User Agent:")
    print(json.dumps(ua_counts,indent=4))
