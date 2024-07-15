# Gentoo Kernel Upgrade Script

![Upgrade Script Demo](img/kernel-upgrade.gif)

## Introduction

This script streamlines the process of manually upgrading your kernel in Gentoo Linux. It's designed for users who prefer to compile their kernel separately from system updates, rather than automatically during `emerge -avuDN @world`.

## Target Audience

This tool is ideal for Gentoo users who:
- Build their kernel from source using `sys-kernel/gentoo-sources`
- Prefer manual control over kernel compilation timing
- Want to simplify the kernel upgrade process

**Note:** This script is not intended for use with `genkernel` or distribution kernels.

## Prerequisites

- GRUB Bootloader (config path: `/boot/grub/grub.cfg`)
- Dracut initramfs generator

## How to Install & Run

```bash
git clone https://gitlab.com/SA1G0N/gentoo-kernel-upgrade-script.git
cd gentoo-kernel-upgrade-script
sudo sh install.sh
sudo kernel-upgrade-custom.py
```
