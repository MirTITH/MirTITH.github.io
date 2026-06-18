# 关于页「项目与竞赛经历」卡片化设计文档

**日期**：2026-06-18
**目标**：将关于页（`content/about/index.md`）的「科研与项目」和「竞赛」两节合并为「项目与竞赛经历」，以卡片网格呈现，卡片内嵌可播放的本地视频或图片。

## 背景

- 站点为 Hugo + Hextra（v0.11.1），关于页见 [content/about/index.md](../../../content/about/index.md)。
- 现状：关于页「科研与项目」（2 条 bullet）与「竞赛」（1 条 bullet）为纯文本列表。
- Hextra 原生 `card` shortcode 支持 `image`/`link`/`tag`，但**不支持内嵌可播放视频**，故需自定义 shortcode。
- 素材位于 `temp/`：视频 `4倍速长序列操作.mp4`（30MB）、`VID_20260121_200147.mp4`（31MB）；图片 `ACG.GY_17.jpg`、`ACG.GY_18.jpg`、`ACG.GY_24.jpg`。**当前为占位素材**。

## 已确认的设计决策

| 维度 | 决策 |
|---|---|
| 分区 | 合并为单个二级分区「项目与竞赛经历」；「实习」分区保持不变 |
| 布局 | 多列响应式网格（桌面 2–3 列，小屏单列） |
| 卡片媒体 | 视频用浏览器原生 `<video controls>`，默认**暂停在第一帧**，点击原生控件播放；竞赛用图片 |
| 视频来源 | 本地 mp4 |
| 视频处理 | ffmpeg 压缩到 720p、单个 <5MB；图片压缩到 ~800px |
| 素材入库 | **不入库**：`static/videos/`、`static/images/proj/`、`temp/` 加入 `.gitignore`（占位素材仅本地预览） |
| 降级 | 媒体缺失时卡片仍正常渲染（标题+描述，媒体区空），不报错、不裂图 |
| 条目 | 科研 2 + 竞赛 3，共 5 张卡片 |
| 实现方式 | 新增 2 个自定义 shortcode，复用 Hextra 样式，不引入额外 JS/依赖 |

## 详细设计

### 1. 自定义 shortcode

**`layouts/shortcodes/media-cards.html`**（网格容器）
- 用 Hextra 的网格样式类包裹多张 `media-card`，响应式多列、小屏折叠。
- 渲染内部 `.Inner` 内容。

**`layouts/shortcodes/media-card.html`**（单张卡片）
- 命名参数：
  - `title`（必填）：卡片标题。
  - `tag`（可选）：右上角状态角标（如「国一」「本科毕设」）。
  - `video`（可选）：本地 mp4 路径（如 `/videos/dual-arm.mp4`）。
  - `image`（可选）：本地图片路径（如 `/images/proj/smartcar.jpg`）。
  - `poster`（可选）：视频封面图路径；不提供则浏览器显示视频第一帧。
- 媒体区渲染逻辑：
  - 有 `video` → `<video controls preload="metadata" playsinline poster="{{ .poster }}">`（无 autoplay、无 muted，默认停第一帧）。
  - 否则有 `image` → `<img>`。
  - 都没有 → 媒体区留空（降级）。
- 媒体下方：标题（加粗）+ `.Inner`（shortcode 包裹的 Markdown 描述要点）。
- 媒体统一固定宽高比（如 16:9）裁切，保证网格对齐。
- 卡片外观复用 Hextra 卡片样式类（圆角、边框、阴影），与站点统一。

### 2. 素材处理（本地，不入库）

| 卡片 | 源（temp/） | 目标 | 处理 |
|---|---|---|---|
| 具身智能双臂移动机器人 | `4倍速长序列操作.mp4` | `static/videos/dual-arm.mp4` | ffmpeg 720p，<5MB |
| 复杂环境机械臂自主避障与抓取 | `VID_20260121_200147.mp4` | `static/videos/grasping.mp4` | ffmpeg 720p，<5MB |
| 全国大学生智能车竞赛 | `ACG.GY_17.jpg` | `static/images/proj/smartcar.jpg` | 压缩到 ~800px |
| ROBOCON | `ACG.GY_18.jpg` | `static/images/proj/robocon.jpg` | 压缩到 ~800px |
| 深圳灵巧手大赛 | `ACG.GY_24.jpg` | `static/images/proj/dexhand.jpg` | 压缩到 ~800px |

### 3. 关于页内容改动

将现有「### 科研与项目」与「### 竞赛」两节，替换为：

```
## 项目与竞赛经历

{{< media-cards >}}
  {{< media-card title="具身智能双臂移动机器人" video="/videos/dual-arm.mp4" >}}
导师组具身智能科研平台核心软硬件开发：机械臂 / 灵巧手 ROS 2 驱动、运动控制与自主移动抓取。
  {{< /media-card >}}
  {{< media-card title="复杂环境机械臂自主避障与抓取" tag="本科毕设" video="/videos/grasping.mp4" >}}
独立完成手眼标定、运动学解算、避障规划与抓取位姿生成，实机平均抓取成功率超过 80%。
  {{< /media-card >}}
  {{< media-card title="全国大学生智能车竞赛" tag="国一" image="/images/proj/smartcar.jpg" >}}
双车接力组别：基于 RT-Thread 的多线程实时系统 + 双环 PID 控制，全国总决赛一等奖。
  {{< /media-card >}}
  {{< media-card title="ROBOCON 全国大学生机器人大赛" tag="三等奖" image="/images/proj/robocon.jpg" >}}
双机器人协作系统：底盘运动学解算、IMU 稳定与激光测距定位，实现全向移动与精准定位。
  {{< /media-card >}}
  {{< media-card title="深圳市智能机器人灵巧手大赛" tag="卓越精准操作奖" image="/images/proj/dexhand.jpg" >}}
双臂移动机器人：结合滤波、自适应柔顺控制与 MPC，实现力接触安全遥操作与数据采集。
  {{< /media-card >}}
{{< /media-cards >}}
```

「实习」「技能」「联系方式」等其余分区不变。

### 4. .gitignore

新增：
```
temp/
static/videos/
static/images/proj/
```

## 文件改动总览

| 文件 | 改动 |
|---|---|
| `layouts/shortcodes/media-cards.html` | 新建（网格容器） |
| `layouts/shortcodes/media-card.html` | 新建（单卡片，视频/图片/降级） |
| `static/videos/dual-arm.mp4`、`grasping.mp4` | 新建（压缩，**不入库**） |
| `static/images/proj/smartcar.jpg`、`robocon.jpg`、`dexhand.jpg` | 新建（压缩，**不入库**） |
| `content/about/index.md` | 合并两节为「项目与竞赛经历」卡片网格 |
| `.gitignore` | 增加 `temp/`、`static/videos/`、`static/images/proj/` |

## 验收标准

- `hugo` 构建无 error。
- 本地 `hugo server`：关于页出现「项目与竞赛经历」分区，5 张卡片成网格排列。
- 视频卡片渲染 `<video controls>`，默认停在第一帧，点击播放正常；图片卡片正常显示。
- 桌面多列、小屏单列（缩窄浏览器窗口验证）。
- 删除某个媒体文件后重建，对应卡片仍正常渲染标题与描述，无裂图/报错（降级验证）。
- `git status` 中 `static/videos/`、`static/images/proj/`、`temp/` 不出现（已被忽略）。
- 提交内容仅含 shortcode、关于页文本、`.gitignore`，不含媒体二进制文件。

## 不做的事（YAGNI）

- 不做悬停自动播放、自定义播放器 UI（采用浏览器原生控件）。
- 不引入第三方视频库、灯箱（lightbox）或额外 JS 依赖。
- 不将占位媒体文件提交入库（日后替换为正式素材后再决定）。
- 不改动「实习」「技能」「联系方式」等其他分区。
