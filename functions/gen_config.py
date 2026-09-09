def generate_config_file(
    device_id, device_ip, lcd_independence, lcd_index, lcd_clock_id, hard_drive
):
    config = {
        "device_id": device_id,
        "device_ip": device_ip,
        "lcd_independence": lcd_independence,
        "lcd_index": lcd_index,
        "lcd_clock_id": lcd_clock_id,
        "hard_drive": ",".join(
            hard_drive
        ),  # Join hard_drive list into a comma-separated string
    }

    with open("config.env", "w") as file:
        try:
            file.write("[DEFAULT]\n")  # Add the section header at the top
            for key, value in config.items():
                file.write(f"{key}={value}\n")
            print("Configuration file generated successfully.")
        except Exception as e:
            print(f"Error: {e}")
