---
title: Conda
type: docs
---

**Conda 是一个开源的包管理系统和虚拟环境管理系统。** 它可以管理 Python 及其他语言的依赖，并通过虚拟环境隔离不同项目的包版本，避免冲突。

{{% details title="Conda 相关概念介绍" closed="true" %}}

> 更详细的介绍请看B站大佬的视频：[15分钟彻底搞懂！Anaconda Miniconda conda-forge miniforge Mamba_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1Fm4ZzDEeY)

Conda 生态涉及多个相关概念，下面分三层介绍：

### 1. 工具层：Conda 与 Mamba

* **Conda**：核心包管理工具，负责环境创建、包安装、依赖解析等操作。
* **Mamba**：Conda 的 C++ 实现版本，命令完全兼容（`mamba install` 等同于 `conda install`），但依赖解析速度显著更快，特别在安装大型环境时优势明显。

### 2. 发行版层：Anaconda、Miniconda、Miniforge

发行版是一个预配置的安装包，包含工具和默认设置。常见选择：

* **Anaconda**：包含 Conda、Python 及 1500+ 科学计算库（NumPy、Pandas、Scikit-learn 等）。体积大，适合快速开始。
* **Miniconda**：包含 Conda、Python 及最小依赖，默认使用官方频道（defaults）。轻量且足够灵活，适合大多数开发者。
* **Miniforge**：包含 Conda、Python、mamba 及最小依赖，默认使用社区频道（conda-forge）。推荐选项。

### 3. 软件源层：Channels

`channel`（频道）是软件包的存储位置。Conda 安装包时，会从配置的 channel 中下载和解析依赖。

* **defaults**：Anaconda 官方维护，更新稳健但节奏相对较慢。**对商业用途收费**。
* **conda-forge**：社区维护，包覆盖广、更新快、跨平台一致性较好。

不建议混用 channel，这样容易导致依赖冲突。

### 推荐方案

**推荐使用 Miniforge + mamba**，原因如下：

* 开箱即用 conda-forge 和 mamba，无需额外配置。
* mamba 依赖解析更快，提升日常工作效率。
* conda-forge 生态活跃，包更新更及时，商业用途免费。

{{% /details %}}

### Miniforge（推荐）

**安装**

```bash
wget "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
```

上面的脚本会提示是否初始化 bash，但不会初始化 zsh。如果使用 zsh 需要手动初始化：

```bash
~/miniforge3/bin/conda init zsh
~/miniforge3/bin/mamba shell init -s zsh
```

推荐再安装 [Zsh 补全](#conda-zsh-补全)

**取消默认进入 base 环境**
```
conda config --set auto_activate false
```

[Conda 换源](/docs/网络/换源/#conda)

### Miniconda

安装：

```bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
```

初始化 bash 和 zsh：

```bash
~/miniconda3/bin/conda init bash
~/miniconda3/bin/conda init zsh
```

推荐再安装 [Zsh 补全](#conda-zsh-补全)

取消默认进入 base 环境：

```shell
conda config --set auto_activate false
```

### Conda Zsh 补全

```bash
# Arch Linux 用户可以直接安装 conda-zsh-completion 包
paru -S conda-zsh-completion
```
