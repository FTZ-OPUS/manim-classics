# -*- coding: utf-8 -*-
"""
弱大数定律 (Weak Law of Large Numbers) — Manim CE 横屏大字动画
=================================================================
渲染命令:
    manim wlln_animation.py WeakLawOfLargeNumbers -ql     # 480p 预览
    manim wlln_animation.py WeakLawOfLargeNumbers -qh     # 1080p60 高清

仅依赖 manim 与 numpy，无音频。
"""

from manim import *
import numpy as np

# ---------------- 全局配置：16:9 横屏 ----------------
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16.0
config.frame_height = 9.0

# ---------------- 配色（黑底高对比护眼） ----------------
BG      = "#0B121B"   # 近纯黑深蓝底
INK     = "#F6F2EA"   # 暖白正文
MUTED   = "#A9B4C2"   # 灰字辅助
BLUE    = "#5DADEC"
GREEN   = "#66D19E"
YELLOW  = "#FFD166"
ORANGE  = "#F59E62"
RED     = "#FF6B6B"
VIOLET  = "#B79CFF"
CARD_BG = "#121D2B"
READ_PAUSE = 1.6

ZH_FONT = "Kaiti SC"  # macOS 楷体；Windows 可改为 "KaiTi"

# ---------------- 可调参数：总体分布（改这里即可换分布） ----------------
DISTRIBUTIONS = [
    dict(
        title="六、数值仿真：抛硬币实验",
        tex=r"\mathrm{Bernoulli}(p=0.5)",
        sampler=lambda rng, n: rng.binomial(1, 0.5, size=n),
        mu=0.5,
        mu_tex=r"\mu = 0.5",
        y_range=[0.0, 1.0, 0.25],
        y_fixed=True,
        curve_color=GREEN,
        seed=7,
    ),
    dict(
        title="七、更换总体分布：指数分布",
        tex=r"\mathrm{Exp}(\lambda=1)",
        sampler=lambda rng, n: rng.exponential(1.0, size=n),
        mu=1.0,
        mu_tex=r"\mu = 1",
        y_range=None,          # None = 按数据自动确定纵轴范围
        y_fixed=False,
        curve_color=BLUE,
        seed=11,
    ),
]


class WeakLawOfLargeNumbers(Scene):
    # ================= 辅助方法（遵循排版规范） =================
    def zh(self, content, font_size=42, color=INK, weight=NORMAL):
        return Text(content, font=ZH_FONT, font_size=font_size,
                    color=color, weight=weight)

    def mt(self, content, font_size=56, color=INK, stroke_width=1):
        return MathTex(content, font_size=font_size, color=color,
                       stroke_width=stroke_width)

    def mt_small(self, content, font_size=50, color=INK):
        return self.mt(content, font_size=font_size, color=color)

    def mixed(self, *items, text_size=38, math_size=44, buff=0.08):
        parts = []
        for kind, content, color in items:
            if kind == "text":
                parts.append(self.zh(content, font_size=text_size, color=color))
            else:
                parts.append(self.mt(content, font_size=math_size, color=color))
        return VGroup(*parts).arrange(RIGHT, buff=buff)

    def fit(self, mob, width=None, height=None):
        target_width = width if width is not None else config.frame_width - 1.2
        target_height = height if height is not None else config.frame_height - 1.0
        if mob.width > target_width:
            mob.scale_to_fit_width(target_width)
        if mob.height > target_height:
            mob.scale_to_fit_height(target_height)
        return mob

    def title_bar(self, text, color=BLUE):
        title = self.zh(text, font_size=52, color=color, weight=BOLD)
        title.to_edge(UP, buff=0.38)
        return VGroup(title)

    def layout_below(self, bar, *lines, centered=False):
        """标题栏下方均匀分布内容行，每页不超过 4 行"""
        n = len(lines)
        for line in lines:
            self.fit(line, width=config.frame_width - 1.2)
        if n <= 2:
            buff = 1.1
        elif n == 3:
            buff = 0.95
        else:
            buff = 0.78
        if centered:
            content = VGroup(*lines).arrange(DOWN, buff=buff)
        else:
            content = VGroup(*lines).arrange(DOWN, buff=buff, aligned_edge=LEFT)
        content.next_to(bar, DOWN, buff=0.7)
        return content

    def wait_formula(self):
        self.wait(READ_PAUSE)

    def write_formula(self, mob, run_time=0.9):
        self.play(Write(mob), run_time=run_time)
        self.wait_formula()

    def write_text(self, mob, run_time=0.75):
        self.play(Write(mob), run_time=run_time)

    def fade_line(self, mob, run_time=0.8, hold=True):
        """公式逐行淡入浮现"""
        self.play(FadeIn(mob, shift=UP * 0.25), run_time=run_time)
        if hold:
            self.wait(READ_PAUSE)

    def chip(self, text, color):
        t = self.zh(text, font_size=25, color=color)
        box = SurroundingRectangle(t, color=color, buff=0.13, stroke_width=1.6)
        return VGroup(box, t)

    def clear_scene(self):
        if self.mobjects:
            for mob in list(self.mobjects):
                try:
                    mob.clear_updaters()
                except Exception:
                    pass
            self.play(*[FadeOut(mob) for mob in list(self.mobjects)], run_time=0.5)

    # ================= 主流程 =================
    def construct(self):
        self.camera.background_color = BG
        self.opening()            # 彩色渐变大标题 + 动态采样引入
        self.concept_defs()       # 一、样本均值 vs 总体期望
        self.concept_theorem()    # 二、定理陈述
        self.meaning_scene()      # 三、物理含义
        self.proof_prep()         # 四、证明准备：两个关键矩
        self.proof_chebyshev()    # 五、切比雪夫不等式完成证明
        self.simulate(DISTRIBUTIONS[0])   # 六、抛硬币动态仿真
        self.simulate(DISTRIBUTIONS[1])   # 七、更换分布再验证
        self.caveat()             # 八、收敛 ≠ 单次准确
        self.summary_card()       # 九、总结卡片

    # ---------------- 开场：渐变大标题 + 动态采样引入 ----------------
    def opening(self):
        title = self.zh("弱大数定律", font_size=88, weight=BOLD)
        title.set_color_by_gradient(BLUE, GREEN, YELLOW)
        title.move_to([0.0, 3.1, 0])
        sub = self.zh("Weak Law of Large Numbers", font_size=27, color=MUTED)
        sub.next_to(title, DOWN, buff=0.22)
        chips = VGroup(
            self.chip("切比雪夫不等式", VIOLET),
            self.chip("依概率收敛", BLUE),
            self.chip("动态数值仿真", GREEN),
        ).arrange(RIGHT, buff=0.5)
        chips.next_to(sub, DOWN, buff=0.32)

        self.play(FadeIn(title, shift=DOWN * 0.5), run_time=0.9)
        self.play(FadeIn(sub, shift=UP * 0.2), run_time=0.5)
        self.play(
            LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in chips],
                        lag_ratio=0.25),
            run_time=0.9,
        )

        # --- 动态采样引入：抛硬币，双柱堆叠 + 频率游标 ---
        nl = NumberLine(
            x_range=[0, 1, 0.5], length=12.0,
            color=MUTED, stroke_width=2.5,
            include_numbers=False, include_tip=False,
        ).move_to([0, -1.9, 0])
        x_t = nl.number_to_point(0.0)[0]
        x_h = nl.number_to_point(1.0)[0]
        line_y = nl.number_to_point(0.5)[1]

        cap_h = self.zh("正面（计 1）", font_size=26, color=YELLOW)
        cap_h.move_to([x_h, line_y - 0.55, 0])
        cap_t = self.zh("背面（计 0）", font_size=26, color=BLUE)
        cap_t.move_to([x_t, line_y - 0.55, 0])

        unit_h = 2.6 / 96.0            # 每次投掷对应的柱高
        heads_t = ValueTracker(0.0)
        total_t = ValueTracker(0.0)

        def bar_heads_fn():
            h = max(0.02, heads_t.get_value() * unit_h)
            return Rectangle(width=0.8, height=h, stroke_width=0,
                             fill_color=YELLOW, fill_opacity=0.85
                             ).move_to([x_h, line_y + h / 2 - 0.02, 0])

        def bar_tails_fn():
            cnt = total_t.get_value() - heads_t.get_value()
            h = max(0.02, cnt * unit_h)
            return Rectangle(width=0.8, height=h, stroke_width=0,
                             fill_color=BLUE, fill_opacity=0.85
                             ).move_to([x_t, line_y + h / 2 - 0.02, 0])

        bar_head = always_redraw(bar_heads_fn)
        bar_tail = always_redraw(bar_tails_fn)

        def marker_fn():
            n = total_t.get_value()
            p = heads_t.get_value() / n if n > 0 else 0.5
            p = float(np.clip(p, 0.0, 1.0))
            pos = nl.number_to_point(p)
            tri = Triangle(radius=0.15, stroke_width=0,
                           fill_color=YELLOW, fill_opacity=1.0
                           ).rotate(PI).move_to(pos + UP * 0.3)
            num = DecimalNumber(p, num_decimal_places=2, font_size=30,
                                color=YELLOW).next_to(pos, DOWN, buff=0.75)
            return VGroup(tri, num)

        marker = always_redraw(marker_fn)

        self.play(Create(nl), FadeIn(cap_h), FadeIn(cap_t), run_time=0.9)
        # 常驻重绘的柱体与游标直接加入场景，避免参与插值动画
        self.add(bar_head, bar_tail, marker)

        rng = np.random.default_rng(1)   # 96 次后频率恰为 0.5，演示效果最佳
        batches, per = 8, 12           # 8 轮 x 12 次 = 96 次投掷
        for _ in range(batches):
            flips = rng.integers(0, 2, size=per)
            k = int(flips.sum())
            h_now = heads_t.get_value()
            t_now = total_t.get_value() - h_now
            dots, targets = [], []
            for f in flips:
                is_h = bool(f)
                x = x_h if is_h else x_t
                col = YELLOW if is_h else BLUE
                d = Dot(radius=0.09, stroke_width=0,
                        fill_color=col, fill_opacity=0.95)
                d.move_to([x + rng.uniform(-0.6, 0.6),
                           2.7 + rng.uniform(0.0, 0.7), 0])
                ty = line_y + (h_now if is_h else t_now) * unit_h + 0.12
                dots.append(d)
                targets.append([x + rng.uniform(-0.28, 0.28), ty, 0])
            self.play(
                heads_t.animate.set_value(h_now + k),
                total_t.animate.set_value(total_t.get_value() + per),
                *[d.animate.move_to(t) for d, t in zip(dots, targets)],
                run_time=0.55,
            )
            self.play(FadeOut(VGroup(*dots), run_time=0.22))

        dash = DashedLine(np.array([0.0, 0.12, 0]), np.array([0.0, -1.42, 0]),
                          color=GREEN, stroke_width=3)
        note = VGroup(
            self.zh("96 次投掷后，正面频率 ", font_size=32, color=INK),
            self.mt(r"\hat{p}_{96}", font_size=38, color=GREEN),
            self.zh(" 稳定在 ", font_size=32, color=INK),
            self.mt(r"0.5", font_size=38, color=GREEN),
            self.zh(" 附近", font_size=32, color=INK),
        ).arrange(RIGHT, buff=0.1).move_to([0.0, 0.45, 0])
        self.play(Create(dash), FadeIn(note, shift=UP * 0.2), run_time=0.9)
        self.wait(2.2)
        self.clear_scene()

    # ---------------- 一、核心概念 ----------------
    def concept_defs(self):
        bar = self.title_bar("一、核心概念：样本均值 vs 总体期望")
        self.play(Write(bar), run_time=0.8)

        l1 = VGroup(
            self.zh("独立同分布样本　", font_size=38, color=BLUE),
            self.mt(r"X_1,\ X_2,\ \cdots,\ X_n", font_size=48, color=INK),
        ).arrange(RIGHT, buff=0.12)
        l2 = VGroup(
            self.zh("总体期望", font_size=38, color=INK),
            self.mt(r"E[X]=\mu", font_size=48, color=YELLOW),
            self.zh("，", font_size=38, color=INK),
            self.zh("总体方差", font_size=38, color=INK),
            self.mt(r"\mathrm{Var}(X)=\sigma^2", font_size=48, color=YELLOW),
        ).arrange(RIGHT, buff=0.14)
        l3 = VGroup(
            self.zh("样本均值　", font_size=38, color=INK),
            self.mt(r"\displaystyle\bar{X}_n=\frac{1}{n}\sum_{i=1}^{n}X_i",
                    font_size=56, color=INK),
        ).arrange(RIGHT, buff=0.12)
        l4 = self.zh("物理含义：n 次重复测量取平均，抹平单次的随机波动",
                     font_size=32, color=MUTED)

        self.layout_below(bar, l1, l2, l3, l4)
        for line in (l1, l2, l3, l4):
            self.fade_line(line)
        self.wait(2.0)
        self.clear_scene()

    # ---------------- 二、定理陈述 ----------------
    def concept_theorem(self):
        bar = self.title_bar("二、弱大数定律：定理陈述")
        self.play(Write(bar), run_time=0.8)

        l1 = self.mt(
            r"\forall\,\varepsilon>0,\quad \lim_{n\to\infty}"
            r"P\left(\,\left|\bar{X}_n-\mu\right|\ \ge\ \varepsilon\,\right)=0",
            font_size=52, color=INK)
        l2 = VGroup(
            self.mt(r"\bar{X}_n", font_size=50, color=BLUE),
            self.mt(r"\ \xrightarrow{\ P\ }\ ", font_size=50, color=ORANGE),
            self.mt(r"\mu", font_size=50, color=GREEN),
            self.zh("　（依概率收敛）", font_size=34, color=MUTED),
        ).arrange(RIGHT, buff=0.1)
        l3 = self.zh("直观理解：n 足够大时，样本均值偏离 μ 超过 ε 的概率趋于 0",
                     font_size=34, color=INK)

        self.layout_below(bar, l1, l2, l3, centered=True)
        self.fade_line(l1)
        box = SurroundingRectangle(l1, color=YELLOW, buff=0.16, stroke_width=3)
        self.play(Create(box), run_time=0.7)
        self.fade_line(l2)
        self.fade_line(l3)
        self.wait(2.0)
        self.clear_scene()

    # ---------------- 三、物理含义：平均的力量 ----------------
    def meaning_scene(self):
        bar = self.title_bar("三、物理含义：平均的力量")
        self.play(Write(bar), run_time=0.8)

        rng = np.random.default_rng(42)
        K = 60
        obs = np.clip(rng.normal(0.0, 0.9, K), -2.6, 2.6)
        run = np.cumsum(obs) / np.arange(1, K + 1)

        ax2 = Axes(
            x_range=[0, K, 10], y_range=[-3, 3, 1],
            x_length=6.4, y_length=4.3,
            axis_config={"color": MUTED, "stroke_width": 2,
                         "include_ticks": False},
        ).move_to([-3.8, -0.2, 0])
        mu_lab = self.mt(r"\mu=0", font_size=30, color=YELLOW)
        mu_lab.next_to(ax2.c2p(K, 0), RIGHT, buff=0.15)

        path = VMobject(color=RED, stroke_width=2.5)
        path.set_points_as_corners([ax2.c2p(i, float(obs[i])) for i in range(K)])
        run_c = VMobject(color=GREEN, stroke_width=4.5)
        run_c.set_points_as_corners([ax2.c2p(i, float(run[i])) for i in range(K)])

        lab_p = VGroup(
            self.mt(r"X_k", font_size=30, color=RED),
            self.zh(" 单次观测", font_size=25, color=RED),
        ).arrange(RIGHT, buff=0.1)
        lab_r = VGroup(
            self.mt(r"\bar{X}_k", font_size=30, color=GREEN),
            self.zh(" 前 k 次平均", font_size=25, color=GREEN),
        ).arrange(RIGHT, buff=0.1)
        VGroup(lab_p, lab_r).arrange(RIGHT, buff=1.1).next_to(ax2, UP, buff=0.22)

        r1 = self.zh("单次观测：随机不定，无法预测", font_size=34, color=RED)
        r2 = self.zh("多次平均：正负波动相互抵消", font_size=34, color=BLUE)
        r3 = VGroup(
            self.zh("平均稳定于总体期望 ", font_size=34, color=INK),
            self.mt(r"\mu", font_size=46, color=GREEN),
            self.zh(" 附近", font_size=34, color=INK),
        ).arrange(RIGHT, buff=0.1)
        VGroup(r1, r2, r3).arrange(DOWN, buff=0.85, aligned_edge=LEFT
                                   ).move_to([4.1, 0.15, 0])

        self.play(FadeIn(ax2), FadeIn(mu_lab), run_time=0.9)
        self.play(FadeIn(lab_p), FadeIn(lab_r), run_time=0.5)
        self.play(Create(path), run_time=2.4, rate_func=linear)
        self.fade_line(r1, hold=False)
        self.play(Create(run_c), run_time=2.2, rate_func=linear)
        self.fade_line(r2, hold=False)
        self.fade_line(r3)
        self.wait(2.0)
        self.clear_scene()

    # ---------------- 四、证明准备：样本均值的期望与方差 ----------------
    def proof_prep(self):
        bar = self.title_bar("四、证明准备：样本均值的期望与方差")
        self.play(Write(bar), run_time=0.8)

        # 左侧：分布收窄示意图
        ax = Axes(
            x_range=[-3.2, 3.2, 1], y_range=[0, 1.3, 0.5],
            x_length=6.4, y_length=3.9,
            axis_config={"color": MUTED, "stroke_width": 2,
                         "include_ticks": False},
        ).move_to([-3.7, -0.35, 0])
        mu_dash = DashedLine(ax.c2p(0, 0), ax.c2p(0, 1.1),
                             color=YELLOW, stroke_width=3)
        mu_lab = self.mt(r"\mu", font_size=38, color=YELLOW)
        mu_lab.next_to(ax.c2p(0, 1.05), UL, buff=0.13)

        def bell(s):
            return lambda x: np.exp(-x * x / (2.0 * s * s))

        wide = ax.plot(bell(1.5), x_range=[-3.2, 3.2],
                       color=ORANGE, stroke_width=4)
        narrow = ax.plot(bell(0.55), x_range=[-3.2, 3.2],
                         color=GREEN, stroke_width=4)

        lab_w = VGroup(
            self.mt(r"X_i", font_size=30, color=ORANGE),
            self.zh(" 的分布", font_size=25, color=ORANGE),
        ).arrange(RIGHT, buff=0.08)
        lab_w.move_to(ax.c2p(-3.0, 0.22), aligned_edge=LEFT)
        lab_n = VGroup(
            self.mt(r"\bar{X}_n", font_size=30, color=GREEN),
            self.zh(" 的分布（n 大）", font_size=25, color=GREEN),
        ).arrange(RIGHT, buff=0.08)
        lab_n.move_to(ax.c2p(-3.0, 1.0), aligned_edge=LEFT)
        arr_w = Arrow(lab_w.get_right() + RIGHT * 0.05,
                      ax.c2p(-1.35, 0.72), stroke_width=3, color=ORANGE,
                      buff=0.08, max_tip_length_to_length_ratio=0.25)
        arr_n = Arrow(lab_n.get_right() + RIGHT * 0.05,
                      ax.c2p(-0.2, 0.95), stroke_width=3, color=GREEN,
                      buff=0.08, max_tip_length_to_length_ratio=0.25)
        note = self.zh("n 越大，样本均值的分布越向 μ 收窄",
                       font_size=27, color=MUTED).next_to(ax, DOWN, buff=0.25)

        # 右侧：两个关键矩
        p1 = self.mt(
            r"\displaystyle E[\bar{X}_n]=\frac{1}{n}\sum_{i=1}^{n}E[X_i]=\mu",
            font_size=44, color=INK)
        c1 = self.zh("期望的线性性 —— 期望不变", font_size=27, color=MUTED)
        p2 = self.mt(
            r"\displaystyle \mathrm{Var}(\bar{X}_n)=\frac{1}{n^{2}}"
            r"\sum_{i=1}^{n}\mathrm{Var}(X_i)=\frac{\sigma^{2}}{n}",
            font_size=44, color=INK)
        c2 = self.zh("独立性 —— 方差按 1/n 衰减", font_size=27, color=MUTED)
        p3 = VGroup(
            self.zh("期望 ", font_size=32, color=INK),
            self.mt(r"\mu", font_size=42, color=YELLOW),
            self.zh(" 不动，离散度 ", font_size=32, color=INK),
            self.mt(r"\sigma^2/n", font_size=42, color=YELLOW),
            self.zh(" 收缩", font_size=32, color=INK),
        ).arrange(RIGHT, buff=0.08)
        col = VGroup(
            VGroup(p1, c1).arrange(DOWN, buff=0.14),
            VGroup(p2, c2).arrange(DOWN, buff=0.14),
            p3,
        ).arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        self.fit(col, width=7.4)
        col.move_to([4.05, 0.0, 0])

        self.play(FadeIn(ax), Create(mu_dash), FadeIn(mu_lab), run_time=0.9)
        self.play(FadeIn(lab_w), GrowArrow(arr_w), Create(wide), run_time=1.2)
        self.play(FadeIn(lab_n), GrowArrow(arr_n), Create(narrow), run_time=1.2)
        self.play(FadeIn(note, shift=UP * 0.15), run_time=0.6)

        self.fade_line(VGroup(p1, c1))
        self.fade_line(VGroup(p2, c2))
        self.fade_line(p3)
        self.wait(2.0)
        self.clear_scene()

    # ---------------- 五、切比雪夫不等式：完成证明 ----------------
    def proof_chebyshev(self):
        bar = self.title_bar("五、切比雪夫不等式：完成证明")
        self.play(Write(bar), run_time=0.8)

        # 左侧：上界 1/n 衰减示意
        axb = Axes(
            x_range=[0, 50, 10], y_range=[0, 1.15, 0.5],
            x_length=6.4, y_length=3.7,
            axis_config={"color": MUTED, "stroke_width": 2,
                         "include_ticks": False},
        ).move_to([-3.7, -0.45, 0])
        bound = axb.plot(lambda x: 1.0 / x, x_range=[1, 50],
                         color=ORANGE, stroke_width=4)
        blab = self.mt(r"\frac{\sigma^{2}}{n\,\varepsilon^{2}}",
                       font_size=42, color=ORANGE)
        blab.move_to(axb.c2p(24, 0.5))
        barr = Arrow(blab.get_bottom() + DOWN * 0.05, axb.c2p(7, 0.20),
                     stroke_width=3, color=ORANGE, buff=0.08,
                     max_tip_length_to_length_ratio=0.25)
        note2 = self.zh("示意：σ²=1，ε=1 时上界 = 1/n → 0",
                        font_size=26, color=MUTED).next_to(axb, DOWN, buff=0.22)
        nlab = self.mt(r"n", font_size=30, color=MUTED)
        nlab.next_to(axb.c2p(50, 0), RIGHT, buff=0.15).shift(UP * 0.22)

        # 右侧：三步推导
        r1 = self.mt(
            r"\displaystyle P\left(\left|Y-\mathbb{E}[Y]\right|\ge\varepsilon"
            r"\right)\le\frac{\mathrm{Var}(Y)}{\varepsilon^{2}}",
            font_size=42, color=INK)
        c1 = VGroup(
            self.zh("切比雪夫不等式，取　", font_size=27, color=ORANGE),
            self.mt(r"Y=\bar{X}_n", font_size=32, color=ORANGE),
        ).arrange(RIGHT, buff=0.08)
        r2 = self.mt(
            r"\displaystyle P\left(\left|\bar{X}_n-\mu\right|\ge\varepsilon"
            r"\right)\le\frac{\sigma^{2}}{n\,\varepsilon^{2}}",
            font_size=46, color=YELLOW)
        r3 = self.mt(
            r"\displaystyle \lim_{n\to\infty}"
            r"P\left(\left|\bar{X}_n-\mu\right|\ge\varepsilon\right)=0",
            font_size=46, color=GREEN)
        c3 = VGroup(
            self.zh("对任意 ", font_size=28, color=GREEN),
            self.mt(r"\varepsilon>0", font_size=30, color=GREEN),
            self.zh(" 成立 —— 证毕　", font_size=28, color=GREEN),
            self.mt(r"\blacksquare", font_size=30, color=GREEN),
        ).arrange(RIGHT, buff=0.08)
        col = VGroup(
            VGroup(r1, c1).arrange(DOWN, buff=0.16),
            r2,
            VGroup(r3, c3).arrange(DOWN, buff=0.16),
        ).arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        self.fit(col, width=7.5)
        col.move_to([4.1, 0.0, 0])

        self.play(FadeIn(axb), FadeIn(note2), FadeIn(nlab), run_time=0.9)
        self.play(Create(bound), run_time=1.2)
        self.play(FadeIn(blab), GrowArrow(barr), run_time=0.8)

        self.fade_line(VGroup(r1, c1))
        self.fade_line(r2)
        self.fade_line(VGroup(r3, c3))
        box = SurroundingRectangle(r3, color=GREEN, buff=0.12, stroke_width=2.5)
        self.play(Create(box), run_time=0.7)
        self.wait(2.2)
        self.clear_scene()

    # ---------------- 六 / 七、数值仿真 ----------------
    def simulate(self, cfg):
        bar = self.title_bar(cfg["title"])
        tag = self.mt(cfg["tex"], font_size=34, color=ORANGE)
        tag.next_to(bar, RIGHT, buff=0.4)
        self.play(Write(bar), FadeIn(tag, shift=UP * 0.2), run_time=0.8)

        N = 600
        rng = np.random.default_rng(cfg["seed"])
        samples = cfg["sampler"](rng, N)
        means = np.cumsum(samples) / np.arange(1, N + 1)

        if cfg["y_fixed"]:
            y_range = list(cfg["y_range"])
        else:
            y_top = float(np.ceil(max(1.2, float(np.max(means))) * 2.0) / 2.0)
            step = 0.5 if y_top <= 2.5 else (1.0 if y_top <= 5.0 else 2.0)
            y_range = [0.0, y_top, step]

        axes = Axes(
            x_range=[0, N, 100], y_range=y_range,
            x_length=12.2, y_length=4.7,
            axis_config={"color": MUTED, "stroke_width": 2},
        ).to_edge(DOWN, buff=0.55)
        axes.add_coordinates(font_size=17)

        mu_line = DashedLine(axes.c2p(0, cfg["mu"]), axes.c2p(N, cfg["mu"]),
                             color=YELLOW, stroke_width=3.5)
        mu_tag = self.mt(cfg["mu_tex"], font_size=34, color=YELLOW)
        mu_tag.next_to(mu_line.get_end(), RIGHT, buff=0.16)

        trk = ValueTracker(0.0)

        def cur():
            return int(round(trk.get_value() * (N - 1)))

        n_num = DecimalNumber(1, num_decimal_places=0, font_size=32, color=INK)
        mean_num = DecimalNumber(float(means[0]), num_decimal_places=3,
                                 font_size=32, color=cfg["curve_color"])
        g1 = VGroup(self.zh("n =", font_size=30, color=MUTED),
                    n_num).arrange(RIGHT, buff=0.32)
        g2 = VGroup(self.zh("样本均值 =", font_size=30, color=MUTED),
                    mean_num).arrange(RIGHT, buff=0.18)
        top_y = axes.c2p(0, y_range[1])[1] + 0.62
        g1.move_to([axes.c2p(0, 0)[0], top_y, 0], aligned_edge=LEFT)
        g2.move_to([axes.c2p(N, 0)[0], top_y, 0], aligned_edge=RIGHT)

        self.play(FadeIn(axes), Create(mu_line), FadeIn(mu_tag), run_time=1.0)
        self.play(FadeIn(g1), FadeIn(g2), run_time=0.6)
        # 淡入完成后再挂实时更新器，避免动画插值期间位数变化导致报错
        n_num.add_updater(lambda m: m.set_value(cur() + 1))
        mean_num.add_updater(lambda m: m.set_value(float(means[cur()])))

        curve = VMobject(color=cfg["curve_color"], stroke_width=3.5)
        curve.set_points_as_corners(
            [axes.c2p(i, float(means[i])) for i in range(N)])
        tip = always_redraw(lambda: Dot(
            axes.c2p(cur(), float(means[cur()])),
            radius=0.075, stroke_width=0,
            fill_color=cfg["curve_color"], fill_opacity=1.0))
        self.add(tip)
        self.play(Create(curve), trk.animate.set_value(1.0),
                  run_time=9.0, rate_func=linear)

        fin = VGroup(
            self.mt(r"\bar{X}_n\ \longrightarrow\ \mu",
                    font_size=40, color=GREEN),
            self.zh("　波动衰减，贴近期望线", font_size=28, color=MUTED),
        ).arrange(RIGHT, buff=0.22)
        fin.move_to([0.0, top_y, 0])
        self.play(FadeIn(fin, shift=UP * 0.2), run_time=0.8)
        self.wait(2.0)
        self.clear_scene()

    # ---------------- 八、提醒：收敛 ≠ 单次准确 ----------------
    def caveat(self):
        bar = self.title_bar("八、提醒：收敛 ≠ 单次准确", color=ORANGE)
        self.play(Write(bar), run_time=0.8)

        l1 = VGroup(
            self.mt(r"n=10^{4}", font_size=46, color=INK),
            self.zh(" 次投硬币后，正面频率 ", font_size=34, color=INK),
            self.mt(r"\hat{p}=0.5003", font_size=46, color=GREEN),
            self.zh(" ，已非常接近 ", font_size=34, color=INK),
            self.mt(r"0.5", font_size=46, color=INK),
        ).arrange(RIGHT, buff=0.1)
        l2 = self.zh("但第 10001 次的结果：正面概率依然是 50%，依旧无法预测",
                     font_size=34, color=ORANGE)
        l3 = VGroup(
            self.zh("弱大数定律只保证　", font_size=34, color=INK),
            self.mt(r"P\left(\left|\bar{X}_n-\mu\right|<\varepsilon\right)"
                    r"\ \longrightarrow\ 1", font_size=44, color=YELLOW),
            self.zh("　（概率收敛）", font_size=30, color=MUTED),
        ).arrange(RIGHT, buff=0.1)
        l4 = self.zh("大样本 ≠ 每次都准：它只让“平均”越来越稳，不改变单次随机性",
                     font_size=30, color=MUTED)

        self.layout_below(bar, l1, l2, l3, l4)
        for line in (l1, l2, l3, l4):
            self.fade_line(line)
        self.wait(2.0)
        self.clear_scene()

    # ---------------- 九、总结卡片 ----------------
    def summary_card(self):
        card = RoundedRectangle(corner_radius=0.3, width=13.6, height=6.7,
                                stroke_color=BLUE, stroke_width=2.5,
                                fill_color=CARD_BG, fill_opacity=1.0)
        card.move_to([0, -0.1, 0])
        head = self.zh("弱大数定律 · 核心总结", font_size=46, weight=BOLD)
        head.set_color_by_gradient(BLUE, GREEN, YELLOW)
        head.move_to(card.get_top() + DOWN * 0.62)
        sep = Line(card.get_left() + RIGHT * 0.8,
                   card.get_right() + LEFT * 0.8).set_color(MUTED)
        sep.set_stroke(width=1.4)
        sep.set_opacity(0.55)
        sep.move_to([0, card.get_top()[1] - 1.12, 0])

        r1a = self.zh("定理内容", font_size=34, color=BLUE, weight=BOLD)
        r1b = VGroup(
            self.mt(r"\bar{X}_n\ \xrightarrow{\ P\ }\ \mu",
                    font_size=46, color=YELLOW),
            self.zh("　样本均值依概率收敛于总体期望", font_size=29, color=INK),
        ).arrange(RIGHT, buff=0.25)
        r2a = self.zh("证明关键", font_size=34, color=ORANGE, weight=BOLD)
        r2b = VGroup(
            self.zh("切比雪夫不等式 ＋ ", font_size=29, color=INK),
            self.mt(r"\mathrm{Var}(\bar{X}_n)=\dfrac{\sigma^{2}}{n}\to 0",
                    font_size=42, color=INK),
        ).arrange(RIGHT, buff=0.2)
        r3a = self.zh("仿真现象", font_size=34, color=GREEN, weight=BOLD)
        r3b = self.zh("n 增大：均值曲线波动衰减、贴近期望线，更换分布结论不变",
                      font_size=29, color=INK)

        def make_row(a, b, color):
            mark = Rectangle(width=0.09, height=0.62, stroke_width=0,
                             fill_color=color, fill_opacity=1.0)
            return VGroup(mark, a, b).arrange(RIGHT, buff=0.32, aligned_edge=UP)

        row1 = make_row(r1a, r1b, BLUE)
        row2 = make_row(r2a, r2b, ORANGE)
        row3 = make_row(r3a, r3b, GREEN)
        for row in (row1, row2, row3):
            self.fit(row, width=11.4)
        rows = VGroup(row1, row2, row3).arrange(DOWN, buff=0.55,
                                                aligned_edge=LEFT)
        rows.next_to(sep, DOWN, buff=0.5)
        rows.align_to(card, LEFT).shift(RIGHT * 1.05)

        closing = self.zh("—— 用平均，对抗随机 ——", font_size=28, color=MUTED)
        closing.move_to([0, card.get_bottom()[1] - 0.5, 0])

        self.play(FadeIn(card, scale=1.04), FadeIn(head), Create(sep),
                  run_time=1.0)
        for row in (row1, row2, row3):
            self.play(FadeIn(row, shift=UP * 0.25), run_time=0.7)
            self.wait(0.5)
        self.play(FadeIn(closing, shift=UP * 0.2), run_time=0.6)
        self.wait(2.6)
        self.clear_scene()
