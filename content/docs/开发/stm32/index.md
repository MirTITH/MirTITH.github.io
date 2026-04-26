---
title: STM32 开发环境
type: docs
---

## STM32CubeMX

### 安装

在 ST 官网下载安装 STM32CubeMX。

### 创建快捷方式

1. 从 CubeMX 安装目录中取出 `STM32CubeMX/help/STM32CubeMX.ico`，转换成同名 PNG 图标；或者自行准备一个 PNG 图标
2. 修改 [CubeMX.desktop](CubeMX.desktop) 中的 `Exec` 和 `Icon` 路径
3. 注册 `.ioc` 文件类型并安装 desktop file：

   ```bash
   xdg-mime install --mode user cubemx-ioc.xml
   desktop-file-install --dir=$HOME/.local/share/applications/ CubeMX.desktop
   ```

这样程序菜单中会出现 CubeMX，双击 `.ioc` 文件时也能直接用 CubeMX 打开。

### 相关文件

- [CubeMX.desktop](CubeMX.desktop)
- [cubemx-ioc.xml](cubemx-ioc.xml)

## Arm GNU Toolchain

### 推荐：xPack 预编译工具链

1. 从这里下载安装包：<https://github.com/xpack-dev-tools/arm-none-eabi-gcc-xpack/releases/>

   不建议直接使用 Arm 官网某些版本的安装包，旧经验里它们更容易遇到依赖和 Python 版本问题。

2. 解压到 `~/.local/xPacks/arm-none-eabi-gcc`：

   ```shell
   mkdir -p ~/.local/xPacks/arm-none-eabi-gcc
   cd ~/.local/xPacks/arm-none-eabi-gcc
   tar xvf <下载的安装包路径>

   chmod -R -w <解压后的文件夹>

   cd <解压后的文件夹>/bin
   ./arm-none-eabi-gcc -v
   ./arm-none-eabi-gdb -v
   ```

3. 如有需要，可把工具链链接到 `~/.local/bin`：

   ```shell
   ln -s <解压后的文件夹绝对路径>/bin/* ~/.local/bin
   ```

### Debian / Ubuntu 可选脚本

如果你更想把官方工具链打成一个本地 `.deb` 再安装，可以参考 [install-gcc-arm-none-eabi.sh](install-gcc-arm-none-eabi.sh)。

> 这个脚本是旧版示例，里面的版本号和下载地址可能已经过时，使用前请先更新变量。