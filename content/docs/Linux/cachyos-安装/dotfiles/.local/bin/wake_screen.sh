#!/bin/bash

# 1. 基础环境设置
export XDG_RUNTIME_DIR="/run/user/$(id -u)"
export DBUS_SESSION_BUS_ADDRESS="unix:path=${XDG_RUNTIME_DIR}/bus"

# 2. 动态获取 Wayland Display 名称 (防止在 wayland-1 等变动情况下失效)
# 如果手动指定过，则优先使用手动指定的，否则自动查找
if [ -z "$WAYLAND_DISPLAY" ]; then
    W_DISP=$(ls "${XDG_RUNTIME_DIR}/wayland-*" 2>/dev/null | head -n 1 | xargs basename)
    export WAYLAND_DISPLAY=${W_DISP:-wayland-0}
fi

# 3. 强制 Qt 使用 wayland 平台
export QT_QPA_PLATFORM=wayland

# 4. 执行唤醒命令
echo "正在尝试唤醒屏幕 (Display: $WAYLAND_DISPLAY)..."
kscreen-doctor --dpms on

# 5. 检查执行结果
if [ $? -eq 0 ]; then
    echo "成功：唤醒指令已发送。"
else
    echo "错误：kscreen-doctor 执行失败，请检查图形会话是否已启动。"
fi
