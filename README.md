# Divoom PC Monitor Python - Implementation for Linux Systems

This repository contains the Python code that interfaces with the Divoom PC Monitor application on the Divoom Times Gate or Divoom Pixoo64 to monitor system information for Linux systems.

## Overview

This project is a Python implementation of the Divoom PC Monitor originally written in C# by DivoomDevelop. It allows users to monitor various system metrics and display them on their Divoom Times Gate or Divoom Pixoo64.

## Features

- **System Metrics Displayed**:
   - CPU usage percentage
   - CPU temperature
   - RAM usage
   - GPU usage (NVIDIA, AMD, and Intel via `nvtop`)
   - GPU temperature (NVIDIA, AMD, and Intel via `nvtop`)
   - HDD usage (dynamic drive selection based on highest usage)
- **Easy Setup**: Configuration script simplifies the setup process.
- **Scheduled Task Support**: Users can copy the SystemD config files for easy systemctl support.

## Requirements

The project needs both Python packages and a few Linux command-line tools that are called directly by the scripts.

### Hardware and network

- A Divoom Times Gate or Pixoo64 on the same LAN as the Linux host
- Internet access during `divoom_setup.py` so the script can query Divoom cloud endpoints
- A Linux system with Python 3

### Python packages

Install the Python dependencies with:

```bash
pip install -r requirements.txt
```

This installs:

- `psutil`
- `requests`

### Required Linux packages / binaries

These binaries are used directly by the code and should be installed before running setup or the monitor loop:

- `lspci` from `pciutils`
   Used by `functions/gpu_util.py` to detect whether the GPU is NVIDIA, AMD, or Intel.
- `sensors` from `lm-sensors`
   Used by `functions/cpu_util.py` to read CPU temperatures.
- `iostat` from `sysstat`
   Used by `functions/get_os_drives.py` during setup and by `functions/hdd_util.py` during every monitor update.

Example installs for the common required packages:

```bash
# Fedora
sudo dnf install pciutils lm_sensors sysstat

# Debian / Ubuntu
sudo apt install pciutils lm-sensors sysstat

# Arch Linux
sudo pacman -S pciutils lm_sensors sysstat
```

### GPU vendor-specific requirements

- NVIDIA GPUs: `nvidia-smi`
   Usually provided by the installed NVIDIA driver package.
- AMD GPUs: `rocm-smi`
   Usually provided by ROCm or the distro package that ships the ROCm SMI utility.
- Intel GPUs: `nvtop`
   This project currently uses `nvtop -s` to collect Intel GPU usage and temperature.

Example installs for vendor-specific GPU tooling:

```bash
# Fedora - Intel
sudo dnf install nvtop

# Debian / Ubuntu - Intel
sudo apt install nvtop

# Arch Linux - Intel
sudo pacman -S nvtop
```

`nvtop` is now resolved from your `PATH`, so it does not need to live at `/usr/bin/nvtop`.

For NVIDIA and AMD, the exact package name for `nvidia-smi` or `rocm-smi` depends on how your driver stack is installed on your distro.

### Optional system software

- `systemd`
   Only required if you want to run the monitor as a service with the provided unit files.

## Usage

1. **Configuration**: 
   - Run `divoom_setup.py` to create the necessary configuration file and established the Divoom PC Monitor app on a LCD face.
   
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

   ⚠️ **Attention:** If the PC Monitor app (625) is currently displayed on a 'LCD face', the setup output will include 'Divoom PC Monitor'.  This message doesn't restrict which 'LCD face' you can ultimately use; the app can be assigned to any face regardless of its initial state.

3. Execute main monitor:
   ```bash
   python divoom_pc_monitor.py -i 10 -v
   ```

4. (Optional) Setup SystemD service by copying the distro associated service file:
   ```bash
   cp /systemd-configs/<DISTRO>/divoom_monitor.service  /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable divoom_monitor.service
   sudo systemctl start divoom_monitor.service
   ```

## Work In Progress

1. Intel GPU support currently depends on `nvtop` and the underlying Linux driver/kernel stack, so behavior may vary by device and distro.
2. An on-going bug hunt and optimization. User contributions/recommendations are welcome.

## Author

This project was created by Keith Carichner Jr. due to the lack of a competent implementation that actually functioned and was well-written/documented.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
