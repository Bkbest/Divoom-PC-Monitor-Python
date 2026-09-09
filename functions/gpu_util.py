import json
import re
import shutil
import subprocess


def get_gpu_info():
    try:
        result = subprocess.run(
            ["lspci", "-nnk"], capture_output=True, text=True, check=True
        )
        output = result.stdout

        # Match VGA or 3D controller lines and extract vendor and model
        match = re.search(
            r"(VGA|3D) compatible controller.*?: (.*?) \[(....):(.*?)\]", output
        )
        if match:
            vendor_id = match.group(3)
            model = match.group(2).strip()

            # Determine vendor based on ID
            if vendor_id == "10de":
                vendor = "NVIDIA"
            elif vendor_id == "1002":
                vendor = "AMD"
            elif vendor_id == "8086":
                vendor = "Intel"
            else:
                vendor = "Unknown"  # Handle other vendors if needed

            return vendor, model
        else:
            return None, None

    except (FileNotFoundError, subprocess.CalledProcessError):
        return None, None


def gpu_usage():
    vendor, model = get_gpu_info()

    # Print GPU vendor and model
    print(f"GPU Vendor: {vendor}, Model: {model}")

    if vendor == "NVIDIA":
        try:
            # Run the nvidia-smi command
            result = subprocess.run(
                [
                    "nvidia-smi",
                    "--query-gpu=utilization.gpu,temperature.gpu",
                    "--format=csv,noheader,nounits",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            # Parse the output
            output = result.stdout.strip().split(", ")
            gpu_util = int(output[0])  # GPU utilization percentage
            gpu_temp = int(output[1])  # GPU temperature in Celsius

            return gpu_util, gpu_temp

        except (subprocess.CalledProcessError, ValueError, IndexError) as e:
            print(f"Error running nvidia-smi or parsing output: {e}")
            return None, None

    elif vendor == "AMD":
        try:
            # Run the rocm-smi command
            result = subprocess.run(
                ["rocm-smi", "--showuse", "--showtemp", "--json"],
                capture_output=True,
                text=True,
                check=True,
            )

            # Parse the output
            json_data = json.loads(result.stdout)

            gpu_temp_str = json_data["card0"]["Temperature (Sensor edge) (C)"]
            gpu_util_str = json_data["card0"]["GPU use (%)"]

            # Convert to float, then round, then convert to int
            gpu_temp = round(float(gpu_temp_str))
            gpu_util = round(float(gpu_util_str))

            return gpu_util, gpu_temp

        except (subprocess.CalledProcessError, ValueError, KeyError) as e:
            print(f"Error running rocm-smi or parsing output: {e}")
            return None, None

    # Requires the 'nvtop' command to be installed and available in the system PATH
    elif vendor == "Intel":
        try:
            nvtop_path = shutil.which("nvtop")
            if not nvtop_path:
                raise FileNotFoundError("nvtop was not found in PATH")

            # Run the nvtop command and capture the JSON output
            result = subprocess.run(
                [nvtop_path, "-s"],
                capture_output=True,
                text=True,
                check=True,
            )

            # Parse the output
            json_data = json.loads(result.stdout)

            if not json_data:
                return None, None
            
            # Target the first GPU returned in the list
            gpu_data = json_data[0]

            # Use 'or' to fallback to default strings if the JSON value is null/None
            gpu_util_raw = gpu_data.get("gpu_util") or "0%"
            gpu_temp_raw = gpu_data.get("temp") or "0C"

            # Extract the strings and strip the '%' and 'C' units before casting to int
            gpu_util_str = gpu_util_raw.replace("%", "")
            gpu_temp_str = gpu_temp_raw.replace("C", "")

            gpu_util = int(gpu_util_str)
            gpu_temp = int(gpu_temp_str)

            return gpu_util, gpu_temp

        except (subprocess.CalledProcessError, json.JSONDecodeError, ValueError, IndexError, FileNotFoundError) as e:
            print(f"Error running nvtop or parsing output: {e}")
            return None, None

    else:
        return None, None  # Unknown or unsupported vendor


def gpu_main():
    gpu_util, gpu_temp = gpu_usage()
    return gpu_util, gpu_temp