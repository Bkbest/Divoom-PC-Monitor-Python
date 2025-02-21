import psutil
import glob
import subprocess
import re
import platform
import json

def cpu_usage():
    # CPU usage as a percentage, rounded to the nearest integer
    cpu_usage = round(psutil.cpu_percent(interval=1))
    
    # CPU temperature, rounded to the nearest integer
    cpu_temp = cpu_temp_from_sensors()
    if cpu_temp is not None:
        cpu_temp = round(cpu_temp)
        
    return cpu_usage, cpu_temp

def cpu_temp_from_sensors():
    try:
        cpu_vendor = get_cpu_vendor()

        # Print CPU vendor
        print(f"CPU Vendor: {cpu_vendor}")
        
        if "AMD" in cpu_vendor.upper():  # Check for AMD
            # AMD CPU temperature (k10temp)
            result = subprocess.run(['sensors', '-j'], capture_output=True, text=True, check=True)
            sensors_json = json.loads(result.stdout)

            if "k10temp-pci-00c3" in sensors_json and "Tctl" in sensors_json["k10temp-pci-00c3"]:
                cpu_temp_str = sensors_json["k10temp-pci-00c3"]["Tctl"].get("temp1_input")
                cpu_temp = round(float(cpu_temp_str))
                return cpu_temp

        elif "Intel" in cpu_vendor or "x86_64" in cpu_vendor or "i" in cpu_vendor: # Check for Intel (more general)
            # Intel CPU temperature (coretemp or similar)
            result = subprocess.run(['sensors', '-j'], capture_output=True, text=True, check=True)
            sensors_json = json.loads(result.stdout)

            if "coretemp-isa-0000" in sensors_json and "Package id 0" in sensors_json["coretemp-isa-0000"]:
                cpu_temp_str = sensors_json["coretemp-isa-0000"]["Package id 0"].get("temp1_input")
                cpu_temp = round(float(cpu_temp_str))
                return cpu_temp
                
        else:
            print(f"Unknown CPU vendor! Trying generic method...")
            result = subprocess.run(["sensors"], capture_output=True, text=True, check=True)
            for line in result.stdout.splitlines():
                if 'Core 0' in line:  # More common intel identifier
                    match = re.search(r'([0-9]+\.[0-9]+)°C', line)
                    if match:
                        cpu_temp = float(match.group(1))
                        return cpu_temp

    except subprocess.CalledProcessError as e:
        print(f"Error running sensors: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
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
                        return vendor_id # Return the raw string if not Intel or AMD
            return None  # vendor_id not found

    except FileNotFoundError:
        return None  # /proc/cpuinfo not found
    except Exception as e: # Catch any other potential errors
        print(f"An error occurred: {e}")
        return None