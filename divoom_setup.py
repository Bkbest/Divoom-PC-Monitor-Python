# This script gathers the Divoom device information, system variables, and commits them to a configuation file named config.env.

# Imports
from functions.device_endpoint import get_device_info, get_lcd_info
from functions.get_os_drives import get_os_drives
from functions.gen_config import generate_config_file

# Function to enter a new line, print separator, and enter a new line all in one
def separator():
    print('\n' + '-' * 50 + '\n')

# Gather required variables
def gather_variables():
    device_id, device_ip = get_device_info()
    separator()
    lcd_independence, lcd_index, lcd_clock_id = get_lcd_info(device_id)
    separator()
    hard_drive = get_os_drives()
    separator()

    # Print all gathered variables
    print(f'Device ID: {device_id}')
    print(f'Device IP: {device_ip}')
    print(f'Lcd Independence: {lcd_independence}')
    print(f'Lcd Index: {lcd_index}')
    print(f'Lcd Clock ID: {lcd_clock_id}')
    print(f'Hard Drive: {hard_drive}')
    separator()

    return device_id, device_ip, lcd_independence, lcd_index, lcd_clock_id, hard_drive



device_id, device_ip, lcd_independence, lcd_index, lcd_clock_id, hard_drive = gather_variables()

# Write gathered variables to configuration file
generate_config_file(device_id, device_ip, lcd_independence, lcd_index, lcd_clock_id, hard_drive)
