# Get user selection for device
def get_device_selection(devices):
    device_count = len(devices)
    while True:
        try:
            selection = int(input("Select a device: "))
            if 1 <= selection <= device_count:  # Use <= for upper bound
                return selection - 1  # Return the index (starting from 0)
            else:
                print("Invalid selection. Please enter a number within the range.")
        except ValueError:
            print("Invalid input. Please enter a number.")


# Get user selection for LCD Independence
def get_lcd_independence_selection(lcd_independences):
    lcd_independence_count = len(lcd_independences)
    while True:
        try:
            selection = int(input("Select an LCD Independence: "))
            if 1 <= selection <= lcd_independence_count:  # Use <= for upper bound
                return selection - 1  # Return the actual index
            else:
                print("Invalid selection. Please enter a number within the range.")
        except ValueError:
            print("Invalid input. Please enter a number.")


# Get user selection for LCD
def get_lcd_selection(lcds):
    lcd_count = len(lcds)
    while True:
        try:
            selection = int(input("Select an LCD: "))
            if 1 <= selection <= lcd_count:  # Use <= for upper bound
                return selection - 1  # Return the actual index
            else:
                print("Invalid selection. Please enter a number within the range.")
        except ValueError:
            print("Invalid input. Please enter a number.")


# Get user selection for drive
def get_drive_selection(drives):
    drive_count = len(drives)
    while True:
        user_input = input("Select a drive (type all for all drives): ").lower()
        if user_input == "all":
            return "*"

        try:
            selection = int(user_input)
            if 1 <= selection <= drive_count:  # Use <= for upper bound check
                return selection - 1  # Return the index (starting from 0)
            else:
                print(
                    "Invalid selection. Please enter a number within the range or 'all'."
                )
        except ValueError:
            print('Invalid input. Please enter a number or "all".')
