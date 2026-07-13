# 关于页「项目与竞赛经历」卡片化 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将关于页的「科研与项目」与「竞赛」两节合并为「项目与竞赛经历」卡片网格，卡片内嵌可播放的本地视频（原生 `<video controls>`，默认停第一帧）或图片。

**Architecture:** 新增两个自定义 Hugo shortcode（`media-cards` 网格容器 + `media-card` 单卡片），复用 Hextra v0.11.1 既有的网格 CSS 类，不引入额外 JS/依赖。占位媒体经 ffmpeg/ImageMagick 压缩到 `static/` 下，但通过 `.gitignore` 排除入库；shortcode 在媒体缺失时优雅降级。

**Tech Stack:** Hugo v0.163（extended）、Hextra 主题 v0.11.1、ffmpeg（libx264）、ImageMagick（`magick`）。

---

## File Structure

| 文件 | 责任 |
|---|---|
| `layouts/shortcodes/media-cards.html` | 网格容器：复用 Hextra grid 类包裹多张卡片 |
| `layouts/shortcodes/media-card.html` | 单卡片：渲染视频/图片/降级 + 标题 + 描述 |
| `static/videos/dual-arm.mp4`、`grasping.mp4` | 压缩后的占位视频（**不入库**） |
| `static/images/proj/smartcar.jpg`、`robocon.jpg`、`dexhand.jpg` | 压缩后的占位图（**不入库**） |
| `content/about/index.md` | 合并两节为「项目与竞赛经历」卡片网格 |
| `.gitignore` | 排除 `temp/`、`static/videos/`、`static/images/proj/` |

**复用的 Hextra 网格类**（取自当前构建产物，确保视觉一致）：
`hextra-feature-grid hx:grid hx:sm:max-lg:grid-cols-2 hx:max-sm:grid-cols-1 hx:gap-4 hx:w-full not-prose`

---

### Task 1: 先用 .gitignore 排除媒体目录

先做忽略规则，确保后续生成的媒体二进制不会被误提交。

**Files:**
- Modify: `.gitignore`

- [ ] **Step 1: 查看现有 .gitignore**

Run:
```bash
cd /home/nros/Documents/MirTITH.github.io
cat .gitignore
```
Expected: 显示现有内容（已含 `public` 等）。

- [ ] **Step 2: 追加忽略规则**

将以下三行追加到 `.gitignore` 末尾（保留原有内容不变）：
```
temp/
static/videos/
static/images/proj/
```

- [ ] **Step 3: 验证忽略生效**

Run:
```bash
cd /home/nros/Documents/MirTITH.github.io
mkdir -p static/videos static/images/proj
touch static/videos/_t.mp4 static/images/proj/_t.jpg
git check-ignore temp/ static/videos/_t.mp4 static/images/proj/_t.jpg
rm -f static/videos/_t.mp4 static/images/proj/_t.jpg
```
Expected: 三个路径都被打印（说明已被忽略）。

- [ ] **Step 4: Commit**

```bash
cd /home/nros/Documents/MirTITH.github.io
git add .gitignore
git commit -m "忽略占位媒体目录（temp、static/videos、static/images/proj）"
```

---

### Task 2: 生成网格容器 shortcode `media-cards.html`

**Files:**
- Create: `layouts/shortcodes/media-cards.html`

- [ ] **Step 1: 创建 `layouts/shortcodes/media-cards.html`**

完整写入：
```go-html-template
{{/* 项目/竞赛卡片网格容器，复用 Hextra feature-grid 样式 */}}
<div class="hextra-feature-grid hx:grid hx:sm:max-lg:grid-cols-2 hx:max-sm:grid-cols-1 hx:gap-4 hx:w-full not-prose hx:my-6">
  {{ .Inner }}
</div>
```

- [ ] **Step 2: 提交（容器单独可提交）**

```bash
cd /home/nros/Documents/MirTITH.github.io
git add layouts/shortcodes/media-cards.html
git commit -m "新增 media-cards 网格容器 shortcode"
```

---

### Task 3: 生成单卡片 shortcode `media-card.html`

**Files:**
- Create: `layouts/shortcodes/media-card.html`

- [ ] **Step 1: 创建 `layouts/shortcodes/media-card.html`**

完整写入。逻辑：有 `video` 渲染原生 `<video controls preload="metadata" playsinline>`（默认停第一帧，可选 `poster`）；否则有 `image` 渲染 `<img>`；都没有则媒体区不渲染（降级）。媒体区固定 16:9 比例。

```go-html-template
{{/* 单张项目/竞赛卡片：媒体（视频或图片，可降级）+ 标题 + 描述 */}}
{{ $title := .Get "title" }}
{{ $tag := .Get "tag" }}
{{ $video := .Get "video" }}
{{ $image := .Get "image" }}
{{ $poster := .Get "poster" }}
<div class="hextra-card hx:border hx:border-gray-200 hx:dark:border-neutral-800 hx:rounded-xl hx:overflow-hidden hx:bg-transparent">
  {{ if $video }}
  <div style="position: relative; width: 100%; aspect-ratio: 16 / 9; background: #000;">
    <video controls preload="metadata" playsinline{{ with $poster }} poster="{{ . }}"{{ end }}
           style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover;">
      <source src="{{ $video }}" type="video/mp4" />
    </video>
  </div>
  {{ else if $image }}
  <div style="width: 100%; aspect-ratio: 16 / 9; overflow: hidden;">
    <img src="{{ $image }}" alt="{{ $title }}" loading="lazy"
         style="width: 100%; height: 100%; object-fit: cover;" />
  </div>
  {{ end }}
  <div class="hx:p-4">
    <div style="display: flex; align-items: center; justify-content: space-between; gap: 0.5rem;">
      <span class="hx:font-semibold hx:text-gray-800 hx:dark:text-gray-100">{{ $title }}</span>
      {{ with $tag }}<span class="hx:text-xs hx:rounded hx:px-2 hx:py-0.5 hx:bg-primary-100 hx:dark:bg-primary-900 hx:text-primary-700 hx:dark:text-primary-300 hx:whitespace-nowrap">{{ . }}</span>{{ end }}
    </div>
    <div class="hx:mt-2 hx:text-sm hx:text-gray-600 hx:dark:text-gray-400">
      {{ .Inner | markdownify }}
    </div>
  </div>
</div>
```

- [ ] **Step 2: 提交**

```bash
cd /home/nros/Documents/MirTITH.github.io
git add layouts/shortcodes/media-card.html
git commit -m "新增 media-card 单卡片 shortcode（视频/图片/降级）"
```

---

### Task 4: 替换关于页内容为卡片网格

先用卡片结构替换文本（此时媒体文件尚未生成，正好验证降级渲染）。

**Files:**
- Modify: `content/about/index.md`

- [ ] **Step 1: 替换「科研与项目」与「竞赛」两节**

打开 `content/about/index.md`，将下列原内容：
```markdown
### 科研与项目

- **具身智能双臂移动机器人**（2024.07 – 至今）
  搭建导师组具身智能科研平台，负责机械臂 / 灵巧手 ROS 2 驱动、运动控制与自主移动抓取算法。
- **复杂环境下机械臂自主避障与自主抓取**（本科毕业设计）
  独立完成驱动适配、手眼标定、运动学解算、避障规划与抓取位姿生成，实机平均抓取成功率超过 80%。

### 竞赛

- **全国大学生智能车竞赛** · 全国总决赛一等奖、RT-Thread 创新专项奖（2021）
```

整体替换为（注意：保持三级标题 `###`，与同属 `## 精选经历` 下的 `### 实习` 同级；当前文档结构为 `## 精选经历` → `### 实习` / `### 科研与项目` / `### 竞赛`，替换后变为 `### 实习` / `### 项目与竞赛经历`）：
```markdown
### 项目与竞赛经历

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

文档结构：`## 精选经历` 下保留 `### 实习`，其后接新的 `### 项目与竞赛经历`（替换原 `### 科研与项目` 与 `### 竞赛` 两节）。`## 技能`、`## 联系方式` 等不变。

- [ ] **Step 2: 构建并验证降级渲染（媒体尚不存在）**

Run:
```bash
cd /home/nros/Documents/MirTITH.github.io
hugo --cleanDestinationDir 2>&1 | grep -i error || echo "BUILD CLEAN"
echo "=== 分区标题 ==="; grep -c "项目与竞赛经历" public/about/index.html
echo "=== 5 张卡片标题 ==="; grep -oE "具身智能双臂移动机器人|复杂环境机械臂自主避障与抓取|全国大学生智能车竞赛|ROBOCON|深圳市智能机器人灵巧手大赛" public/about/index.html | sort -u | wc -l
echo "=== 网格容器类 ==="; grep -c "hextra-feature-grid" public/about/index.html
echo "=== 视频标签 ==="; grep -c "<video" public/about/index.html
echo "=== 角标文案 ==="; grep -oE "国一|三等奖|卓越精准操作奖|本科毕设" public/about/index.html | sort -u | wc -l
```
Expected: `BUILD CLEAN`；分区标题 ≥ 1；卡片标题去重计数 = 5；网格容器 ≥ 1（关于页现在有了 grid）；`<video` = 2；角标去重计数 = 4。

- [ ] **Step 3: Commit（卡片结构 + 文本，永久入库）**

```bash
cd /home/nros/Documents/MirTITH.github.io
git add content/about/index.md
git commit -m "关于页：科研与竞赛合并为「项目与竞赛经历」卡片网格"
```

---

### Task 5: 生成压缩后的占位媒体（本地，不入库）

**Files:**
- Create（不入库）: `static/videos/dual-arm.mp4`、`static/videos/grasping.mp4`
- Create（不入库）: `static/images/proj/smartcar.jpg`、`robocon.jpg`、`dexhand.jpg`

- [ ] **Step 1: 转码视频 1（H.264 720p，目标 <5MB）**

源 36.8s / 1080p / H.264。720p、CRF 28、限速、faststart。

Run:
```bash
cd /home/nros/Documents/MirTITH.github.io
mkdir -p static/videos static/images/proj
ffmpeg -y -i "temp/4倍速长序列操作.mp4" \
  -vf "scale=-2:720" -c:v libx264 -crf 28 -maxrate 1500k -bufsize 3000k \
  -preset veryfast -movflags +faststart -c:a aac -b:a 96k \
  static/videos/dual-arm.mp4
du -h static/videos/dual-arm.mp4
```
Expected: 生成成功，体积 < 5MB。若 ≥ 5MB，将 `-crf` 提高到 30 重试。

- [ ] **Step 2: 转码视频 2（H.265→H.264 720p，目标 <5MB）**

源 18.7s / 1080p / **H.265** → 必须转 H.264。

Run:
```bash
cd /home/nros/Documents/MirTITH.github.io
ffmpeg -y -i "temp/VID_20260121_200147.mp4" \
  -vf "scale=-2:720" -c:v libx264 -crf 28 -maxrate 2000k -bufsize 4000k \
  -preset veryfast -movflags +faststart -c:a aac -b:a 96k \
  static/videos/grasping.mp4
du -h static/videos/grasping.mp4
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,height -of default=noprint_wrappers=1 static/videos/grasping.mp4
```
Expected: 体积 < 5MB；`codec_name=h264`、`height=720`（确认已转 H.264 且为 720p）。

- [ ] **Step 3: 压缩三张竞赛图片到 ~800px**

Run:
```bash
cd /home/nros/Documents/MirTITH.github.io
magick temp/ACG.GY_17.jpg -resize 800x -strip -quality 82 static/images/proj/smartcar.jpg
magick temp/ACG.GY_18.jpg -resize 800x -strip -quality 82 static/images/proj/robocon.jpg
magick temp/ACG.GY_24.jpg -resize 800x -strip -quality 82 static/images/proj/dexhand.jpg
du -h static/images/proj/*.jpg
```
Expected: 三个文件生成，每个体积明显减小（典型 < 200KB）。

- [ ] **Step 4: 确认媒体未被 git 跟踪**

Run:
```bash
cd /home/nros/Documents/MirTITH.github.io
git status --short
```
Expected: 输出中**不含** `static/videos/` 或 `static/images/proj/` 下的文件（已被 Task 1 的忽略规则排除）。工作区应为干净或仅含未追踪的被忽略项（不显示）。

---

### Task 6: 整体验收（本地播放 + 降级 + 响应式）

**Files:** 无（仅验证）

- [ ] **Step 1: 构建并冒烟检查媒体已被引用且可访问**

Run:
```bash
cd /home/nros/Documents/MirTITH.github.io
hugo --cleanDestinationDir >/dev/null 2>&1
timeout 15 hugo server --disableFastRender >/tmp/hugo-cards.log 2>&1 &
sleep 8
echo "=== about 分区 ==="; curl -s localhost:1313/about/ | grep -c "项目与竞赛经历"
echo "=== video 标签数 ==="; curl -s localhost:1313/about/ | grep -c "<video"
echo "=== 视频文件可访问 ==="; curl -s -o /dev/null -w "%{http_code}\n" localhost:1313/videos/dual-arm.mp4
echo "=== 图片可访问 ==="; curl -s -o /dev/null -w "%{http_code}\n" localhost:1313/images/proj/smartcar.jpg
wait 2>/dev/null
```
Expected: 分区 ≥ 1；`<video` = 2；视频与图片均返回 `200`。

- [ ] **Step 2: 降级验证（删除一个媒体文件后卡片仍正常）**

Run:
```bash
cd /home/nros/Documents/MirTITH.github.io
mv static/videos/dual-arm.mp4 /tmp/dual-arm.bak.mp4
hugo --cleanDestinationDir 2>&1 | grep -i error || echo "BUILD CLEAN (degraded)"
grep -c "具身智能双臂移动机器人" public/about/index.html
mv /tmp/dual-arm.bak.mp4 static/videos/dual-arm.mp4
hugo --cleanDestinationDir >/dev/null 2>&1
```
Expected: `BUILD CLEAN (degraded)`；标题计数 ≥ 1（即使视频文件缺失，卡片标题/描述仍渲染，无报错）。注意：`<video>` 的 `src` 仍会指向缺失文件，浏览器显示空播放器但不崩溃——这是预期的降级行为（媒体是本地占位、不入库）。

- [ ] **Step 3: 确认提交历史与工作区干净**

Run:
```bash
cd /home/nros/Documents/MirTITH.github.io
git status --short
git log --oneline -5
```
Expected: 工作区干净（无媒体二进制待提交）；最近提交包含 `.gitignore`、两个 shortcode、关于页改动。

---

## Self-Review

**1. Spec coverage:**
- 合并为「项目与竞赛经历」单分区 → Task 4 ✓
- 多列响应式网格 → Task 2（复用 Hextra grid 类，含 `sm:max-lg:grid-cols-2`、`max-sm:grid-cols-1`）✓
- 原生 `<video controls>` 默认停第一帧、可选 poster → Task 3 ✓
- 竞赛用图片 → Task 3（`image` 分支）+ Task 4 ✓
- 视频 720p / H.264 / faststart / <5MB；H.265→H.264 → Task 5 Step 1-2 ✓
- 图片 ~800px → Task 5 Step 3 ✓
- 素材不入库（gitignore temp/videos/images） → Task 1 + Task 5 Step 4 ✓
- 媒体缺失降级 → Task 3（无媒体不渲染媒体区）+ Task 6 Step 2 ✓
- 科研 2 + 竞赛 3 共 5 卡 → Task 4 ✓
- 不引入额外 JS/依赖 → 全程纯 shortcode + 原生标签 ✓
- 验收标准（构建无错、网格、播放、降级、gitignore） → Task 6 ✓

**2. Placeholder scan:** 无 TBD/TODO。Task 4 已按关于页实际层级（`## 精选经历` → `### 实习` / `### 科研与项目` / `### 竞赛`）明确为 `### 项目与竞赛经历`，无条件分支、无占位。

**3. Type/路径一致性:** shortcode 参数名 `title`/`tag`/`video`/`image`/`poster` 在 Task 3 定义、Task 4 使用，一致；媒体路径 `/videos/*.mp4`、`/images/proj/*.jpg` 在 Task 4（引用）与 Task 5（生成到 `static/videos`、`static/images/proj`）一致；网格类字符串与 Task 2 容器一致。
