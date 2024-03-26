#!/bin/bash

# Define constants for better readability and maintenance -> adjust if your system is different
LINUX_PATH=/usr/src/linux
CONFIG_FILE=".config"
GRUB_CONFIG_PATH=/boot/grub/grub.cfg

# Automatically determine the current and new kernel versions
CURRENT_KERNEL=$(uname -r)
NEW_KERNEL_VERSION=$(eselect kernel list | tail -n 1 | awk -F'[- ]' '{print $(NF-1)"-"$NF}')

# Select the latest kernel version
NEW_KERNEL_SELECTION=$(eselect kernel list | tail -n 1 | awk -F'[][]' '{print $2}')
eselect kernel set $NEW_KERNEL_SELECTION

# Path adjustments
NEW_KERNEL_PATH="${LINUX_PATH}-${NEW_KERNEL_VERSION}"
OLD_CONFIG_PATH="${LINUX_PATH}-${CURRENT_KERNEL}/${CONFIG_FILE}"
NEW_CONFIG_PATH="${LINUX_PATH}/${CONFIG_FILE}"

# Ensure the new kernel directory exists
if [ ! -d "$NEW_KERNEL_PATH" ]; then
    echo "New kernel path '$NEW_KERNEL_PATH' does not exist. Exiting."
    exit 1
fi

# Copy the old configuration to the new kernel path and prepare for building
cp "$OLD_CONFIG_PATH" "$NEW_CONFIG_PATH"
cd $LINUX_PATH || exit
make olddefconfig

# Build the kernel with the number of parallel jobs equal to the number of CPUs
NUM_JOBS=$(nproc)
make -j"$NUM_JOBS" && make modules_install && make install

# Update the initial ramdisk and Grub configuration
dracut --kver $NEW_KERNEL_VERSION
grub-mkconfig -o "$GRUB_CONFIG_PATH"

echo "Kernel update to version $NEW_KERNEL_VERSION completed successfully."

