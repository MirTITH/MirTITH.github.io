---
title: 使用 Rust 进行 ESP32 开发
type: docs
---

## Rustup 安装

使用 Rust 进行 ESP32 开发前，首先需要安装 Rustup 来管理 `cargo`、Rust 编译器和工具链。可以直接使用包管理器安装，例如：

```shell
paru -S rustup
```

也可以从官网获取其他安装方式：<https://rust-lang.org/zh-CN/learn/get-started/>

## 安装其他 Rust 编译器

完成上一步后，通常会自动安装适用于本机的最新稳定版 Rust。如果需要安装特定版本，可以用 Rustup 安装，例如 nightly：

```shell
rustup install nightly
```

ESP32 常见架构主要分为 Xtensa 和 RISC-V，两者的交叉编译工具链安装方式不同。

### RISC-V 架构

对于 RISC-V 架构的 ESP32 芯片，可以直接使用 Rustup 安装目标：

```shell
rustup target add riscv32imc-unknown-none-elf
```

某些更新型号可能需要改用 `riscv32imac-unknown-none-elf` 等目标三元组。

### Xtensa 架构

Rust 官方暂未直接支持 Xtensa，因此通常使用乐鑫的 `espup` 工具安装交叉编译工具链。

先安装 `espup`：

```shell
cargo install espup
```

然后执行：

```shell
espup install
```

安装完成后，`espup` 会生成环境变量脚本（通常是 `~/export-esp.sh`）。按脚本说明把环境变量接入你使用的 shell。可以用下面的命令验证是否配置成功：

```shell
xtensa-esp32-elf-gcc --version
echo $LIBCLANG_PATH
```

## 安装开发工具

使用 Cargo 安装模板工程生成工具 `esp-generate` 和烧录工具 `espflash`：

```shell
cargo install esp-generate espflash
```

## 其他工具

### Wokwi 仿真器

Wokwi 的 VS Code 扩展可以在本地开发环境中进行 ESP32 仿真。扩展市场页面：<https://marketplace.visualstudio.com/items?itemName=Wokwi.wokwi-vscode>

安装后按提示登录账号并填写 License Key，即可启用仿真功能。