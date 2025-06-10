# Log Explorer

This script (`log_explorer.py`) is for analyzing web server logs. It provides several utilities to extract and summarize key information from server access logs.

## Objectives

1. **For each IP address, check how many requests came in after the first request in a 10-second window**

   - The script identifies all requests from each unique IP address and determines how many requests occurred within a 10-second window after the first request from that IP. This is useful for rate-limiting analysis and detecting bursts of activity.

2. **Count requests coming from each user agent type**

   - The script extracts the user agent string (browser, bot, etc.) from each log entry and counts how many requests were made by each unique user agent. This helps in understanding client diversity and identifying automated traffic.

3. **Count the number of times each endpoint was accessed**
   - The script parses the HTTP request line from each log entry to extract the endpoint (e.g., `/`, `/favicon.ico`) and counts how many times each endpoint was requested. This is useful for identifying popular resources and usage patterns.

## How It Works

- The script reads a log file (default: `NodeJsApp.log`) and processes each line.
- It uses regular expressions and Python's standard libraries for parsing and analysis.
- The output is a summary report printed to the console, including:
  - Total number of requests
  - List of unique IP addresses
  - Number of requests per IP
  - Number of requests per IP in a 10-second window after the initial request
  - List of unique user agents
  - Number of requests per user agent
  - Number of times each endpoint was called

## Usage

1. Place your server log file (e.g., `NodeJsApp.log`) in the same directory as `log_explorer.py`.
2. Run the script with Python 3:

   ```bash
   python log_explorer.py
   ```

3. The analysis report will be printed to the terminal.

## Requirements

- Python 3.7+
- No external dependencies required (uses only Python standard library)

## File Overview

- `log_explorer.py`: Main script containing all analysis functions.
- `NodeJsApp.log`: Example log file to analyze (not included).

## Notes

- The script expects log lines in a format similar to standard morgan log.
- Invalid lines (e.g., missing IP address) are skipped with a warning.
