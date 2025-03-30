# Imports
import requests

from functions.get_selection import get_device_selection, get_lcd_selection, get_lcd_independence_selection
from functions.format_list import format_device_list, format_lcd_list, format_lcd_independence_list

# Get device list from the network endpoint, output the formatted list, and return the selected device
def get_device_info():
    try:
        response = requests.get(f'https://app.divoom-gz.com/Device/ReturnSameLANDevice')
        device_list = response.json().get('DeviceList')
        if not device_list:  # Check if device_list is empty
            print("No devices found on the network.")
            return None, None
        format_device_list(device_list)
        selected_device = get_device_selection(device_list)
        return device_list[selected_device].get('DeviceId'), device_list[selected_device].get('DevicePrivateIP')
    except Exception as e:
        print(f'Error getting device list: {e}')
        return None, None  # Return None for both values on error


# Get the LCD list from the network endpoint, output the formatted list, and return the selected LCD
def get_lcd_info(device_id):
    try:
        response = requests.get(f'https://app.divoom-gz.com/Channel/Get5LcdInfoV2?DeviceType=LCD&DeviceId={device_id}')
        data = response.json()
        lcd_independence_list = data.get('LcdIndependenceList', [])

        if not lcd_independence_list:
            print("LcdIndependenceList is empty. Assuming device is Pixoo64 or similar.")
            print("LCD Independence set to 0, LCD Index set to 0, LCD Clock ID set to 625")
            return 0, 0, 625

        # If more then one LCD Independence is available, select one
        if len(lcd_independence_list) > 1:
            print("Select a LCD Group (Independence):")
            format_lcd_independence_list(lcd_independence_list)
            selected_lcd_independence = get_lcd_independence_selection(lcd_independence_list)
        else:
            selected_lcd_independence = 0

        lcd_list = lcd_independence_list[selected_lcd_independence].get('LcdList', [])

        if not lcd_list:
            print("LcdList is empty.")
            return None, None, None

        format_lcd_list(lcd_list)
        selected_lcd_index = get_lcd_selection(lcd_list)

        return (
            lcd_independence_list[selected_lcd_independence].get('LcdIndependence'),
            selected_lcd_index, # Return the actual index
            lcd_list[selected_lcd_index].get('LcdClockId')
        )
    except Exception as e:
        print(f'Error getting LCD list: {e}')
        return None, None, None