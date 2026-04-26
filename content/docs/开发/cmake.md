---
title: CMake
type: docs
---

## `find_package()`

### 示例

```cmake
find_package(fmt 10.2.1 REQUIRED)
target_link_libraries(YOUR_TARGET fmt::fmt)
```

- `fmt`：包名
- `10.2.1`：最小要求版本
- `REQUIRED`：表示 CMake 必须找到该包，否则停止构建

如果库本身的 CMake 配置写得足够规范，通常这两步就足够完成依赖接入。

## 库的搜索路径

```cmake
# 这些是 find_package() 的一部分搜索路径
# 这里只列出常见变量，完整机制请参考官方文档
# ${CMAKE_PREFIX_PATH} 是 CMake 变量
# $ENV{CMAKE_PREFIX_PATH} 是 shell 环境变量

message("CMAKE_PREFIX_PATH: ${CMAKE_PREFIX_PATH}")
message("CMAKE_FRAMEWORK_PATH: ${CMAKE_FRAMEWORK_PATH}")
message("CMAKE_APPBUNDLE_PATH: ${CMAKE_APPBUNDLE_PATH}")

message("CMAKE_PREFIX_PATH env: $ENV{CMAKE_PREFIX_PATH}")
message("CMAKE_FRAMEWORK_PATH env: $ENV{CMAKE_FRAMEWORK_PATH}")
message("CMAKE_APPBUNDLE_PATH env: $ENV{CMAKE_APPBUNDLE_PATH}")

message("PATH env: $ENV{PATH}")

message("CMAKE_SYSTEM_PREFIX_PATH: ${CMAKE_SYSTEM_PREFIX_PATH}")
message("CMAKE_SYSTEM_FRAMEWORK_PATH: ${CMAKE_SYSTEM_FRAMEWORK_PATH}")
message("CMAKE_SYSTEM_APPBUNDLE_PATH: ${CMAKE_SYSTEM_APPBUNDLE_PATH}")

message("CMAKE_FIND_ROOT_PATH: ${CMAKE_FIND_ROOT_PATH}")
```

官方文档：<https://cmake.org/cmake/help/latest/command/find_package.html>