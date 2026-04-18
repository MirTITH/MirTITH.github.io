---
title: MATLAB
type: docs
---

## For Arch Linux

1. **安装mpm (Matlab package manager)**
   
   ```shell
   paru -S matlab-mpm
   ```
   
2. **使用mpm安装Matlab**
   
   ```shell
   mpm install --release=<release> --destination=~/matlab MATLAB <other products>
   ```
   若希望为设备上所有用户安装，则将目录修改为公共目录，例如:
   ```shell
   sudo mpm install --release R2025b --products \
                  Simulink \
                  Stateflow \
                  Simulink_Control_Design \
                  Simulink_Compiler \
                  Simulink_Real-Time \
                  DSP_System_Toolbox \
                  Simscape \
                  Simscape_Electrical \
                  Simscape_Fluids \
                  Simscape_Multibody \
                  Fixed-Point_Designer \
                  --matlabroot /opt/MATLAB/R2025b/
   ```
   
3. **激活Matlab**

   如果 `--release <= R2022b`
   ```shell
   ~/matlab/bin/activate_matlab.sh
   ```
   如果 `--release >= R2023a`
   ```shell
   ~/matlab/bin/glnxa64/MathWorksProductAuthorizer.sh
   ```
   注意，当为所有用户安装时，应相应修改路径。可能需要sudo以提供权限，否则可能出现权限冲突的错误提示：Unable to install license. Please try again later.
   ```shell
   sudo /opt/MATLAB/R2025b/bin/glnxa64/MathWorksProductAuthorizer.sh
   ```

4. **修复链接库**
   如果 `--release >= R2023a`，在运行`MathWorksProductAuthorizer.sh`时极大概率报`segfault`，是由于某个版本的`gnutls`更新导致的，运行以下命令使得matlab激活脚本使用老版的`gnutls`：
   ```shell
   wget https://archive.archlinux.org/packages/g/gnutls/gnutls-3.8.9-1-x86_64.pkg.tar.zst
   mkdir -p matlab/gnutls
   tar -xf gnutls-3.8.9-1-x86_64.pkg.tar.zst -C matlab/gnutls
   mkdir -p ~/matlab/bin/glnxa64/gnutls
   cp -a ~/matlab/gnutls/usr/lib/libgnutls* ~/matlab/bin/glnxa64/gnutls/
   cd /home/user/matlab/bin/glnxa64/
   ln -s gnutls/* ./
   ```
   为所有用户安装的命令相应修改为
   ```shell
   wget https://archive.archlinux.org/packages/g/gnutls/gnutls-3.8.9-1-x86_64.pkg.tar.zst
   mkdir -p matlab/gnutls
   tar -xf gnutls-3.8.9-1-x86_64.pkg.tar.zst -C matlab/gnutls
   sudo mkdir -p /opt/MATLAB/R2025b/bin/glnxa64/gnutls
   sudo cp -a matlab/gnutls/usr/lib/libgnutls.* /opt/MATLAB/R2025b/bin/glnxa64/gnutls/
   sudo ln -s gnutls/* ./
   ```
   之后应该可以回到上一步成功进行Matlab的激活。
   ```shell
   sudo ./MathWorksProductAuthorizer.sh
   ```

5. **权限问题**
   直接运行会出现安全提示：You are currently running MATLAB as root。在 Linux 中，长期以 root 身份运行图形界面程序会有安全风险，且以后产生的代码文件权限也会变成 root，导致普通用户无法编辑。最后可以把MATLAB目录的所有权交还给普通用户
   首先创建软连接：
   ```shell
   sudo ln -s /opt/MATLAB/R2025b/bin/matlab /usr/local/bin/matlab
   ```

6. **（可选）修复中文输入法**

   由于 Arch 总是滚动更新到最新的 GCC 和 Qt，而 MATLAB 捆绑的库相对滞后，导致了 ABI 不兼容。通过强制使用系统 C++ 标准库可以暂时修复输入法。
   <u>***注意**：如果下次 MATLAB 小版本更新（如 R2025b Update 1），这些操作可能需要重新执行，因为更新程序可能会还原这些库文件。</u>

   （1）进入 MATLAB 安装目录下的系统库路径，重命名其自带的库文件，迫使系统调用 `/usr/lib/libstdc++.so.6`。

   ```bash
   cd /opt/MATLAB/R2025b/sys/os/glnxa64/
   sudo mv libstdc++.so.6 libstdc++.so.6.bak
   ```

   （2）将 MATLAB 自带的 Qt5 相关动态库移出搜索路径，强制使用与系统插件版本一致（或兼容）的 Qt 库。

   ```bash
   cd /opt/MATLAB/R2025b/bin/glnxa64/
   sudo mkdir qt_backup
   sudo mv libQt5* qt_backup/
   ```

   （3）在MATLAB插件目录下建立系统插件软连接，注入 fcitx5 输入法插件

   ```bash
   sudo mkdir -p /opt/MATLAB/R2025b/bin/glnxa64/platforminputcontexts
   sudo ln -sf /usr/lib/qt/plugins/platforminputcontexts/libfcitx5platforminputcontextplugin.so /opt/MATLAB/R2025b/bin/glnxa64/platforminputcontexts/
   ```

   （4）在启动脚本中加入环境配置

   ```bash
   export QT_IM_MODULE=fcitx
   export XMODIFIERS=@im=fcitx
   ```