#!/bin/bash
## Path to the script you want to manage
SCRIPT_NAME="kernel-upgrade-custom.sh"
TARGET_DIR="/usr/local/bin"
TARGET_PATH="${TARGET_DIR}/${SCRIPT_NAME}"

# Function to install the script
install_script() {
    if [ -f "$SCRIPT_NAME" ]; then
        if [ ! -f "$TARGET_PATH" ]; then
            cp "$SCRIPT_NAME" "$TARGET_PATH"
            chmod +x "$TARGET_PATH"
            echo "Script installed successfully into '$TARGET_PATH'"
        else
            echo "Error: Script is already installed."
        fi
    else
        echo "Error: Script '$SCRIPT_NAME' does not exist."
    fi
}

# Function to uninstall the script
uninstall_script() {
    if [ -f "$TARGET_PATH" ]; then
        rm "$TARGET_PATH"
        echo "Script uninstalled successfully from '$TARGET_PATH'"
    else
        echo "Error: Script is not installed."
    fi
}

# Main script logic
case "$1" in
    install)
        install_script
        ;;
    uninstall)
        uninstall_script
        ;;
    *)
        echo "Usage: $0 {install|uninstall}"
        exit 1
        ;;
esac

