---
title: Docker
type: docs
---

## 安装

### For Ubuntu

1. 安装 docker

   ```shell
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   ```

2. 使 docker 命令不需要 root 运行

   ```shell
   sudo groupadd docker
   sudo usermod -aG docker $USER
   ```

3. Log out and log back in so that your group membership is re-evaluated.

4. Test your docker installation

   ```shell
   docker run hello-world
   ```

5. 安装 Nvidia Container Toolkit：
   1. 打开链接：<https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html>
   2. 按照网页中的指引，在主机中安装 nvidia-container-toolkit
   3. 执行网页中 Configuring Docker 的部分，注意不需要执行 Rootless mode

### For Manjaro/Arch Linux

```shell
# 安装
paru -S docker docker-buildx

# 启动和开机自启
sudo systemctl start docker.service
sudo systemctl enable docker.service

# 检查
sudo docker version
sudo docker info

# 使得运行 docker 命令不需要 root 权限，重启生效
sudo usermod -aG docker $USER
reboot
```

接下来安装 NVIDIA Container Toolkit，使 docker 能够使用 NVIDIA GPU

```shell
# 安装
sudo pacman -S nvidia-container-toolkit

# 配置
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

## docker 运行 GUI 程序

```shell
# Manjaro/Arch Linux 需要安装 xorg-xhost
# （Ubuntu 自带 xhost，不需要安装）
sudo pacman -S xorg-xhost

# 允许 docker 访问主机的显示服务：
# 注意：重启电脑后需要再次执行
xhost +local:docker

# 在 docker 中测试
# 进入一个 docker 容器，执行：
sudo apt update
sudo apt install x11-apps
xclock
```

## 常见问题

如果更新显卡驱动后 docker 容器启动异常，报错类似于：
```
Error response from daemon: failed to create task for container: failed to create shim task: OCI runtime create failed: runc create failed: unable to start container process: error during container init: failed to fulfil mount request: open /usr/lib/libEGL_nvidia.so.590.48.01: no such file or directory
```

可重新安装 nvidia-container-toolkit，或执行：

```bash
sudo nvidia-ctk cdi generate --output="/etc/cdi/nvidia.yaml"
```