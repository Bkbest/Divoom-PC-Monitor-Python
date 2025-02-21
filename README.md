# Divoom PC Monitor Python - Python Implementation for Linux Systems

This repository contains the Python code that interfaces with the Divoom PC Monitor application on the Divoom Times Gate to monitor system information for Linux systems.

## Overview

This project is a Python implementation of the Divoom PC Monitor originally written in C# by DivoomDevelop. It allows users to monitor various system metrics and display them on their Divoom Times Gate.

## Features

- **System Metrics Displayed**: 
  - CPU usage percentage
  - CPU temperature
  - RAM usage
  - GPU usage (NVIDIA & AMD)
  - GPU temperature (NVIDIA & AMD)
  - HDD usage (dynamic drive selection based on highest usage)
- **Easy Setup**: Configuration script simplifies the setup process.
- **Scheduled Task Support**: Users can copy the SystemD config files for easy systemctl support.

## Usage

1. **Configuration**: 
   - Run `divoom_setup.py` to create the necessary configuration file.
   
2. **Running the Script**:
   - Execute `divoom_pc_monitor.py`
   - The following arguments are accepted:
   ``` bash
    usage: divoom_pc_monitor.py [-h] [-i INTERVAL_IN_SECONDS] [-v]

    DivoomPCMonitor.py - Monitor system information on a Divoom Times Gate device

    options:
    -h, --help            show this help message and exit
    -i, --interval_in_seconds INTERVAL_IN_SECONDS
                            Interval in seconds to update the system information (default: 30)
    -v, --verbose         Display verbose output on the console
    ```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/KallanX/Divoom-PC-Monitor-Python.git
   cd Divoom-PC-Monitor-Python
   ```

2. Run the setup:
   ```bash
   python divoom_setup.py
   ```

   ⚠️ **Attention:** Be sure to set the PC Monitor app to the desired device LCD before running the setup script via the Divoom app. During the setup script, select the LCD with the Device ID of 625.

3. Execute main monitor:
   ```bash
   python divoom_pc_monitor.py -i 10 -v
   ```

4. (Optional) Setup SystemD service by coping the OS associated service file:
   ```bash
   cd /systemd-configs/<OS>/divoom_monitor.service  /etc/systemd/system/
   ```

## Author

This project was created by Keith Carichner Jr. due to the lack of a competent implementation that actually functioned and was well-written/documented.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
