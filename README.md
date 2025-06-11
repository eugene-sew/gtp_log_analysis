# Log Analysis Scripts

This project provides standalone Python scripts for analyzing web server logs. Each script is self-contained and focused on a specific type of analysis. You do **not** need to use or reference any shared module—all logic is included in each script.

**All script outputs are in JSON format, making them easy to ingest by other systems, tools, or for further automation and visualization.**

## Log File Format

Each script expects your log file to have lines in the following format:

```
2025-06-03T10:09:02.588Z 197.159.135.110 - - [03/Jun/2025:10:09:02 +0000] "GET /favicon.ico HTTP/1.1" 200 - "http://108.129.212.117:8080/" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
```

- **Timestamp**: 2025-06-03T10:09:02.588Z
- **IP Address**: 197.159.135.110
- **HTTP Method/Endpoint**: "GET /favicon.ico HTTP/1.1"
- **User Agent**: "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"

## Standalone Scripts and Output Structure

Place your log file (e.g., `NodeJsApp.log`) in the project directory. Run any script with Python 3 as shown below. Each script prints its results as formatted JSON.

### 1. Requests per IP in 10-Second Window

For each IP address, count how many requests came in within a 10-second window after the first request from that IP.

**Usage:**

```bash
python scripts/requests_per_ip_10sec_window.py NodeJsApp.log
```

**Output Structure:**

```json
{
    "129.222.148.186": {
        "window_start": "2025-06-03T10:08:27.332000+00:00",
        "requests_within_window": 8,
        "window_end": "2025-06-03T10:08:37.332000+00:00"
    },
    ...
}
```

### 2. Requests per User Agent

Count the number of requests made by each user agent string.

**Usage:**

```bash
python scripts/requests_per_user_agent.py NodeJsApp.log
```

**Output Structure:**

```json
{
  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36": 427,
  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36": 133,
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Safari/605.1.15": 84,
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36": 42,
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36": 21,
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36": 6,
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36": 11
}
```

### 3. Requests per Endpoint

Count the number of times each endpoint (path) was called.

**Usage:**

```bash
python scripts/requests_per_endpoint.py NodeJsApp.log
```

**Output Structure:**

```json
{
  "/favicon.ico": 316,
  "/": 408
}
```

### 4. Requests per IP in 10-Second Window

For each IP address, count how many requests came in within a 10-second window after the first request from that IP.

**Usage:**

```bash
python scripts/requests_per_ip_10sec_window.py NodeJsApp.log
```

**Output Structure:**

```json
{
    "129.222.148.186": {
        "window_start": "2025-06-03T10:08:27.332000+00:00",
        "requests_within_window": 8,
        "window_end": "2025-06-03T10:08:37.332000+00:00"
    },
    ...
}
```

## Requirements

- Python 3.7+
- No external dependencies required (uses only Python standard library)
