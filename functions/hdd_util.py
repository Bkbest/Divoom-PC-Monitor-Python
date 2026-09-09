import json
import subprocess


def hdd_usage(hard_drive_list):
    # Run iostat command and capture JSON output
    command = ["iostat", "-dxy", "2", "1", "-o", "JSON"]
    result = subprocess.run(command, capture_output=True, text=True)

    # Parse the JSON output
    iostat_data = json.loads(result.stdout)

    # Extract the disk utilization values
    disks = iostat_data["sysstat"]["hosts"][0]["statistics"][0]["disk"]

    # Variables to store the disk with the highest utilization
    highest_util = 0
    highest_disk = None

    for disk in disks:
        disk_name = disk["disk_device"]
        # Check if the disk name is in the hard_drive_list and exclude "ram" devices
        if disk_name in hard_drive_list and "ram" not in disk_name:
            util = disk["util"]
            # Update highest_disk and highest_util if this disk has a higher utilization
            if util > highest_util:
                highest_util = util
                highest_disk = disk_name

    # Round the highest utilization
    rounded_util = round(highest_util)

    return highest_disk, rounded_util
