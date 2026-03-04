---
title: "解决 Isaac Sim 5.1.0 的 CXXABI_1.3.15 Not Found 错误"
type: docs
date: 2026-03-04T21:43:48+08:00
draft: false
---

## 问题描述

在 Ubuntu 22.04 上安装 Isaac Sim 5.1.0，再使用 [Installation using Isaac Sim Pre-built Binaries](https://isaac-sim.github.io/IsaacLab/main/source/setup/installation/binaries_installation.html#installation-using-isaac-sim-pre-built-binaries) 方式安装 Isaac Lab，最后使用 `./isaaclab.sh --conda` 创建 conda 环境，在 conda 环境中运行训练脚本时，报错如下：

{{% details title="点击展开" closed="true" %}}

```
2026-03-04T13:23:56Z [2,332ms] [Error] [omni.ext._impl.custom_importer] Failed to import python module omni.kit.test. Error: /lib/x86_64-linux-gnu/libstdc++.so.6: version `CXXABI_1.3.15' not found (required by /home/xieyang/miniforge3/envs/env_isaaclab/lib/python3.11/lib-dynload/../.././libicui18n.so.78). Traceback:
Traceback (most recent call last):
  File "/home/xieyang/IsaacLab/_isaac_sim/kit/kernel/py/omni/ext/_impl/custom_importer.py", line 85, in import_module
    return importlib.import_module(name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/xieyang/miniforge3/envs/env_isaaclab/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/xieyang/isaacsim/extscache/omni.kit.test-2.0.1+69cbf6ad.lx64.r.cp311/omni/kit/test/__init__.py", line 7, in <module>
    from . import unittests
  File "/home/xieyang/isaacsim/extscache/omni.kit.test-2.0.1+69cbf6ad.lx64.r.cp311/omni/kit/test/unittests.py", line 21, in <module>
    from .async_unittest import AsyncTestSuite, AsyncTextTestRunner, OmniTestResult, AsyncTestCase
  File "/home/xieyang/isaacsim/extscache/omni.kit.test-2.0.1+69cbf6ad.lx64.r.cp311/omni/kit/test/async_unittest.py", line 25, in <module>
    from .reporter import TestReporter
  File "/home/xieyang/isaacsim/extscache/omni.kit.test-2.0.1+69cbf6ad.lx64.r.cp311/omni/kit/test/reporter.py", line 27, in <module>
    from .test_coverage import generate_coverage_report
  File "/home/xieyang/isaacsim/extscache/omni.kit.test-2.0.1+69cbf6ad.lx64.r.cp311/omni/kit/test/test_coverage.py", line 10, in <module>
    import coverage
  File "/home/xieyang/isaacsim/extscache/omni.kit.pip_archive-0.0.0+69cbf6ad.lx64.cp311/pip_prebundle/coverage/__init__.py", line 24, in <module>
    from coverage.control import (
  File "/home/xieyang/isaacsim/extscache/omni.kit.pip_archive-0.0.0+69cbf6ad.lx64.cp311/pip_prebundle/coverage/control.py", line 28, in <module>
    from coverage.collector import Collector, HAS_CTRACER
  File "/home/xieyang/isaacsim/extscache/omni.kit.pip_archive-0.0.0+69cbf6ad.lx64.cp311/pip_prebundle/coverage/collector.py", line 19, in <module>
    from coverage.data import CoverageData
  File "/home/xieyang/isaacsim/extscache/omni.kit.pip_archive-0.0.0+69cbf6ad.lx64.cp311/pip_prebundle/coverage/data.py", line 24, in <module>
    from coverage.sqldata import CoverageData
  File "/home/xieyang/isaacsim/extscache/omni.kit.pip_archive-0.0.0+69cbf6ad.lx64.cp311/pip_prebundle/coverage/sqldata.py", line 16, in <module>
    import sqlite3
  File "/home/xieyang/miniforge3/envs/env_isaaclab/lib/python3.11/sqlite3/__init__.py", line 57, in <module>
    from sqlite3.dbapi2 import *
  File "/home/xieyang/miniforge3/envs/env_isaaclab/lib/python3.11/sqlite3/dbapi2.py", line 27, in <module>
    from _sqlite3 import *
ImportError: /lib/x86_64-linux-gnu/libstdc++.so.6: version `CXXABI_1.3.15' not found (required by /home/xieyang/miniforge3/envs/env_isaaclab/lib/python3.11/lib-dynload/../.././libicui18n.so.78)

2026-03-04T13:23:56Z [2,332ms] [Error] [carb.scripting-python.plugin] Exception: Extension python module: 'omni.kit.test' in '/home/xieyang/isaacsim/extscache/omni.kit.test-2.0.1+69cbf6ad.lx64.r.cp311' failed to load.

At:
  /home/xieyang/IsaacLab/_isaac_sim/kit/kernel/py/omni/ext/_impl/_internal.py(222): startup
  /home/xieyang/IsaacLab/_isaac_sim/kit/kernel/py/omni/ext/_impl/_internal.py(337): startup_extension
  PythonExtension.cpp::startup()(2): <module>
  /home/xieyang/IsaacLab/_isaac_sim/exts/isaacsim.simulation_app/isaacsim/simulation_app/simulation_app.py(534): _start_app
  /home/xieyang/IsaacLab/_isaac_sim/exts/isaacsim.simulation_app/isaacsim/simulation_app/simulation_app.py(270): __init__
  /home/xieyang/IsaacLab/source/isaaclab/isaaclab/app/app_launcher.py(823): _create_app
  /home/xieyang/IsaacLab/source/isaaclab/isaaclab/app/app_launcher.py(131): __init__
  /home/xieyang/Documents/IsaacLabTutorial/scripts/skrl/train.py(60): <module>

2026-03-04T13:23:56Z [2,332ms] [Error] [omni.ext.plugin] [ext: omni.kit.test-2.0.1] Failed to startup python extension.
```

{{% /details %}}

## 分析

在你的报错信息中，链路是这样的：

1. **Isaac Lab** 启动时加载了 `omni.kit.test`。
2. `omni.kit.test` 调用了 Python 的 `coverage` 模块。
3. `coverage` 模块需要用到 **`sqlite3`**（数据库）。
4. `sqlite3` 的 Python 绑定需要加载系统/环境中的 **`libsqlite3.so`**。
5. **`libsqlite3` 编译时链接了 `icu` 库**（为了支持数据库中的字符串排序和搜索）。
6. 系统试图加载 `libicui18n.so.78`（这是 ICU 的一部分）。
7. 由于这个 `so.78` 是用较新的 C++ 标准编译的，而你的系统 `libstdc++.so` 版本太老，于是就崩了。

## 解决方案

降级 `icu` 到 Ubuntu 22.04 默认版本。

首先查看默认版本：

```bash
apt list --installed | grep icu
```

输出如下：

```
icu-devtools/jammy,now 70.1-2 amd64 [installed,automatic]
libharfbuzz-icu0/jammy-security,jammy-updates,now 2.7.4-1ubuntu3.2 amd64 [installed,automatic]
libicu-dev/jammy,now 70.1-2 amd64 [installed,automatic]
libicu70/jammy,now 70.1-2 amd64 [installed,automatic]
```

可以看到默认版本是 70.1。
因此需要将当前环境中的 `icu` 降级到 70.1：

```bash
conda install icu=70.1
```

> [!TIP]
> 可以使用 `conda search icu` 来查看可用版本。  
> `conda` 太慢了，可以使用 `mamba search icu`