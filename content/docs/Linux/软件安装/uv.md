---
title: uv
type: docs
---

## 安装 uv

```bash
# For Arch Linux：
paru -S uv
# For Other Linux：
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Shell 自动补全

```bash
# zsh
echo 'eval "$(uv generate-shell-completion zsh)"' >> ~/.zshrc
echo 'eval "$(uvx --generate-shell-completion zsh)"' >> ~/.zshrc

# bash
echo 'eval "$(uv generate-shell-completion bash)"' >> ~/.bashrc
echo 'eval "$(uvx --generate-shell-completion bash)"' >> ~/.bashrc
```

## 升级 uv

```bash
# Arch Linux 会由包管理器自动升级
# For Other Linux：
uv self update
```
