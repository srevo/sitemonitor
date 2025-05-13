#!/usr/bin/env python3
"""
Terminal Website Monitor - A simple console-based website monitoring tool
that checks website status and latency at regular intervals.
"""

import requests
import time
import datetime
import statistics
import signal
import sys
import argparse
from urllib.parse import urlparse
import os

# ANSI color codes for terminal output
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"

# Check if terminal supports colors
def supports_color():
    """Check if the terminal supports color output."""
    plat = sys.platform
    supported_platform = plat != 'win32' or 'ANSICON' in os.environ
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    return supported_platform and is_a_tty

# Toggle colors based on terminal capability
USE_COLORS = supports_color()

def colored(text, color):
    """Apply color to text if supported."""
    if USE_COLORS:
        return f"{color}{text}{Colors.RESET}"
    return text

class WebsiteMonitor:
    def __init__(self, url, interval=5, timeout=10):
        self.url = url
        self.interval = interval
        self.timeout = timeout
        self.response_times = []
        self.success_count = 0
        self.error_count = 0
        self.running = True
        self.last_status = None
        self.start_time = datetime.datetime.now()
        
        # Setup signal handlers for clean exit
        signal.signal(signal.SIGINT, self.handle_exit)
        signal.signal(signal.SIGTERM, self.handle_exit)
        
        # Validate URL
        self.validate_url()
    
    def validate_url(self):
        """Ensure URL is properly formatted."""
        if not urlparse(self.url).scheme:
            self.url = "http://" + self.url
        
        try:
            result = urlparse(self.url)
            if not all([result.scheme, result.netloc]):
                print(colored("Error: Invalid URL format", Colors.RED))
                sys.exit(1)
        except Exception as e:
            print(colored(f"Error: {str(e)}", Colors.RED))
            sys.exit(1)
    
    def handle_exit(self, signum, frame):
        """Handle Ctrl+C and other termination signals."""
        print("\n" + colored("Stopping website monitoring...", Colors.YELLOW))
        self.running = False
        self.print_summary()
        sys.exit(0)
    
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print the application header."""
        self.clear_screen()
        print(colored("==================================", Colors.CYAN))
        print(colored("    TERMINAL WEBSITE MONITOR     ", Colors.CYAN + Colors.BOLD))
        print(colored("==================================", Colors.CYAN))
        print(f"Monitoring: {colored(self.url, Colors.CYAN)}")
        print(f"Interval: {colored(f'{self.interval} seconds', Colors.CYAN)}")
        print(f"Started at: {colored(self.start_time.strftime('%Y-%m-%d %H:%M:%S'), Colors.CYAN)}")
        print(colored("==================================", Colors.CYAN))
        print("Press Ctrl+C to exit\n")
    
    def check_website(self):
        """Perform a single website check."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        status_indicator = "✓"
        status_color = Colors.GREEN
        
        try:
            start_time = time.time()
            response = requests.get(self.url, timeout=self.timeout)
            response_time = time.time() - start_time
            response_time_ms = round(response_time * 1000)
            
            # Add response time to list for statistics
            self.response_times.append(response_time_ms)
            
            # Process status code
            if response.status_code < 400:
                status = f"Online (HTTP {response.status_code})"
                self.success_count += 1
            else:
                status = f"Error (HTTP {response.status_code})"
                status_indicator = "!"
                status_color = Colors.YELLOW
                self.error_count += 1
                
        except requests.exceptions.Timeout:
            status = "Timeout"
            response_time_ms = None
            status_indicator = "✗"
            status_color = Colors.RED
            self.error_count += 1
            
        except requests.exceptions.ConnectionError:
            status = "Connection Failed"
            response_time_ms = None
            status_indicator = "✗"
            status_color = Colors.RED
            self.error_count += 1
            
        except requests.exceptions.RequestException as e:
            status = f"Request Error: {str(e)}"
            response_time_ms = None
            status_indicator = "✗"
            status_color = Colors.RED
            self.error_count += 1
            
        except Exception as e:
            status = f"Error: {str(e)}"
            response_time_ms = None
            status_indicator = "✗"
            status_color = Colors.RED
            self.error_count += 1
        
        self.last_status = {
            'timestamp': timestamp,
            'status': status,
            'response_time': response_time_ms,
            'indicator': status_indicator,
            'color': status_color
        }
        
        return self.last_status
    
    def calculate_statistics(self):
        """Calculate statistics from response times."""
        stats = {
            'count': len(self.response_times),
            'min': None,
            'max': None,
            'avg': None,
            'success_rate': 0
        }
        
        if self.response_times:
            stats['min'] = min(self.response_times)
            stats['max'] = max(self.response_times)
            stats['avg'] = round(statistics.mean(self.response_times), 1)
        
        total_checks = self.success_count + self.error_count
        if total_checks > 0:
            stats['success_rate'] = round((self.success_count / total_checks) * 100, 1)
        
        return stats
    
    def print_status_line(self, status_data):
        """Print a formatted status line."""
        timestamp = status_data['timestamp']
        status = status_data['status']
        response_time = status_data['response_time']
        indicator = status_data['indicator']
        color = status_data['color']
        
        indicator_colored = colored(f"[{indicator}]", color)
        time_str = colored(timestamp, Colors.GRAY)
        status_str = colored(status, color)
        
        # Format response time if available
        if response_time is not None:
            if response_time < 100:
                rt_color = Colors.GREEN
            elif response_time < 300:
                rt_color = Colors.YELLOW
            else:
                rt_color = Colors.RED
            
            response_str = colored(f"{response_time} ms", rt_color)
            print(f"{indicator_colored} {time_str} - {status_str} - {response_str}")
        else:
            print(f"{indicator_colored} {time_str} - {status_str}")
    
    def print_statistics(self, stats):
        """Print current statistics."""
        print("\n" + colored("--- Statistics ---", Colors.BLUE))
        
        if stats['count'] > 0:
            # Use separate variables to avoid dictionary access inside f-strings
            count = stats['count']
            success_rate = stats['success_rate']
            min_time = stats['min']
            max_time = stats['max']
            avg_time = stats['avg']
            
            print(f"Checks: {count}")
            # Create colored strings separately from the f-strings
            success_rate_colored = colored(f"{success_rate}%", Colors.GREEN)
            min_time_colored = colored(f"{min_time} ms", Colors.CYAN)
            max_time_colored = colored(f"{max_time} ms", Colors.MAGENTA)
            avg_time_colored = colored(f"{avg_time} ms", Colors.BLUE)
            
            print(f"Success Rate: {success_rate_colored}")
            print(f"Min Response: {min_time_colored}")
            print(f"Max Response: {max_time_colored}")
            print(f"Avg Response: {avg_time_colored}")
        else:
            print(colored("No data collected yet", Colors.GRAY))
    
    def print_summary(self):
        """Print a summary of the monitoring session."""
        duration = datetime.datetime.now() - self.start_time
        minutes, seconds = divmod(duration.seconds, 60)
        hours, minutes = divmod(minutes, 60)
        
        print("\n" + colored("=== Monitoring Summary ===", Colors.CYAN + Colors.BOLD))
        print(f"URL: {self.url}")
        print(f"Duration: {hours}h {minutes}m {seconds}s")
        print(f"Total Checks: {self.success_count + self.error_count}")
        print(f"Successful: {self.success_count}")
        print(f"Failed: {self.error_count}")
        
        stats = self.calculate_statistics()
        if stats['count'] > 0:
            print(f"Success Rate: {stats['success_rate']}%")
            print(f"Min Response: {stats['min']} ms")
            print(f"Max Response: {stats['max']} ms")
            print(f"Avg Response: {stats['avg']} ms")
    
    def run(self):
        """Main monitoring loop."""
        try:
            while self.running:
                self.print_header()
                
                # Perform the check
                status_data = self.check_website()
                self.print_status_line(status_data)
                
                # Calculate and display statistics
                stats = self.calculate_statistics()
                self.print_statistics(stats)
                
                # Show last 5 checks if we have history
                if hasattr(self, 'history') and len(self.history) > 1:
                    print("\n" + colored("--- Recent Checks ---", Colors.BLUE))
                    for hist in self.history[-5:]:
                        if hist != status_data:  # Don't repeat the current check
                            self.print_status_line(hist)
                
                # Keep a history of the last 10 checks
                if not hasattr(self, 'history'):
                    self.history = []
                self.history.append(status_data)
                if len(self.history) > 10:
                    self.history.pop(0)
                
                # Wait for next check
                if self.running:
                    for _ in range(self.interval):
                        if not self.running:
                            break
                        time.sleep(1)
                        
        except Exception as e:
            print(colored(f"Error in monitoring loop: {str(e)}", Colors.RED))
            self.running = False
        finally:
            if self.running:
                self.print_summary()

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Monitor website status and response times.")
    parser.add_argument("url", help="URL to monitor (e.g., https://example.com)")
    parser.add_argument("-i", "--interval", type=int, default=5, 
                      help="Check interval in seconds (default: 5)")
    parser.add_argument("-t", "--timeout", type=int, default=10,
                      help="Request timeout in seconds (default: 10)")
    
    return parser.parse_args()

def main():
    """Main entry point."""
    args = parse_arguments()
    
    monitor = WebsiteMonitor(args.url, args.interval, args.timeout)
    monitor.run()

if __name__ == "__main__":
    main()

