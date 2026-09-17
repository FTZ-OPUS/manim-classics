# FTZ · Manim 经典数学动画源码合集

这里收录了我挑选的 13 份 Manim 数学动画源码：从高节奏公式混剪，到线性代数、概率论、几何推导和视频逆向复刻。欢迎下载、阅读，也欢迎把代码交给你的 AI，继续制作属于自己的数学动画。

本合集侧重源代码和制作思路，包含横屏公式卡片、动态函数图、彩色矩阵、简笔叙事和竖屏 3D 几何等不同表现形式。源码保留了原始文件名与内容；文件中的“复刻”“还原”及播放量描述沿用原稿，并非额外的独立验证结果。

## 下载

- [下载整个源码合集 ZIP](https://github.com/FTZ-OPUS/manim-classics/archive/refs/heads/main.zip)
- [我的 GitHub 主页](https://github.com/FTZ-OPUS)
- [AI 技能与教程合集](https://github.com/FTZ-OPUS/SKIll)
- [公式混剪 Manim Skill](https://github.com/FTZ-OPUS/formula-mixcut-manim-skill)

## 作品目录

| 作品 / 源码 | Manim 场景名 | 内容 |
| --- | --- | --- |
| [圆锥曲线结论混剪](dy5%E4%B8%87%E6%92%AD%E6%94%BE%E5%9C%86%E9%94%A5%E6%9B%B2%E7%BA%BF%E7%BB%93%E8%AE%BA%E6%B7%B7%E5%89%AA.py) | `ConicMixCut` | 圆锥曲线定义、性质与公式卡片形变混剪 |
| [复变函数邪修进阶之路](%E5%A4%8D%E5%8F%98%E5%87%BD%E6%95%B0%E9%82%AA%E4%BF%AE%E8%BF%9B%E9%98%B6%E4%B9%8B%E8%B7%AF.py) | `ComplexMix` | 复变函数公式与动态彩色函数图双层混剪 |
| [概率论混剪](%E6%A6%82%E7%8E%87%E8%AE%BA%E6%B7%B7%E5%89%AA.py) | `ProbMixCut` | 概率统计公式、条件概率与贝叶斯等知识卡片 |
| [立体几何邪修之路](%E7%AB%8B%E4%BD%93%E5%87%A0%E4%BD%95.py) | `LitiGod` | 36 张公式与绘图双层卡片，使用伪 3D 投影 |
| [我曾九次认识世界](%E6%88%91%E6%9B%BE%E4%B9%9D%E6%AC%A1%E8%AE%A4%E8%AF%86%E4%B8%96%E7%95%8C_%E8%BF%98%E5%8E%9F%E7%89%88.py) | `NineWorlds` | 星空壁纸层、九张动态数学卡片与公式形变转场 |
| [若尔当标准型](jordan%E6%A0%87%E5%87%86.py) | `JordanRemix` | 米白网格、彩色矩阵与分段讲解的复刻动画 |
| [有理标准型](%E6%9C%89%E7%90%86%E6%A0%87%E5%87%86%E5%9E%8B_%E5%90%8Cjordan%E9%A3%8E%E6%A0%BC%E7%89%88%E6%BA%90%E7%A0%81.py) | `RationalForm` | 友矩阵、不变因子与有理标准型，延续矩阵讲解风格 |
| [哈密顿–凯莱定理](%E5%93%88%E5%AF%86%E9%A1%BF%E5%87%AF%E8%8E%B1.py) | `CHVideo` | 矩阵函数、相似不变性与摄动法证明；需额外 common.py |
| [弱大数定律](%E5%A4%A7%E6%95%B0%E5%AE%9A%E5%BE%8B.py) | `WeakLawOfLargeNumbers` | 黑底大字的概率论逐步讲解 |
| [梯度与偏导数估计](%E6%A2%AF%E5%BA%A6.py) | `GradientBoundProofExtended` | 多元函数偏导数估计与极值定位 |
| [不等式凑 1:16](%E4%B8%8D%E7%AD%89%E5%BC%8F%E5%87%911%3A16.py) | `WangBaoReply` | 米白纸面、彩色圆角框和简笔叙事动画 |
| [埃尔伯格悖论](%E5%9F%83%E5%B0%94%E4%BC%AF%E6%A0%BC%E6%82%96%E8%AE%BA_.py) | `EllsbergRemake` | 两罐实验、逻辑矛盾与模糊厌恶的分段复刻 |
| [甜甜圈体积推导](%E7%94%9C%E7%94%9C%E5%9C%88%E4%BD%93%E7%A7%AF%E6%8E%A8%E5%AF%BC_%E5%A4%8D%E5%88%BB%E6%BA%90%E7%A0%81.py) | `TorusVolume` | 竖屏 3D 环面与帕普斯定理；需额外封面图片 |

## 如何运行

源码主要使用 Manim Community 与 NumPy。部分原稿标注了 Manim CE 0.21 / 0.21.0；实际兼容性请以你的渲染环境为准。公式排版通常还需要 LaTeX，视频输出需要 FFmpeg。

```bash
python -m pip install manim numpy
```

在解压后的仓库目录运行，先用低画质预览：

```bash
python -m manim -ql "我曾九次认识世界_还原版.py" NineWorlds
python -m manim -ql "复变函数邪修进阶之路.py" ComplexMix
python -m manim -ql "jordan标准.py" JordanRemix
```

将文件名和场景名替换成上表对应项即可。需要高画质时可将 `-ql` 换成 `-qh`；分辨率、帧率和横竖屏也可能由各源码里的 `config` 设置指定。

### 中文字体

多份源码使用 macOS 字体，如 `Kaiti SC`、`Songti SC`、`PingFang SC`、`Hiragino Sans GB`。在其他系统上运行时，请将相应字体常量替换成已安装的中文字体。

### 已知依赖与本机路径

- **哈密顿凯莱.py** 使用 `from common import *` 和 `BaseScene`。原始分享文件夹未包含 `common.py`，因此这份源码目前不能独立渲染，需补齐原项目的公共模块。
- **甜甜圈体积推导_复刻源码.py** 的 `stage_cover()` 引用了原机器上的 `cover.png`，封面不在原始分享文件夹中。运行前需提供封面并改成自己的路径，或调整封面段；后续 3D 环面绘制由代码完成。
- **不等式凑1:16.py** 设置了原机器的绝对 `config.media_dir` 路径。请改成自己的输出目录或 `media`。
- 发布时已对全部 13 份 Python 文件进行静态语法解析，并核对发布副本与原文件一致；未逐份完整渲染，视觉效果与运行成功仍需在对应环境中验证。

## 交给 AI 使用

将感兴趣的源码与本 README 一起提供给 AI，说明你想修改的知识点、配色、节奏、画幅和输出分辨率。保留动画的场景结构与可复用组件，让 AI 先处理字体和依赖，再预览渲染、检查画面，最后输出成品。
