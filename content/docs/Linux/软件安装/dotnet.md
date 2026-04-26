---
title: .NET
type: docs
---

## .NET 6

### ubuntu 20.04

```bash
wget https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
rm packages-microsoft-prod.deb
sudo apt update
sudo apt install dotnet-runtime-6.0
```

### ubuntu 22.04

```bash
sudo apt install dotnet-runtime-6.0
```