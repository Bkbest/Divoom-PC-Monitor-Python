# Form JSON payloads based on the system information and send to the Divoom device

import json
import requests

def send_system_info(device_id, device_ip, lcd_independence, lcd_index, lcd_clock_id, cpu_util, cpu_temp, gpu_util, gpu_temp, mem_util, disk_util, verbose):
    # Send Select Clock to the Divoom Times Gate device
    post_info_clock = {
        "Command": "Channel/SetClockSelectId",
        "LcdIndependence": lcd_independence,
        "DeviceId": device_id,
        "LcdIndex": lcd_index,
        "ClockId": lcd_clock_id
    }

    param_info_clock = json.dumps(post_info_clock)

    if verbose:
        print(f"Select Clock Data to be sent: {param_info_clock}")

    # Send the HTTP POST request for setting the clock
    clock_response = requests.post(
        f"http://{device_ip}:80/post",
        data=param_info_clock,
        headers={"Content-Type": "application/json"}
    )
    print(f"Select Clock Response: {clock_response.text}")

    # Change lcd_index to integer
    lcd_index = int(lcd_index)
    
    # Define the Divoom device post structure for system information
    post_info_system = {
        "Command": "Device/UpdatePCParaInfo",
        "ScreenList": [
            {
                "LcdId": lcd_index,
                "DispData": [
                    f"{cpu_util}%",        # CPU Utilization as %
                    f"{gpu_util}%",        # GPU Utilization as %
                    f"{cpu_temp}°C",       # CPU Temperature as °C
                    f"{gpu_temp}°C",       # GPU Temperature as °C
                    f"{mem_util}%",        # Memory Utilization as %
                    f"{disk_util}%"        # Disk Utilization as %
                ]
            }
        ]
    }

    param_info_system = json.dumps(post_info_system, indent=2)
    
    if verbose:
        print(f"Data to be sent: {param_info_system}")

    # Send the HTTP POST request for system information
    system_response = requests.post(
        f"http://{device_ip}:80/post",
        data=param_info_system,
        headers={"Content-Type": "application/json"}
    )
    print(f"System Information Response: {system_response.text}")
