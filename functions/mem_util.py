# Get RAM usage via psutil

import psutil


def mem_usage():
    # Get memory usage statistics
    mem = psutil.virtual_memory()

    # Calculate memory utilization percentage
    mem_util = round(mem.percent)

    return mem_util
