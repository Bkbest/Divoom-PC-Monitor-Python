# Format the device json and output
def format_device_list(devices):
    for index, device in enumerate(devices):
        print(f'Device {index + 1}:') # Show index starting from 1
        print(f'---------')
        print(f'Device Name: {device.get("DeviceName")}')
        print(f'Device ID: {device.get("DeviceId")}')
        print(f'Private IP: {device.get("DevicePrivateIP")}')
        print(f'MAC Address: {device.get("DeviceMac")}')
        print(f'Hardware Version: {device.get("Hardware")}')
        print()

# Format the LCD json and output
def format_lcd_list(lcds):
    for index, lcd in enumerate(lcds):
        print(f'LCD {index + 1}:')  # Use enumerate for correct index, starting from 1
        print(f'------')
        print(f'Clock ID: {lcd.get("LcdClockId")}') # Removed LcdSelectIndex, no longer needed
        if lcd.get("LcdClockId") == 625:
            print("Divoom PC Monitor")
        print(f'Image Pixel ID: {lcd.get("ClockImagePixelId")}')
        print()


# Format the drive list and output
def format_drive_list(drives):
    for index, drive in enumerate(drives):
        print(f'Drive {index + 1}:')  # Start index from 1 for user display
        print(f'--------')
        print(drive)
        print()