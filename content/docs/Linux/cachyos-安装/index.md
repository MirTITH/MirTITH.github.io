---
title: CachyOS 安装
type: docs
---

## LiveCD 安装前的准备

CachyOS 在国内安装容易因网络问题失败，需要进行一些准备工作以确保安装顺利完成。

### 1. 跳过 update-mirrorlist 脚本

编辑文件：

```bash
kate /etc/calamares/scripts/update-mirrorlist
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

打开文件：

```bash
cd /etc/pacman.d
kate cachyos-mirrorlist cachyos-v3-mirrorlist cachyos-v4-mirrorlist mirrorlist
```

在以下文件最顶端添加：

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
    # 校内源
    # Server = https://mirrors.osa.moe/archlinux/$repo/os/$arch
    # 中科大源
    Server = https://mirrors.ustc.edu.cn/archlinux/$repo/os/$arch
    ```

最后更新镜像：

```bash
sudo pacman -Syy
```

### 3. 启动安装程序

启动安装程序。安装时最好选择英文语言，使得家目录文件夹命名为英文。

## 安装后配置

### 启用 archlinuxcn

编辑 `/etc/pacman.conf`，在末尾添加：

```ini
[archlinuxcn]
# 校内源
Server = https://mirrors.osa.moe/archlinuxcn/$arch
# 中科大源
# Server = https://mirrors.ustc.edu.cn/archlinuxcn/$arch
```

安装 keyring：

```bash
sudo pacman -Sy archlinuxcn-keyring
```

### 配置 paru

编辑 `/etc/paru.conf`，取消 `BottomUp` 和 `SudoLoop` 的注释。

### 基础配置

```bash
git config --global user.name "<your-name>"
git config --global user.email "<your-email>"
git config --global core.quotepath false
```

让 `sudo` 继承代理变量，使得在使用 `sudo` 执行命令时也能使用代理：

```bash
paru -S --needed vi
sudo visudo /etc/sudoers.d/05_proxy
```

添加（优先尝试这一行）：

```text
Defaults env_keep += "*_proxy *_PROXY"
```

若系统提示语法不支持，则改用：

```text
Defaults env_keep += "http_proxy https_proxy ftp_proxy all_proxy no_proxy HTTP_PROXY HTTPS_PROXY FTP_PROXY ALL_PROXY NO_PROXY"
```

### 代理软件 

```bash
paru -S sparkle
```

### 字体与常用软件

```bash
paru -S --needed ttf-lxgw-wenkai ttf-lxgw-wenkai-mono noto-fonts-cjk typora visual-studio-code-bin moonlight-qt mission-center
```

### 解决部分软件显示为日文字形问题

创建文件 `~/.config/fontconfig/conf.d/64-language-selector-prefer.conf`：

```xml
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <alias>
    <family>sans-serif</family>
    <prefer>
      <family>Noto Sans CJK SC</family>
    </prefer>
  </alias>
  <alias>
    <family>serif</family>
    <prefer>
      <family>Noto Serif CJK SC</family>
    </prefer>
  </alias>
  <alias>
    <family>monospace</family>
    <prefer>
      <family>Noto Sans Mono CJK SC</family>
    </prefer>
  </alias>
</fontconfig>
```

> 来自 Claude

### 输入法（Wayland + Fcitx5）

安装：

```bash
paru -S --needed fcitx5-im fcitx5-chinese-addons fcitx5-mozc fcitx5-pinyin-zhwiki fcitx5-pinyin-moegirl
```

在 KDE 中进入 `System Settings -> Virtual Keyboard`，选择 `Fcitx 5`。

然后编辑 GTK 程序的配置文件：

```bash
kate ~/.gtkrc-2.0 ~/.config/gtk-3.0/settings.ini ~/.config/gtk-4.0/settings.ini
```

进行如下修改：

- `~/.gtkrc-2.0` 在末尾加入：
    ```ini
    gtk-im-module="fcitx"
    ```

- `~/.config/gtk-3.0/settings.ini` 在 `[Settings]` 部分加入：
    ```ini
    gtk-im-module=fcitx
    ```

- `~/.config/gtk-4.0/settings.ini` 在 `[Settings]` 部分加入：
    ```ini
    gtk-im-module=fcitx
    ```

> 参考：  
> <https://fcitx-im.org/wiki/Using_Fcitx_5_on_Wayland>  
> <https://wiki.archlinux.org/title/Fcitx5>  

### 服务项

#### SSH

```bash
paru -S --needed openssh

# （可选）修改配置（最好改个端口，默认的 22 端口容易被攻击）
kate /etc/ssh/sshd_config

sudo systemctl enable --now sshd
```

#### 禁用鼠标/键盘唤醒

```bash
paru -S --needed wakeup-triggers
sudo systemctl enable --now wakeup-triggers.service
```

#### Sunshine （远程桌面）

```bash
paru -S --needed sunshine
systemctl --user enable --now sunshine
```

### 常用应用

```bash
# 微信
paru -S --needed wechat

# QQ（在沙箱中运行，可以解决装了docker 后因虚拟网卡变动导致每次都要重新登录的问题）
# 沙箱隔离了文件系统，可以在 ~/.config/qq-bwrap-flags.conf 中配置映射路径
# 示例文件见 `一些配置文件` 部分
paru -S --needed slirp4netns linuxqq-nt-bwrap

# 音乐播放器
paru -S --needed python-pyqt5-webengine feeluown-full
```

### 一些配置文件

<https://github.com/MirTITH/MirTITH.github.io/tree/main/content/docs/Linux/cachyos-安装/dotfiles>

### KDE 设置建议

- 鼠标：禁用指针加速度
- 键盘：NumLock 在开机时的状态：打开
- 显示和监视器→屏幕边缘：左上角改为无操作
- 颜色和主题
  - 全局主题：Breeze 微风阴阳
  - 颜色：基于壁纸获取强调色
- 窗口管理
    - 窗口行为→窗口操作→窗口内部、标题栏和边框操作：鼠标滚轮：更改不透明度
    - 任务切换器->可视化：缩略图网格
    - 桌面特效：勾选 窗口透明度
    - 虚拟桌面：增加行数，添加一个桌面，勾选循环切换。
- 登录屏幕：勾选自动登录，点击应用 Plasma 设置（可配合 KDE 启动时立刻锁定）
- 电源管理：空闲时无操作，关闭屏幕 30 分钟，锁屏延迟约 20 秒。

**配置 KDE 启动时立刻锁定（配合自动登陆）**

好处：自动登录使得 sunshine 和 sparkle 能够在开机后自动启动，立即锁屏则保证了安全性。

```bash
kate ~/.config/kscreenlockerrc
```

添加`LockOnStart=true`：
```
[Daemon]
Timeout=30
LockOnStart=true
```

### 将家目录文件夹改成英文

如果安装时选择了中文，家目录文件夹会被命名为中文。如果希望改成英文，可以执行：

```bash
export LANG=en_US.UTF-8
xdg-user-dirs-update --force
```

再修改 Dolphin 文件管理器的书签：

```bash
kate ~/.local/share/user-places.xbel
```
