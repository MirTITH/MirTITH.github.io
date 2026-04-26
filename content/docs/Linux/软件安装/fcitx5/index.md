---
title: Fcitx5
type: docs
---

## 卸载旧版 Fcitx（可选）

```bash
sudo apt purge *fcitx*
```

## 安装

### Ubuntu 22.04

```bash
sudo apt update
sudo apt install fcitx5 'fcitx5-frontend*' fcitx5-chinese-addons fcitx5-material-color fcitx5-module-cloudpinyin kde-config-fcitx5
```

### Ubuntu 20.04

```bash
sudo apt update
sudo apt install fcitx5 'fcitx5-frontend*' fcitx5-chinese-addons
```

### Arch / CachyOS

Wayland + KDE 环境下的安装与 GTK 配置，可直接参考 [CachyOS 安装](/docs/Linux/cachyos-安装/#输入法wayland--fcitx5)。

## 启用与基础配置

- Kubuntu 22.04 一般重启后即可生效
- 如果重启后仍未生效，可以执行：

  ```bash
  im-config
  ```

  然后选择 `fcitx5`

- KDE 下可在系统设置中添加拼音输入法（不是 Keyboard - Chinese）

## 安装词典

中文维基词典：<https://github.com/felixonmars/fcitx5-pinyin-zhwiki>

萌娘百科词典：<https://github.com/outloudvi/mw2fcitx/releases>

下载最新的 `.dict` 文件后，复制到：

```bash
mkdir -p ~/.local/share/fcitx5/pinyin/dictionaries/
```

## 安装主题

### fcitx5-breeze

1. 从 <https://github.com/scratch-er/fcitx5-breeze/releases> 下载发布包
2. 执行包中的 `install.sh`

### Simple-white / Simple-dark

参考：<https://www.cnblogs.com/maicss/p/15056420.html>

```bash
mkdir -p ~/.local/share/fcitx5/themes/
cp -r <主题目录>/* ~/.local/share/fcitx5/themes/
gedit ~/.config/fcitx5/conf/classicui.conf
```

将主题名改为 `Simple-white` 或 `Simple-dark`。