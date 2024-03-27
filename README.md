# Gentoo Kernel Upgrade Script


## Why was this script created

This script was written to simplify the process of manually upgrading your kernel in Gentoo Linux.

It only applies to those who have built their kernel from source using "sys-kernel/gentoo-sources", any other kernels such as "genkernel" or distribution kernels should not be used with this script.

## Requirements
* GRUB Bootloader (config path set to "/boot/grub/grub.cfg")
* Dracut initramfs generator

## How to use

```
git clone https://gitlab.com/SA1G0N/gentoo-kernel-upgrade-script.git
cd gentoo-kernel-upgrade-script
sudo sh kernel-upgrade.sh
```

