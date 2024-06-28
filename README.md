# Gentoo Kernel Upgrade Script

![Upgrade Script GIF](img/kernel-upgrade.gif)


## Why was this script created

This script was written to simplify the process of manually upgrading your kernel in Gentoo Linux.
It should be useful to those who do not want to compile their kernel automatically during system updates via 'emerge -avuDN @world',
but would rather reserve the ability to compile their kernel later.

It only applies to those who have built their kernel from source using "sys-kernel/gentoo-sources", any other kernels such as "genkernel" or distribution kernels should not be used with this script.

## Requirements
* GRUB Bootloader (config path set to "/boot/grub/grub.cfg")
* Dracut initramfs generator

## How to use

```
git clone https://gitlab.com/SA1G0N/gentoo-kernel-upgrade-script.git
cd gentoo-kernel-upgrade-script
sudo sh install.sh
sudo kernel-upgrade-custom.py
```
