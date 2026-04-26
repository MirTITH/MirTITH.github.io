---
title: Samba
type: docs
---

## 软件安装和基本配置

### Manjaro / Arch Linux

参考：<https://wiki.archlinux.org/title/Samba>

```bash
# 安装
sudo pacman -S samba

# 添加用户（会要求输入 Samba 共享密码）
sudo smbpasswd -a $USER

# Enable usershares，之后可以直接在 Dolphin 中右键共享文件夹
sudo mkdir /var/lib/samba/usershares
sudo groupadd -r sambashare
sudo chown root:sambashare /var/lib/samba/usershares
sudo chmod 1770 /var/lib/samba/usershares
sudo gpasswd sambashare -a $USER

# 启动并设置开机自启
sudo systemctl enable --now smb

# （可选）通过 NetBIOS 主机名访问
sudo systemctl enable --now nmb
```

### Ubuntu

1. 安装并添加 Samba 用户：

   ```bash
   sudo apt install samba
   sudo smbpasswd -a <用户名>
   ```

2. 在 `/etc/samba/smb.conf` 的 `[global]` 下添加：

   ```conf
   usershare owner only = false
   unix extensions = No
   follow symlinks = Yes
   wide links = Yes
   ```

3. 重启服务：

   ```bash
   sudo service smbd restart
   ```

## 添加共享目录

- KDE/Manjaro 下通常可以直接在 Dolphin 文件管理器中右键共享文件夹
- 共享目录的记录位置：`/var/lib/samba/usershares`
- Samba 主配置文件位置：`/etc/samba/smb.conf`

## 用户别名

如果需要为用户或用户组配置别名，可以在 `smb.conf` 的全局配置中添加：

```conf
username map = /etc/samba/users.map
```

然后创建 `/etc/samba/users.map`，按如下格式填写：

```text
xy = DOMAIN\user
```

用户组别名可写成：

```text
alias = @DOMAIN\group
```

## 常见问题

### `net usershare` 返回错误 255

在 `smb.conf` 的 `[global]` 下添加：

```conf
usershare owner only = false
```

### 共享目录中的软链接无法访问

在 `smb.conf` 的 `[global]` 下添加：

```conf
unix extensions = No
follow symlinks = Yes
wide links = Yes
```

### `daemon failed to start: Samba cannot init registry`

```bash
sudo rm /var/lib/samba/registry.tdb
```

参考：<https://blog.csdn.net/u013310025/article/details/86721604>