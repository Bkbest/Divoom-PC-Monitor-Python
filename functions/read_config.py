import configparser


def read_config():
    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Read the config file
    config.read("config.env")

    # Accessing variables from the config file
    device_id = config["DEFAULT"]["device_id"]
    device_ip = config["DEFAULT"]["device_ip"]
    lcd_independence = config["DEFAULT"]["lcd_independence"]
    lcd_index = config["DEFAULT"]["lcd_index"]
    lcd_clock_id = config["DEFAULT"]["lcd_clock_id"]
    hard_drive = config["DEFAULT"]["hard_drive"].split(
        ","
    )  # Assuming hard_drive is a comma-separated string in the file

    # Remove any leading/trailing whitespace from each item in the list
    hard_drive = [item.strip() for item in hard_drive]

    return device_id, device_ip, lcd_independence, lcd_index, lcd_clock_id, hard_drive
