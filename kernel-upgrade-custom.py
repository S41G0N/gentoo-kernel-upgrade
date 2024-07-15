#!/usr/bin/env python3
import os
import subprocess
import shutil
import multiprocessing
import argparse
import logging
from typing import List, Tuple

# Define constants
LINUX_PATH = "/usr/src/linux"
CONFIG_FILE = ".config"
GRUB_CONFIG_PATH = "/boot/grub/grub.cfg"

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_command(command: str) -> None:
    """Run a shell command and log the output in real-time."""
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    for stream in [process.stdout, process.stderr]:
        if stream:
            for line in iter(stream.readline, ""):
                logging.info(line.strip())
            stream.close()
    returncode = process.wait()
    if returncode != 0:
        raise subprocess.CalledProcessError(returncode, command)

def get_command_output(command: str) -> str:
    """Run a shell command and return the output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
    return result.stdout.strip()

def backup_old_kernel(current_kernel: str) -> None:
    """Backup the old kernel and configuration."""
    old_kernel_path = f"{LINUX_PATH}-{current_kernel}"
    backup_path = f"{old_kernel_path}.backup"
    if os.path.exists(old_kernel_path):
        shutil.copytree(old_kernel_path, backup_path)
        logging.info(f"Backed up old kernel to {backup_path}")

def main(args: argparse.Namespace) -> None:
    current_kernel = get_command_output("uname -r")
    logging.info(f"Current kernel version: {current_kernel}")

    new_kernel_number = get_command_output(
        "eselect kernel list | tail -n 1 | awk -F'[][]' '{print $2}'"
    )
    new_kernel_version = get_command_output("eselect kernel list | tail -n 1").split("-", 1)[1]
    if '*' in new_kernel_version:
        new_kernel_version = new_kernel_version.split(' ')[0]
    
    logging.info(f"New kernel number: {new_kernel_number}")
    logging.info(f"New kernel version: {new_kernel_version}")

    if args.backup:
        backup_old_kernel(current_kernel)

    try:
        run_command(f"eselect kernel set {new_kernel_number}")
        logging.info("New kernel version symlinked")

        new_kernel_path = f"{LINUX_PATH}-{new_kernel_version}"
        old_config_path = f"{LINUX_PATH}-{current_kernel}/{CONFIG_FILE}"
        new_config_path = f"{LINUX_PATH}/{CONFIG_FILE}"

        if not os.path.isdir(new_kernel_path):
            raise FileNotFoundError(f"New kernel path '{new_kernel_path}' does not exist.")

        shutil.copy(old_config_path, new_config_path)
        os.chdir(LINUX_PATH)
        run_command("make olddefconfig")

        num_jobs = multiprocessing.cpu_count()
        run_command(f"make -j{num_jobs} && make modules_install && make install")

        run_command(f"dracut --kver {new_kernel_version} --force")
        run_command(f"grub-mkconfig -o {GRUB_CONFIG_PATH}")

        logging.info(f"Kernel update to version {new_kernel_version} completed successfully.")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gentoo Kernel Upgrade Script")
    parser.add_argument('--backup', action='store_true', help='Backup the old kernel before upgrading')
    args = parser.parse_args()

    setup_logging()
    main(args)
