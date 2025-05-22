# Terminal Website Monitor

A simple console-based website monitoring tool that checks website status and latency at regular intervals. This script is designed for users who prefer to monitor websites from the terminal, providing clear, colored output and useful statistics.

## Features

- **Real-time Monitoring:** Checks website status at user-defined intervals.
- **Latency Tracking:** Measures and records response times for each check.
- **Color-coded Output:** Uses ANSI color codes to indicate status (Online, Error, Timeout) for easy visual assessment.
- **Statistical Summary:** Provides statistics like min/max/average response times and success rate.
- **Command-line Interface:** Configurable via command-line arguments for URL, interval, and timeout.
- **Clean Exit:** Handles `Ctrl+C` gracefully, printing a final summary before exiting.
- **Dynamic Color Support:** Automatically detects if the terminal supports colors.
- **URL Validation:** Basic validation to ensure the URL is correctly formatted.

## Requirements

- Python 3
- `requests` library

## Installation

1.  **Python 3:** Ensure you have Python 3 installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
2.  **requests library:** If you don't have the `requests` library installed, you can install it using pip:
    ```bash
    pip install requests
    ```

## Usage

Run the script from your terminal using the following command structure:

```bash
python terminal_monitor.py <URL> [options]
```

**Arguments:**

-   `URL`: The full URL of the website to monitor (e.g., `https://example.com` or `example.com`). If the scheme (http/https) is omitted, `http://` will be prepended.

**Options:**

-   `-i, --interval <seconds>`: Check interval in seconds. Default is `5` seconds.
-   `-t, --timeout <seconds>`: Request timeout in seconds. Default is `10` seconds.

**Examples:**

1.  Monitor `google.com` with default settings (5s interval, 10s timeout):
    ```bash
    python terminal_monitor.py google.com
    ```

2.  Monitor `mysite.org` every 10 seconds with a timeout of 5 seconds:
    ```bash
    python terminal_monitor.py https://mysite.org -i 10 -t 5
    ```

## Output Description

The script provides a continuously updating display in your terminal:

-   **Header:** Shows the URL being monitored, the check interval, and the start time.
-   **Status Lines:** Each check is displayed with:
    -   `[✓]`, `[!]`, or `[✗]`: An indicator of the check result.
        -   `✓` (Green): Successful check (HTTP 2xx-3xx).
        -   `!` (Yellow): HTTP error (HTTP 4xx-5xx).
        -   `✗` (Red): Request error (Timeout, Connection Failed, etc.).
    -   `Timestamp`: The time of the check.
    -   `Status`: A description of the result (e.g., "Online (HTTP 200)", "Timeout", "Connection Failed").
    -   `Response Time`: The time taken for the server to respond, in milliseconds (ms). The color of the response time indicates performance:
        -   Green: < 100ms
        -   Yellow: 100ms - 300ms
        -   Red: > 300ms
-   **Statistics:** A summary of the monitoring session so far:
    -   `Checks`: Total number of checks performed.
    -   `Success Rate`: Percentage of successful checks.
    -   `Min Response`: Minimum response time recorded.
    -   `Max Response`: Maximum response time recorded.
    -   `Avg Response`: Average response time.
-   **Recent Checks:** A list of the last few checks to provide historical context.

Upon exiting (Ctrl+C), a final summary of the entire monitoring session is displayed.

## How to Contribute

Contributions are welcome! If you have suggestions for improvements or find any issues, please feel free to:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes.
4.  Submit a pull request with a clear description of your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
(Note: You will need to create a LICENSE file, typically containing the MIT License text if that's your chosen license).
