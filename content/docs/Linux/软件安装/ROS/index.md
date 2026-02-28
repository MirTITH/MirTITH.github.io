---
title: ROS
type: docs
---

## 在 Conda 中安装 ROS/ROS 2

安装 Conda 的方法见 [Conda](../conda)。

在 Conda 中安装 ROS/ROS 2 的方法： <https://robostack.github.io/GettingStarted.html>

## 在 Ubuntu 上安装 ROS/ROS 2

### ROS

校内源：<https://mirrors-help.osa.moe/ros>

官网：<http://wiki.ros.org/noetic/Installation/Ubuntu>

### ROS 2

#### Humble for Ubuntu 22.04

```shell
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

# 添加源（以下几个源选择一个）：
# 官方源
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
# HITsz 内网源
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] https://mirrors.osa.moe/ros2/ubuntu jammy main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
# 中科大源
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] https://mirrors.ustc.edu.cn/ros2/ubuntu jammy main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
# 清华源
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] https://mirrors.tuna.tsinghua.edu.cn/ros2/ubuntu jammy main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

sudo apt update
sudo apt upgrade
sudo apt install ros-humble-desktop ros-dev-tools
# 完成！

# Gazebo 11（可选）
sudo apt install ros-humble-gazebo-ros-pkgs

# colcon mixin
sudo apt install python3-colcon-common-extensions python3-colcon-mixin
colcon mixin add default https://raw.githubusercontent.com/colcon/colcon-mixin-repository/master/index.yaml
colcon mixin update default

# 测试：
# 开一个终端：
source /opt/ros/humble/setup.bash
ros2 run demo_nodes_cpp talker
# 再开一个终端：
source /opt/ros/humble/setup.bash
ros2 run demo_nodes_py listener
```

> [!NOTE]
> 不建议直接将 `source /opt/ros/humble/setup.bash` 添加到 `~/.bashrc` 或 `~/.zshrc` 中，这会导致每次打开终端都自动进入 ROS 环境，干扰其他开发工作（如干扰 Python 包搜索路径）。
> 
> 为避免每次进入 ROS 环境都要输入长指令，我编写了终端快捷指令，**安装步骤如下**：
> 
> 1. 根据 ros2 版本，选择合适的文件，保存为 `~/.local/ros2_rc`：
>    - [ROS 2 Humble](ros2_rc/humble)
>    - [ROS 2 Jazzy](ros2_rc/jazzy)
> 2. 在 `~/.bashrc` 和 `~/.zshrc` 中添加以下内容：
>    ```bash
>    # ROS 2 环境切换
>    [[ ! -f ~/.local/ros2_rc ]] || source ~/.local/ros2_rc
>    ```
> **使用方式**：打开一个新的终端，然后：
> - 输入 `rr` 即可 source 系统 ros2
> - 输入 `rs` 即可先 source 系统 ros2，再 source 当前目录下的 ros2 工作空间
> 该脚本还会自动配置 `ros2`, `colcon`, `colcon_cd` 等命令的自动补全，并支持设置 `ROS_DOMAIN_ID` 环境变量。

## 常见问题

### 构建 ros2 python 包时报 EasyInstallDeprecationWarning

因为 ros2 humble 安装 Python 包的方式已经被弃用了，所以报 warning. 

但目前 ros2 humble 并没有很好的替代方案，所以为了不报 warning, 只能降级安装工具 setuptools. 

```shell
# 降级到最后一个不会报 warning 的版本
pip install setuptools==58.2.0
```

> 参考链接：<https://answers.ros.org/question/396439/setuptoolsdeprecationwarning-setuppy-install-is-deprecated-use-build-and-pip-and-other-standards-based-tools/>
