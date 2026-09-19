---
title: "解决 Isaac Sim 5.1 在新 NVIDIA 驱动下的 RTX 启动崩溃"
type: docs
date: 2026-09-19T16:00:00+08:00
draft: false
---

Isaac Sim 5.1.0 在部分新 NVIDIA 驱动下可能在 RTX 初始化阶段崩溃，涉及 `librtx.scenedb.plugin.so`。本文提供一个 Vulkan Profiles 兼容工具包，通过调整驱动报告的内存分配上限，绕过这一兼容性问题，无需降级驱动或自行编译。

<!--more-->

## 适用环境

预编译工具包面向 **Ubuntu 22.04 x86_64 + Isaac Sim 5.1.0**。以下组合已完成启动验证：

| 项目 | 测试环境 |
| --- | --- |
| 系统 | Ubuntu 22.04 x86_64 |
| 显卡 | NVIDIA GeForce RTX 4070 Ti SUPER |
| NVIDIA 驱动 | 610.57.04 |
| Isaac Sim | 5.1.0 |
| Vulkan Profiles 层 | v1.4.341，使用 Ubuntu 22.04 工具链编译 |

该方案针对下文所述的 Vulkan 属性兼容性问题，不适用于所有 RTX 崩溃，也不处理 ROS 环境或端口冲突。预编译库不保证适用于 ARM、Windows 或不同 glibc 环境。

## 下载与启动

下载 [完整兼容工具包](isaac-sim-rtx-compat-ubuntu22.04-x86_64.tar.gz)，在下载目录打开终端并解压：

```bash
tar -xzf isaac-sim-rtx-compat-ubuntu22.04-x86_64.tar.gz
```

将以下所有命令中的 **`/path/to/isaacsim-5.1.0` 替换为你的 Isaac Sim 安装目录**，该目录应包含 `isaac-sim.sh` 和 `kit/`。命令均在解压目录的上一级执行，路径两侧的引号请保留。

```bash
bash isaac-sim-rtx-compat/launch.sh "/path/to/isaacsim-5.1.0"
```

无窗口启动时追加 `--no-window`：

```bash
bash isaac-sim-rtx-compat/launch.sh "/path/to/isaacsim-5.1.0" --no-window
```

工具包使用 Isaac Sim 自带的 Python，无需安装额外 Python 包。启动脚本会先配置兼容环境，再调用安装目录中的 `isaac-sim.sh`，保留原有 ROS 环境设置和启动参数，不覆盖安装文件。

请保留完整的解压目录，以后仍通过 `launch.sh` 启动。直接运行原版 `isaac-sim.sh` 不会自动使用此工具包。

### 工具包内容

```text
isaac-sim-rtx-compat/
├── launch.sh
├── isaacsim_rtx_compat.py
├── README.txt
├── THIRD_PARTY_NOTICES.txt
├── licenses/
└── tools/
    └── vulkan_profiles/
        └── libVkLayer_khronos_profiles.so
```

以下资源可单独查看；实际使用推荐下载完整压缩包，以保留目录结构和文件权限：

- [启动脚本](isaac-sim-rtx-compat/launch.sh)与[兼容模块](isaac-sim-rtx-compat/isaacsim_rtx_compat.py)
- [预编译 Vulkan Profiles 库](isaac-sim-rtx-compat/tools/vulkan_profiles/libVkLayer_khronos_profiles.so)
- [使用说明](isaac-sim-rtx-compat/README.txt)与[第三方版权说明](isaac-sim-rtx-compat/THIRD_PARTY_NOTICES.txt)
- [Apache 2.0 许可证](isaac-sim-rtx-compat/licenses/Apache-2.0.txt)
- [SHA-256 校验清单](SHA256SUMS.txt)

将校验清单下载到压缩包所在目录，解压后可执行 `sha256sum -c SHA256SUMS.txt` 检查文件完整性。

## 问题原因

在上述测试环境中，Vulkan 返回了以下属性值：

```text
VkPhysicalDeviceMaintenance3Properties.maxMemoryAllocationSize
= 0xffffffffffffffff
= UINT64_MAX
```

该属性表示单次内存分配大小上限。新驱动报告的值与 Isaac Sim 5.1 的 RTX 初始化路径存在兼容性问题，可能导致 `librtx.scenedb.plugin.so` 段错误。社区 [Issue #568](https://github.com/isaac-sim/IsaacSim/issues/568) 记录了相关问题与规避方式。

兼容模块在 Kit 创建 Vulkan 实例之前加载 Khronos Vulkan Profiles 层，将该属性覆盖为不超过以下数值：

```text
4 GiB - 2 MiB = 4292870144 bytes
```

这调整的是应用查询到的单次分配上限，并不意味着将显卡总显存限制为 4 GiB。

### 自动检测逻辑

默认情况下，兼容模块在以下条件同时满足时启用覆盖：

1. 设备厂商为 NVIDIA。
2. 按 NVIDIA Vulkan 编码解析的驱动版本大于 `(590, 48, 1, 0)`。
3. `maxMemoryAllocationSize` 大于 `4 GiB - 2 MiB`。

版本号是模块采用的判断阈值，不代表所有高于该版本的驱动都会崩溃。模块还会参考设备本地显存堆大小，取符合条件的设备候选上限中的最小值，并按 256 字节向下对齐。

兼容层通过 `SIMULATE_PROPERTIES_BIT` 模拟属性，不修改系统驱动。生成的 profile 和层描述文件默认保存在 `~/.cache/isaac-sim-vulkan-rtx-compat/`；其中 `~` 表示运行用户的主目录。如果设置了 `XDG_CACHE_HOME`，则使用该目录作为缓存根目录。

## 检查与排查

开启详细日志，查看驱动信息、原始属性值和兼容层状态：

```bash
ISAAC_SIM_RTX_COMPAT_VERBOSE=1 \
    bash isaac-sim-rtx-compat/launch.sh "/path/to/isaacsim-5.1.0"
```

启用成功时，日志会包含 `[isaacsim_rtx_compat] enabled Vulkan compatibility profile`，并显示覆盖值和库路径。若未启用，先确认设备是否满足自动检测条件。

如需临时禁用兼容处理进行对比：

```bash
ISAAC_SIM_DISABLE_RTX_COMPAT=1 \
    bash isaac-sim-rtx-compat/launch.sh "/path/to/isaacsim-5.1.0"
```

如果提示工具包不完整或库文件缺少权限，请重新解压完整压缩包。如果提示 `no compatible Vulkan Profiles layer was found`，则表示未找到可用库；程序可能继续启动，但兼容处理没有生效。

检查预编译库的动态依赖：

```bash
ldd isaac-sim-rtx-compat/tools/vulkan_profiles/libVkLayer_khronos_profiles.so
```

若出现 `not found` 或 glibc 版本不匹配，请先核对系统与工具包的适用环境。其他系统需要匹配的库构建，可参考 [Vulkan-Profiles 上游源码与构建说明](https://github.com/KhronosGroup/Vulkan-Profiles/tree/v1.4.341)。

## 验证范围

2026 年 8 月的测试中，上述环境启用同一兼容模块与库后，GUI 和 `--no-window` 启动均到达 `app ready`，测试运行期间未再出现该 RTX 段错误。这验证了启动路径，不代表所有场景、训练任务或长期负载均已验证。

随文分发的独立启动脚本另外检查了环境变量传递、参数转发、带空格路径及禁用开关；未针对该打包入口重新执行完整 Isaac Sim 启动测试。

直接运行 `kit/kit`、其他 Python 入口或 Isaac Lab 不会自动经过本工具包。如需用于这些入口，需要在创建 Vulkan 实例前完成兼容环境配置。

## 参考资料

- [Isaac Sim 5.1 系统与驱动要求](https://docs.isaacsim.omniverse.nvidia.com/5.1.0/installation/requirements.html)
- [IsaacSim Issue #568](https://github.com/isaac-sim/IsaacSim/issues/568)
- [Khronos Vulkan Profiles 指南](https://github.khronos.org/Vulkan-Site/guide/latest/vulkan_profiles.html)
- [Vulkan-Profiles v1.4.341 源码](https://github.com/KhronosGroup/Vulkan-Profiles/tree/v1.4.341)
