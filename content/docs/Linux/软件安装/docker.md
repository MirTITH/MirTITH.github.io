---
title: Docker
type: docs
---

## 准备工作：将 docker 数据目录放到单独的 btrfs 子卷上 （可选）

如果使用 btrfs 文件系统作为根目录并且配置了快照，建议将 docker 的数据目录放到单独的 btrfs 子卷上，防止对 docker 打快照。

### 1. 准备存储空间

> Docker 使用的路径：<https://docs.docker.com/engine/daemon/#daemon-data-directory>

Docker 默认会将数据存储在 `/var/lib/docker` 和 `/var/lib/containerd` 目录下。于是我们创建2个子卷：

```bash
# 查看根目录对应的设备的 UUID
lsblk -f

# 假设是 00efe411-cb8a-42f3-8fab-2c12840cf6df，将其挂载到 /mnt/root
sudo mkdir /mnt/root
sudo mount /dev/disk/by-uuid/00efe411-cb8a-42f3-8fab-2c12840cf6df /mnt/root
cd /mnt/root

# 检查内容，应该类似 @ @cache  @home  @log  @root  @srv  @tmp
ls

# 创建子卷
sudo btrfs subvolume create @docker @containerd

# 如果 /var/lib/docker 和 /var/lib/containerd 已有内容，则需要移动到新的子卷中：
# 检查是否有内容
sudo ls -A /var/lib/docker
sudo ls -A /var/lib/containerd
# 如果有内容，移动到新的子卷中
sudo mv /var/lib/docker/* /mnt/root/@docker/
sudo mv /var/lib/containerd/* /mnt/root/@containerd/
# 再次检查，应该没有内容了
sudo ls -A /var/lib/docker
sudo ls -A /var/lib/containerd
```

### 2. 配置 fstab

编辑 `/etc/fstab`，添加以下内容：

```conf
UUID=00efe411-cb8a-42f3-8fab-2c12840cf6df /var/lib/docker       btrfs   subvol=@docker,defaults,noatime,compress=zstd:1     0 0
UUID=00efe411-cb8a-42f3-8fab-2c12840cf6df /var/lib/containerd   btrfs   subvol=@containerd,defaults,noatime,compress=zstd:1 0 0
```

之后执行以下命令挂载：

```bash
sudo systemctl daemon-reload
sudo mount -m /var/lib/docker
sudo mount -m /var/lib/containerd
```

验证：

```bash
 mount | grep /var/lib/
# 输出内容应该类似：
# /dev/nvme1n1p2 on /var/lib/docker type btrfs (rw,noatime,compress=zstd:1,ssd,discard=async,space_cache=v2,# subvolid=1771,subvol=/@docker)
# /dev/nvme1n1p2 on /var/lib/containerd type btrfs (rw,noatime,compress=zstd:1,ssd,discard=async,space_cache=v2,subvolid=1772,subvol=/@containerd)
```

### 3. 卸载 `/mnt/root`

```bash
sudo umount /mnt/root
sudo rmdir /mnt/root
```

注：`rmdir` 命令只会删除空目录，相比于 `rm -rf` 更安全（否则万一忘记卸载，容易把系统删了）

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
sudo systemctl enable --now docker.service

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

## 修改配置以使用传统的 overlay2 存储驱动

Docker 在 29.0 版本之后默认使用 [containerd image store](https://docs.docker.com/engine/storage/containerd/)，而不是传统的 overlay2 存储驱动。

> 不同存储驱动的介绍：<https://docs.docker.com/engine/storage/drivers/select-storage-driver/>

containerd image store 支持的新功能我们完全用不到，却会带来构建速度下降、磁盘占用增加等问题，因此建议改回 overlay2，方法如下：  

**停止 Docker：**
```bash
sudo systemctl stop docker
```

**创建或修改 `/etc/docker/daemon.json` 文件，写入以下内容：**
```json
{
  "storage-driver": "overlay2"
}
```

注意：如果文件中已有其他配置，需合并。例如：
```json
{
    "runtimes": {
        "nvidia": {
            "args": [],
            "path": "nvidia-container-runtime"
        }
    },
    "storage-driver": "overlay2"
}
```

**启动 Docker：**

```bash
sudo systemctl start docker
```

**验证：**

```bash
docker info | grep 'Storage Driver'
# 输出内容应该是：
# Storage Driver: overlay2
# 而不是：
# Storage Driver: overlayfs
```

> 参考自：<https://docs.docker.com/engine/storage/drivers/overlayfs-driver/>

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

## docker 代理上网

> 请看：  
> 1. docker daemon 配置代理（适用于 docker pull）：<https://docs.docker.com/engine/daemon/proxy/>
> 2. docker CLI 配置代理（适用于构建阶段、运行容器时）：<https://docs.docker.com/engine/cli/proxy/>

### 太长不看版

#### docker daemon 配置代理   

1. 创建文件：
   ```bash
   sudo mkdir -p /etc/systemd/system/docker.service.d
   sudo vim /etc/systemd/system/docker.service.d/http-proxy.conf
   ```
   写入以下内容：
   ```conf
   [Service]
   Environment="HTTP_PROXY=http://localhost:7890"
   Environment="HTTPS_PROXY=http://localhost:7890"
   Environment="NO_PROXY=localhost,127.0.0.1,::1,10.0.0.0/8,192.168.0.0/16,mirrors.osa.moe,.osa.moe,.internal,.local"
   ```
2. 应用：
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl restart docker
   ```
3. 验证：
   ```bash
   sudo systemctl show --property=Environment docker
   # 输出内容应该包含：
   # Environment=HTTP_PROXY=http://localhost:7890 HTTPS_PROXY=http://localhost:7890 NO_PROXY=localhost,127.0.0.1,::1,10.0.0.0/8,192.168.0.0/16,mirrors.osa.moe,.osa.moe,.internal,.local
   ```

#### docker CLI 配置代理

```bash
docker build \
   --build-arg HTTP_PROXY=http://localhost:7890 \
   --build-arg HTTPS_PROXY=http://localhost:7890 \
   --build-arg NO_PROXY=localhost,127.0.0.1,::1,10.0.0.0/8,192.168.0.0/16,mirrors.osa.moe,.osa.moe,.internal,.local \
   -t your-image:tag .
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