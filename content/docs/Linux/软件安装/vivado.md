---
title: Vivado
type: docs
---

## For Arch Linux

1. 安装依赖库
```bash
paru -S ncurses5-compat-libs  libxcrypt-compat  libpng12  lib32-libpng12  gtk3  inetutils  xorg-xlsclients  cpio
```

2. 在Vivado官网下载安装脚本并运行
```bash
chmod +x FPGA_*.bin
./ FPGA_*.bin
```