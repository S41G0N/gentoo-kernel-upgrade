#!/usr/bin/env python3

import os
import subprocess
import shutil
import multiprocessing

# Define constants for better readability and maintenance
LINUX_PATH = "/usr/src/linux"
CONFIG_FILE = ".config"
GRUB_CONFIG_PATH = "/boot/grub/grub.cfg"

def run_command(command):
    """Run a shell command and return the output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command failed: {command}\nError: {result.stderr}")
        exit(1)
    return result.stdout.strip()

def main():
    # Automatically determine the current and new kernel versions
    current_kernel = run_command("uname -r")
    new_kernel_version = run_command("eselect kernel list | tail -n 1 | awk -F'[- ]' '{print $(NF-1)\"-\"$NF}'")
    print(new_kernel_version)

    # Select the latest kernel version
    new_kernel_selection = run_command("eselect kernel list | tail -n 1 | awk -F'[][]' '{print $2}'")
    print(new_kernel_selection)

    # Check if the newest kernel has already been selected
    if '*' in new_kernel_selection:
        print("The newest kernel has already been selected.")
        exit(1)

    run_command(f"eselect kernel set {new_kernel_selection}")

    # Path adjustments
    new_kernel_path = f"{LINUX_PATH}-{new_kernel_version}"
    old_config_path = f"{LINUX_PATH}-{current_kernel}/{CONFIG_FILE}"
    new_config_path = f"{LINUX_PATH}/{CONFIG_FILE}"

    # Ensure the new kernel directory exists
    if not os.path.isdir(new_kernel_path):
        print(f"New kernel path '{new_kernel_path}' does not exist. Exiting.")
        exit(1)

    # Copy the old configuration to the new kernel path and prepare for building
    shutil.copy(old_config_path, new_config_path)
    os.chdir(LINUX_PATH)
    run_command("make olddefconfig")

    # Build the kernel with the number of parallel jobs equal to the number of CPUs
    num_jobs = multiprocessing.cpu_count()
    run_command(f"make -j{num_jobs} && make modules_install && make install")

    # Update the initial ramdisk and Grub configuration
    run_command(f"dracut --kver {new_kernel_version} --force")
    run_command(f"grub-mkconfig -o {GRUB_CONFIG_PATH}")

    print(f"Kernel update to version {new_kernel_version} completed successfully.")

if __name__ == "__main__":
    main()

