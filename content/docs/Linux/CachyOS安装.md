---
title: CachyOS安装
type: docs
---

## 解决 CachyOS 安装前的网络问题

CachyOS 在国内安装容易因网络问题失败，在此记录解决方法。

### 1. 跳过 update-mirrorlist 脚本

编辑 `/etc/calamares/scripts/update-mirrorlist`

```bash
/etc/calamares/scripts/update-mirrorlist
```

在第二行添加 `exit 0`，使脚本直接退出，最终内容如下：

```bash
#!/usr/bin/env bash
exit 0
echo "Updating rate-mirrors"
sudo pacman -Sy --noconfirm --needed cachyos-rate-mirrors rate-mirrors
sudo cachyos-rate-mirrors
```

将该文件设为只读，以防止安装过程中被修改：

```bash
sudo chattr +i /etc/calamares/scripts/update-mirrorlist
```

### 2. 换源

将 CachyOS 与 Arch 的镜像优先切换到中科大源。

先备份原配置：

```bash
sudo cp /etc/pacman.d/cachyos-mirrorlist /etc/pacman.d/cachyos-mirrorlist.bak
sudo cp /etc/pacman.d/cachyos-v3-mirrorlist /etc/pacman.d/cachyos-v3-mirrorlist.bak
sudo cp /etc/pacman.d/cachyos-v4-mirrorlist /etc/pacman.d/cachyos-v4-mirrorlist.bak
sudo cp /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.bak
```

在以下文件最顶端添加对应 `Server` 行（放在第一行即可）：

- `/etc/pacman.d/cachyos-mirrorlist`

```ini
Server = https://mirrors.ustc.edu.cn/cachyos/repo/$arch/$repo
```

- `/etc/pacman.d/cachyos-v3-mirrorlist`

```ini
Server = https://mirrors.ustc.edu.cn/cachyos/repo/$arch_v3/$repo
```

- `/etc/pacman.d/cachyos-v4-mirrorlist`

```ini
Server = https://mirrors.ustc.edu.cn/cachyos/repo/$arch_v4/$repo
```

- `/etc/pacman.d/mirrorlist`

```ini
Server = https://mirrors.ustc.edu.cn/archlinux/$repo/os/$arch
```

最后更新镜像：

```bash
sudo pacman -Sy
```
