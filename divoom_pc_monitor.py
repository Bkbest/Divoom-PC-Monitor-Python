import argparse
import time
from threading import Timer

from functions.read_config import read_config
from functions.cpu_util import cpu_usage
from functions.gpu_util import gpu_main
from functions.mem_util import mem_usage
from functions.hdd_util import hdd_usage
from functions.http_post import send_system_info

def collect_and_send_info(interval, verbose, testing):
    # Print start data/time
    print(f"Data collection started at {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Gather system variables from config.env file
    device_id, device_ip, lcd_independence, lcd_index, lcd_clock_id, hard_drive_list = read_config()

    # Get CPU usage and temperature
    cpu_util, cpu_temp = cpu_usage()
    if verbose:
        print(f"CPU Usage: {cpu_util}%, CPU Temperature: {cpu_temp}°C")

    # Get GPU usage and temperature
    gpu_util, gpu_temp = gpu_main()
    if verbose:
        print(f"GPU Usage: {gpu_util}%, GPU Temperature: {gpu_temp}°C")

    # Get memory usage
    mem_util = mem_usage()
    if verbose:
        print(f"Memory Usage: {mem_util}%")
    
    # Get disk with highest utilization
    disk_name, disk_util = hdd_usage(hard_drive_list)
    if verbose:
        print(f"Disk with highest utilization: {disk_name}, Utilization: {disk_util}%")

    # Send system information to the Divoom Times Gate device
    if not testing:
        send_system_info(device_ip, lcd_index, cpu_util, cpu_temp, gpu_util, gpu_temp, mem_util, disk_util, verbose)

    # Print end data/time
    print(f"Data collection completed at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Next data collection in {interval} seconds")
    print("-" * 50)

    # Set up the next timer
    Timer(interval, collect_and_send_info, [interval, verbose, testing]).start()

def main():
    parser = argparse.ArgumentParser(
        description="DivoomPCMonitor.py - Monitor system information on a Divoom Times Gate device"
    )
    parser.add_argument(
        "-i", "--interval_in_seconds",
        type=int,
        default=30,
        help="Interval in seconds to update the system information (default: 30)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        dest="verbose",
        default=False,
        help="Display verbose output on the console"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="v1.4.0"
    )
    parser.add_argument(
        "--testing",
        action="store_true",
        dest="testing",
        default=False,
        help="Run in testing mode; do not send data to the Divoom Times Gate device"
    )

    args = parser.parse_args()

    # Start the initial data collection and sending process
    collect_and_send_info(args.interval_in_seconds, args.verbose, args.testing)

if __name__ == "__main__":
    main()
