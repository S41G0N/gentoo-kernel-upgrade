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
    """Run a shell command and print the output in real-time."""
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    if process.stdout:
        for line in iter(process.stdout.readline, ""):
            print(line, end="")
        process.stdout.close()

    if process.stderr:
        for line in iter(process.stderr.readline, ""):
            print(line, end="")
        process.stderr.close()

    returncode = process.wait()
    if returncode != 0:
        print(f"Command failed: {command}")
        exit(1)


def get_command_output(command):
    """Run a shell command and return the output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command failed: {command}\nError: {result.stderr}")
        exit(1)
    return result.stdout.strip()


def main():
    # Automatically determine the current and new kernel versions
    current_kernel = get_command_output("uname -r")
    print(f"CURRENT KERNEL VERSION: {current_kernel}")

    # Get latest kernel number
    new_kernel_number = get_command_output(
        "eselect kernel list | tail -n 1 | awk -F'[][]' '{print $2}'"
    )
    print(f"NEW KERNEL NUMBER: {new_kernel_number}")

    #Get latest kernel version
    new_kernel_version = (
        get_command_output("eselect kernel list | tail -n 1").split("-", 1)[1]
    )

    if '*' in new_kernel_version:
        new_kernel_version = new_kernel_version.split(' ')[0]

    print(f"NEW KERNEL VERSION: {new_kernel_version}")

    run_command(f"eselect kernel set {new_kernel_number}")
    print("NEW KERNEL VERSION SYMLINKED")

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
