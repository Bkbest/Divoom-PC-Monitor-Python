import json
import subprocess

from functions.format_list import format_drive_list
from functions.get_selection import get_drive_selection


def get_os_drives():
    # Run iostat command and capture JSON output
    result = subprocess.run(
        ["iostat", "-dxy", "2", "1", "-o", "JSON"], capture_output=True, text=True
    )

    # Parse JSON to get disk devices, excluding any with "ram" in the name
    disks = []
    if result.returncode == 0:
        iostat_data = json.loads(result.stdout)
        disks = [
            disk["disk_device"]
            for disk in iostat_data["sysstat"]["hosts"][0]["statistics"][0]["disk"]
            if "ram" not in disk["disk_device"]
        ]

    drive_list = format_drive_list(disks)
    selected_drive = get_drive_selection(drive_list)
    if selected_drive == "*":
        return disks
    else:
        return disks[selected_drive]

    return disks
