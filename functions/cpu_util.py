import json
import re
import subprocess

import psutil


def cpu_usage():
    usage_percent = round(psutil.cpu_percent(interval=1))

    # CPU temperature, rounded to the nearest integer
    temp_val = cpu_temp_from_sensors()
    if temp_val is not None:
        temp_val = round(temp_val)

    return usage_percent, temp_val


def cpu_temp_from_sensors():
    try:
        cpu_vendor = get_cpu_vendor()
        vendor_safe = (cpu_vendor or "").upper()

        # ---------------------------------------------------------
        # SHARED SENSOR FETCH (Run once for both Intel/AMD)
        # ---------------------------------------------------------
        if "AMD" in vendor_safe or "INTEL" in vendor_safe or "X86_64" in vendor_safe:
            result = subprocess.run(
                ["sensors", "-j"], capture_output=True, text=True, check=True
            )
            sensors_json = json.loads(result.stdout)
        else:
            sensors_json = {}

        # ---------------------------------------------------------
        # AMD LOGIC
        # ---------------------------------------------------------
        if "AMD" in vendor_safe:
            amd_sensor_data = {}
            for key in sensors_json:
                if key.startswith("k10temp"):
                    amd_sensor_data = sensors_json[key]
                    break

            # Tctl is the standard AMD temperature reading
            tctl_data = amd_sensor_data.get("Tctl", {})
            cpu_temp_str = tctl_data.get("temp1_input")

            if cpu_temp_str:
                return round(float(cpu_temp_str))

        # ---------------------------------------------------------
        # INTEL LOGIC
        # ---------------------------------------------------------
        elif "INTEL" in vendor_safe or "X86_64" in vendor_safe:
            intel_sensor_data = {}
            for key in sensors_json:
                if key.startswith("coretemp"):
                    intel_sensor_data = sensors_json[key]
                    break

            package_data = intel_sensor_data.get("Package id 0", {})
            cpu_temp_str = package_data.get("temp1_input")

            if cpu_temp_str:
                return round(float(cpu_temp_str))

        # ---------------------------------------------------------
        # FALLBACK LOGIC (Generic text parsing)
        # ---------------------------------------------------------
        print("Standard JSON parsing failed. Trying generic text method...")
        result = subprocess.run(["sensors"], capture_output=True, text=True, check=True)

        for line in result.stdout.splitlines():
            # Look for common identifiers
            if "Core 0" in line or "Package id 0" in line or "Tctl" in line:
                match = re.search(r"([0-9]+\.[0-9]+)", line)
                if match:
                    return float(match.group(1))

    except subprocess.CalledProcessError as e:
        print(f"Error running sensors command: {e}")
        return None

    except json.JSONDecodeError as e:
        print(f"Error parsing sensors JSON: {e}")
        return None

    # General catch-all MUST come last
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

    return None


def get_cpu_vendor():
    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                match = re.search(r"vendor_id\s*:\s*(.+)", line)
                if match:
                    vendor_id = match.group(1).strip()
                    if vendor_id.lower() == "genuineintel":
                        return "Intel"
                    elif vendor_id.lower() == "authenticamd":
                        return "AMD"
                    else:  # Handle other vendors if needed
                        return vendor_id
            return None  # vendor_id not found

    except FileNotFoundError:
        return None  # /proc/cpuinfo not found
    except Exception as e:  # Catch any other potential errors
        print(f"An error occurred detecting vendor: {e}")
        return None
