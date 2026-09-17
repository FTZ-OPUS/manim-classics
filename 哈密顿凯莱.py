# -*- coding: utf-8 -*-
"""
视频 1：哈密顿–凯莱定理的摄动法证明（数学科普，约 3.5 分钟）
排版严格遵循《横屏大·字公式manim.md》规范
"""
from common import *


class CHVideo(BaseScene):
    def construct(self):
        self.camera.background_color = BG
        self.opening()
        self.strategy()
        self.statement()
        self.prep1_matrix_function()
        self.demo_2x2()
        self.prep2_similarity()
        self.prep3_limit_lemma()
        self.case1_formulas()
        self.case1_visual()
        self.hard_case()
        self.perturb_numberline()
        self.bad_t()
        self.schur()
        self.finale()
        self.summary()
        self.outlook()
        self.ending()

    # ------------------------------------------------------------------ 开场
    def opening(self):
        ghost = self.mt(r"f(A)=O", font_size=230, color=MUTED).set_opacity(0.09)
        ghost.move_to(DOWN * 0.2)

        title = self.zh("哈密顿–凯莱定理", font_size=64, color=INK, weight=BOLD)
        title.to_edge(UP, buff=1.0)
        subtitle = self.zh("Cayley–Hamilton · 摄动法 · 矩阵函数 · 极限引理",
                           font_size=34, color=MUTED)
        subtitle.next_to(title, DOWN, buff=0.45)

        eq = self.mt(r"f(A)=O", font_size=100, color=YELLOW, stroke_width=1.5)
        eq.move_to(UP * 0.1)
        box = SurroundingRectangle(eq, color=YELLOW, corner_radius=0.18, buff=0.32)

        tail = self.zh("每个方阵，最终都满足自己的特征多项式", font_size=38, color=INK)
        tail.to_edge(DOWN, buff=0.9)

        self.play(FadeIn(ghost), run_time=0.6)
        self.play(Write(title), run_time=0.9)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=0.6)
        self.play(GrowFromCenter(box), FadeIn(eq, scale=1.25), run_time=0.9)
        self.wait(0.8)
        self.play(FadeIn(tail, shift=UP * 0.25), run_time=0.6)
        self.wait(1.6)
        self.clear_scene()

    # ------------------------------------------------------------------ 思路
    def strategy(self):
        bar = self.title_bar("证明思路 · 四步走")
        self.play(Write(bar), run_time=0.8)

        s1 = self.zh("一、预备工具：矩阵函数 · 相似不变性 · 极限引理",
                     font_size=38, color=BLUE)
        s2 = self.mixed(
            ("text", "二、简单情形：特征值互异 → 可对角化 → ", GREEN),
            ("math", r"f(A)=O", GREEN),
        )
        s3 = self.mixed(
            ("text", "三、摄动法：", ORANGE),
            ("math", r"T_t=T+tD", ORANGE),
            ("text", " 把重叠的特征值轻轻推开", ORANGE),
        )
        s4 = self.mixed(
            ("text", "四、收官：无穷多个好 ", VIOLET),
            ("math", r"t\to 0", VIOLET),
            ("text", " 取极限 ＋ 相似不变性 → 一切方阵 ", VIOLET),
            ("math", r"f(A)=O", VIOLET),
        )
        content = self.layout_below(bar, s1, s2, s3, s4)
        for line in [s1, s2, s3, s4]:
            self.play(Write(line), run_time=0.8)
        self.wait(1.8)
        self.clear_scene()

    # ------------------------------------------------------------------ 定理陈述
    def statement(self):
        bar = self.title_bar("第一步 · 定理在说什么")
        self.play(Write(bar), run_time=0.8)

        l1 = self.mixed(
            ("text", "设 ", INK), ("math", r"A", INK),
            ("text", " 是 ", INK), ("math", r"n", INK),
            ("text", " 阶方阵，它的特征多项式为", INK),
        )
        l2 = self.mt(r"f(\lambda)=\det(\lambda I_n-A)", font_size=60, color=INK)
        l3 = self.mixed(
            ("text", "把 ", INK), ("math", r"\lambda", YELLOW), ("text", " 换成 ", INK),
            ("math", r"A", YELLOW), ("text", "，常数 ", INK), ("math", r"c", INK),
            ("text", " 换成 ", INK), ("math", r"cI", INK), ("text", "：", INK),
        )
        eq = self.mt(r"f(A)=O", font_size=84, color=YELLOW, stroke_width=1.5)
        box = SurroundingRectangle(eq, color=YELLOW, corner_radius=0.16, buff=0.28)
        row4 = VGroup(eq, box)

        content = self.layout_below(bar, l1, l2, l3, row4, buff=0.72)
        self.write_formula(l1, 0.8)
        self.write_formula(l2, 0.9)
        self.write_formula(l3, 0.8)
        self.play(GrowFromCenter(box), FadeIn(eq, scale=1.2), run_time=0.8)
        self.wait(1.2)
        note = self.zh("定理中的 0 是零矩阵：数字世界的等式，变成了矩阵世界的等式",
                       font_size=33, color=MUTED)
        note.to_edge(DOWN, buff=0.55)
        self.play(FadeIn(note, shift=UP * 0.2), run_time=0.6)
        self.wait(1.6)
        self.clear_scene()

    # ------------------------------------------------------------------ 预备1 定义
    def prep1_matrix_function(self):
        bar = self.title_bar("预备 1 · 矩阵函数（矩阵多项式）")
        self.play(Write(bar), run_time=0.8)

        l1 = self.mixed(
            ("text", "给定普通多项式 ", INK),
            ("math", r"f(x)=a_0+a_1x+\cdots+a_mx^m", INK),
            ("text", "，定义", INK),
        )
        l2 = self.mt(r"f(A)=a_0I+a_1A+\cdots+a_mA^m", font_size=58, color=YELLOW)
        box2 = SurroundingRectangle(l2, color=YELLOW, corner_radius=0.14, buff=0.22)
        l3 = self.mixed(
            ("text", "代换规则：", INK), ("math", r"x\mapsto A", INK),
            ("text", "，", INK), ("math", r"c\mapsto cI", INK),
            ("text", "；其中 ", INK), ("math", r"I", INK), ("text", " 是单位阵，", INK),
            ("math", r"O", INK), ("text", " 是零矩阵", INK),
        )
        l4 = self.zh("它就是“把矩阵当自变量”的多项式 —— 加法、乘法、幂，全按矩阵规则进行",
                     font_size=33, color=MUTED)

        content = self.layout_below(bar, l1, VGroup(l2, box2), l3, l4, buff=0.78)
        self.write_formula(l1, 0.8)
        self.play(Write(l2), DrawBorderThenFill(box2), run_time=1.0)
        self.wait_formula()
        self.write_formula(l3, 0.8)
        self.write_text(l4, 0.7)
        self.wait(1.6)
        self.clear_scene()

    # ------------------------------------------------------------------ 预备1 数值实验
    def demo_2x2(self):
        bar = self.title_bar("预备 1 · 动手算一个（2 阶方阵）")
        self.play(Write(bar), run_time=0.8)

        l1 = self.mixed(
            ("math", r"A=\begin{pmatrix}1&2\\3&4\end{pmatrix}", INK),
            ("text", "，取 ", INK),
            ("math", r"f(\lambda)=\lambda^2-5\lambda-2", INK),
        )
        l2 = self.mixed(
            ("math", r"A^2=\begin{pmatrix}7&10\\15&22\end{pmatrix}", INK),
            ("text", "　（矩阵乘法，先算平方）", MUTED),
        )
        l3 = self.mt(
            r"A^2-5A-2I=\begin{pmatrix}0&0\\0&0\end{pmatrix}=O",
            font_size=54, color=GREEN,
        )
        content = self.layout_below(bar, l1, l2, l3, buff=0.95)
        box3 = SurroundingRectangle(l3, color=GREEN, corner_radius=0.14, buff=0.22)
        self.write_formula(l1, 0.9)
        self.write_formula(l2, 0.9)
        self.play(Write(l3), run_time=1.0)
        self.play(Create(box3), Flash(l3, color=GREEN, flash_radius=1.4), run_time=0.8)
        self.wait_formula()
        concl = self.zh("数值验证成功：这个 A 确实满足自己的特征多项式",
                        font_size=36, color=GREEN)
        concl.to_edge(DOWN, buff=0.55)
        self.play(FadeIn(concl, shift=UP * 0.2), run_time=0.6)
        self.wait(1.6)
        self.clear_scene()

    # ------------------------------------------------------------------ 预备2 相似不变性
    def prep2_similarity(self):
        bar = self.title_bar("预备 2 · 相似不变性（引理，当场证明）")
        self.play(Write(bar), run_time=0.8)

        l1 = self.mixed(
            ("text", "先看幂：", INK),
            ("math", r"(P^{-1}AP)^k=P^{-1}A^kP", INK),
            ("text", "　（中间的 ", INK), ("math", r"P^{-1}P=I", INK),
            ("text", " 成对抵消）", INK),
        )
        l2 = self.mt(r"\Longrightarrow\quad f(P^{-1}AP)=P^{-1}f(A)P",
                     font_size=54, color=YELLOW)
        box2 = SurroundingRectangle(l2, color=YELLOW, corner_radius=0.14, buff=0.24)
        l3 = self.mixed(
            ("text", "特别地，", INK), ("math", r"P^{-1}OP=O", INK),
            ("text", "：所以 ", INK), ("math", r"f(A)=O", INK),
            ("text", " 与 ", INK), ("math", r"f(P^{-1}AP)=O", INK),
            ("text", " 同真同假", INK),
        )
        l4 = self.zh("想证 f(A) = O，可以换成证它的任何相似矩阵 —— 这给了我们“搬家”的自由",
                     font_size=33, color=MUTED)

        content = self.layout_below(bar, l1, VGroup(l2, box2), l3, l4, buff=0.78)
        self.write_formula(l1, 0.9)
        self.play(Write(l2), run_time=0.9)
        self.play(Create(box2), run_time=0.5)
        self.wait_formula()
        self.write_formula(l3, 0.9)
        self.write_text(l4, 0.7)
        self.wait(1.6)
        self.clear_scene()

    # ------------------------------------------------------------------ 预备3 极限引理
    def prep3_limit_lemma(self):
        bar = self.title_bar("预备 3 · 极限引理（摄动法的发动机）")
        self.play(Write(bar), run_time=0.8)

        k1 = self.mixed(
            ("text", "设矩阵值函数 ", INK), ("math", r"M(t)", INK),
            ("text", " 的每个元素都是 ", INK), ("math", r"t", INK),
            ("text", " 的多项式", INK),
        )
        k2 = self.mixed(
            ("text", "若有无穷多个互不相同的 ", INK), ("math", r"t_k\to 0", INK),
            ("text", "，使得", INK),
        )
        k3 = self.mt(r"M(t_k)=O\qquad(k=1,2,\dots)", font_size=50, color=INK)
        k4 = self.mt(r"\Longrightarrow\quad M(0)=O", font_size=60, color=GREEN)
        box4 = SurroundingRectangle(k4, color=GREEN, corner_radius=0.16, buff=0.26)

        left = VGroup(k1, k2, k3, VGroup(k4, box4)).arrange(DOWN, buff=0.72)
        self.fit(left, width=8.6)
        left.move_to(LEFT * 3.0 + UP * 0.35)

        # 右侧小图：多项式曲线，零点无穷多 ⇒ 恒为零
        axes = Axes(
            x_range=[0, 1.3, 0.5], y_range=[-1.1, 1.3, 1.0],
            x_length=5.6, y_length=3.6,
            axis_config={"color": MUTED, "stroke_width": 2,
                         "include_ticks": False, "include_tip": True},
        ).move_to(RIGHT * 4.15 + UP * 0.6)
        curve = axes.plot(
            lambda t: 6.5 * (t - 0.25) * (t - 0.62) * (t - 1.05),
            x_range=[0.02, 1.26], color=BLUE, stroke_width=4,
        )
        zeros = VGroup(*[
            Dot(axes.c2p(x, 0), radius=0.09, color=RED) for x in (0.25, 0.62, 1.05)
        ])
        more = self.zh("…… 零点越聚越多", font_size=26, color=RED)
        more.next_to(zeros, DOWN, buff=0.35).align_to(axes, RIGHT)
        plabel = self.mt(r"p(t)", font_size=36, color=BLUE)
        plabel.next_to(curve.get_start(), UR, buff=0.15)

        reason = self.mixed(
            ("text", "原因：单变量多项式若有无穷多个零点，就只能恒为零 —— ", INK),
            ("math", r"M(0)", INK), ("text", " 的每个元素都是这样", INK),
            text_size=33, math_size=38,
        )
        self.fit(reason, width=config.frame_width - 1.2)
        reason.to_edge(DOWN, buff=0.55)

        self.play(Write(k1), run_time=0.8)
        self.play(Write(k2), run_time=0.8)
        self.write_formula(k3, 0.9)
        self.play(Write(k4), Create(box4), run_time=0.9)
        self.wait(0.6)
        self.play(Create(axes), Create(curve), run_time=1.0)
        self.play(FadeIn(zeros, lag_ratio=0.2), FadeIn(more), FadeIn(plabel), run_time=0.8)
        self.wait(0.8)
        self.play(FadeIn(reason, shift=UP * 0.2), run_time=0.6)
        self.wait(1.6)
        self.clear_scene()

    # ------------------------------------------------------------------ 简单情形（公式）
    def case1_formulas(self):
        bar = self.title_bar("第二关 · 简单情形：特征值互异")
        self.play(Write(bar), run_time=0.8)

        l1 = self.mixed(
            ("text", "若 ", INK), ("math", r"\lambda_1,\dots,\lambda_n", INK),
            ("text", " 互不相同，则 ", INK), ("math", r"A", INK),
            ("text", " 一定可对角化", INK),
        )
        l2 = self.mt(r"P^{-1}AP=\Lambda=\mathrm{diag}(\lambda_1,\dots,\lambda_n)",
                     font_size=54, color=INK)
        l3 = self.mixed(
            ("text", "由相似不变性：", INK),
            ("math", r"P^{-1}f(A)P=f(\Lambda)=\prod_{i=1}^{n}(\Lambda-\lambda_iI)",
             YELLOW),
            text_size=38, math_size=46,
        )
        l4 = self.zh("（互异特征值的特征向量线性无关，恰好拼成可逆矩阵 P —— 标准定理）",
                     font_size=32, color=MUTED)

        content = self.layout_below(bar, l1, l2, l3, l4, buff=0.82)
        self.write_formula(l1, 0.8)
        self.write_formula(l2, 0.9)
        self.write_formula(l3, 1.0)
        self.write_text(l4, 0.7)
        self.wait(1.8)
        self.clear_scene()

    # ------------------------------------------------------------------ 简单情形（逐格击破可视化）
    def case1_visual(self):
        bar = self.title_bar("为什么 f(Λ) = O ？逐格击破")
        self.play(Write(bar), run_time=0.8)

        # 对角格
        cells = VGroup()
        labels = VGroup()
        for i in range(3):
            cell = RoundedRectangle(corner_radius=0.12, width=1.05, height=1.05,
                                    stroke_color=BLUE, stroke_width=3,
                                    fill_color=BLUE, fill_opacity=0.10)
            cell.move_to(UP * 1.45 + RIGHT * (i - 1) * 1.45)
            lab = self.mt(r"\lambda_%d" % (i + 1), font_size=44, color=INK)
            lab.move_to(cell.get_center())
            cells.add(cell)
            labels.add(lab)
        obox = RoundedRectangle(corner_radius=0.12, width=1.05, height=1.05,
                                stroke_color=GREEN, stroke_width=3.5,
                                fill_color=GREEN, fill_opacity=0.15)
        obox.move_to(UP * 1.45 + RIGHT * 3.6)
        olabel = self.mt(r"O", font_size=52, color=GREEN)
        olabel.move_to(obox.get_center())
        arrow = Arrow(cells.get_right() + RIGHT * 0.12, obox.get_left() + LEFT * 0.12,
                      stroke_width=5, color=MUTED, buff=0.08)

        factor = self.mt(r"\times\ \left(\Lambda-\lambda_1I\right)",
                         font_size=48, color=ORANGE)
        factor.move_to(UP * 0.15)

        hint = self.zh("对角阵相乘 = 对角元分别相乘", font_size=34, color=MUTED)
        hint.move_to(DOWN * 0.85)

        self.play(FadeIn(cells, lag_ratio=0.15), FadeIn(labels, lag_ratio=0.15),
                  FadeIn(obox), FadeIn(olabel), run_time=0.8)
        self.play(GrowArrow(arrow), run_time=0.5)
        self.play(Write(factor), run_time=0.6)
        self.play(FadeIn(hint, shift=UP * 0.2), run_time=0.5)

        for i in range(3):
            new_factor = self.mt(r"\times\ \left(\Lambda-\lambda_%dI\right)" % (i + 1),
                                 font_size=48, color=ORANGE)
            new_factor.move_to(factor.get_center())
            step = self.mixed(
                ("text", "第 ", INK), ("math", r"%d" % (i + 1), INK),
                ("text", " 个对角元：", INK),
                ("math", r"\lambda_%d-\lambda_%d=0" % (i + 1, i + 1), RED),
                text_size=36, math_size=44,
            )
            step.move_to(DOWN * 2.0)
            self.play(ReplacementTransform(factor, new_factor), run_time=0.45)
            factor = new_factor
            zero = self.mt(r"0", font_size=48, color=RED)
            zero.move_to(labels[i].get_center())
            self.play(FadeIn(step, shift=UP * 0.15), run_time=0.4)
            self.play(ReplacementTransform(labels[i], zero),
                      Flash(zero, color=RED, flash_radius=0.7), run_time=0.55)
            labels[i] = zero
            self.play(FadeOut(step), run_time=0.3)

        concl = self.mixed(
            ("math", r"f(\Lambda)=O", GREEN),
            ("text", "　从而　", INK),
            ("math", r"f(A)=O", GREEN),
            text_size=38, math_size=52,
        )
        concl.move_to(DOWN * 3.0)
        boxc = SurroundingRectangle(concl, color=GREEN, corner_radius=0.14, buff=0.24)
        self.play(Write(concl), Create(boxc), run_time=0.9)
        self.wait(1.8)
        self.clear_scene()

    # ------------------------------------------------------------------ 困难：重根
    def hard_case(self):
        bar = self.title_bar("第三关 · 如果特征值重合了呢？")
        self.play(Write(bar), run_time=0.8)

        nl = NumberLine(x_range=[0, 4, 1], length=11.5, include_numbers=True,
                        font_size=28, stroke_width=2.5, include_tip=True,
                        tip_length=0.22).move_to(UP * 1.15)
        self.play(Create(nl), run_time=0.8)

        d1 = Dot(nl.number_to_point(1), radius=0.17, color=YELLOW)
        d1b = Dot(nl.number_to_point(1) + UR * 0.16, radius=0.10, color=YELLOW)
        badge = self.zh("×2", font_size=30, color=RED)
        badge.next_to(d1b, UP, buff=0.12)
        lab1 = self.zh("1（二重）", font_size=34, color=YELLOW)
        lab1.next_to(d1, DOWN, buff=0.5)
        d3 = Dot(nl.number_to_point(3), radius=0.17, color=GREEN)
        lab3 = self.zh("3", font_size=34, color=GREEN)
        lab3.next_to(d3, DOWN, buff=0.5)

        self.play(FadeIn(d1, scale=2), FadeIn(d1b, scale=2), FadeIn(badge),
                  FadeIn(lab1, shift=UP * 0.2), run_time=0.7)
        self.play(FadeIn(d3, scale=2), FadeIn(lab3, shift=UP * 0.2), run_time=0.5)

        l1 = self.mixed(
            ("text", "有重根时，", INK), ("math", r"A", INK),
            ("text", " 可能“亏损”而不可对角化 —— ", INK),
            ("math", r"P^{-1}AP=\Lambda", INK), ("text", " 未必存在", INK),
        )
        l1.move_to(DOWN * 1.15)
        l2 = self.zh("对角化这条路被堵死 → 换一件新武器：摄动法",
                     font_size=42, color=ORANGE, weight=BOLD)
        l2.move_to(DOWN * 2.55)

        self.write_formula(l1, 0.9)
        self.play(FadeIn(l2, shift=UP * 0.2), run_time=0.6)
        self.play(Circumscribe(l2, color=ORANGE, buff=0.18), run_time=0.9)
        self.wait(1.8)
        self.clear_scene()

    # ------------------------------------------------------------------ 摄动法数轴动画（核心）
    def perturb_numberline(self):
        bar = self.title_bar("摄动法 · 把重叠的特征值轻轻推开", color=ORANGE)
        self.play(Write(bar), run_time=0.8)

        l1 = self.mixed(
            ("math", r"T_t=T+tD,\qquad D=\mathrm{diag}(1,2,\dots,n)", INK),
            text_size=38, math_size=52,
        )
        l2 = self.mixed(
            ("text", "特征值随之变为 ", INK),
            ("math", r"\lambda_i(t)=\lambda_i+i\,t", YELLOW),
            ("text", "　（i 是座位号，各不相同）", MUTED),
            text_size=36, math_size=48,
        )
        top = VGroup(l1, l2).arrange(DOWN, buff=0.5)
        top.next_to(bar, DOWN, buff=0.5)
        self.play(Write(l1), run_time=0.9)
        self.wait(0.6)
        self.play(Write(l2), run_time=0.9)

        nl = NumberLine(x_range=[0, 5.2, 1], length=12.6, include_numbers=True,
                        font_size=26, stroke_width=2.5, include_tip=True,
                        tip_length=0.22)
        nl.to_edge(DOWN, buff=1.05)
        self.play(Create(nl), run_time=0.8)

        tracker = ValueTracker(0.0)
        lams = [1.0, 1.0, 3.0]
        seats = [1, 2, 3]
        cols = [BLUE, ORANGE, GREEN]
        dots = VGroup()
        labels = VGroup()
        for lam, seat, c in zip(lams, seats, cols):
            dot = Dot(radius=0.15, color=c)
            dot.move_to(nl.number_to_point(lam))
            lab = self.mt(r"\lambda_%d" % seat, font_size=40, color=c)
            lab.move_to(dot.get_center() + UP * 0.62 + RIGHT * (seat - 2) * 0.75)
            dot.add_updater(
                lambda d, lam=lam, seat=seat:
                d.move_to(nl.number_to_point(lam + seat * tracker.get_value()))
            )
            lab.add_updater(
                lambda l, lam=lam, seat=seat:
                l.move_to(nl.number_to_point(lam + seat * tracker.get_value())
                          + UP * 0.62 + RIGHT * (seat - 2) * 0.75)
            )
            dots.add(dot)
            labels.add(lab)
        self.play(FadeIn(dots, lag_ratio=0.15), FadeIn(labels, lag_ratio=0.15),
                  run_time=0.8)

        tnum = DecimalNumber(0.00, num_decimal_places=2, font_size=40, color=INK)
        tnum.add_updater(lambda m: m.set_value(tracker.get_value()))
        tlab = self.mt(r"t=", font_size=40, color=INK)
        tgrp = VGroup(tlab, tnum).arrange(RIGHT, buff=0.1).to_corner(UR, buff=0.7)
        tgrp.shift(DOWN * 1.1)
        self.play(FadeIn(tgrp), run_time=0.4)

        cap_pos = DOWN * 1.55
        cap1 = self.zh("t ＝ 0：三个特征值 1, 1, 3 —— 有一对重叠", font_size=36, color=INK)
        cap1.move_to(cap_pos)
        self.play(FadeIn(cap1, shift=UP * 0.2), run_time=0.5)
        self.wait(1.1)

        cap2 = self.zh("t ＝ 0.35：被推到 1.35, 1.70, 4.05 —— 全部分开",
                       font_size=36, color=GREEN)
        cap2.move_to(cap_pos)
        self.play(tracker.animate.set_value(0.35), run_time=2.6,
                  rate_func=rate_functions.ease_in_out_sine)
        self.play(FadeOut(cap1, shift=UP * 0.2), FadeIn(cap2, shift=UP * 0.2),
                  run_time=0.5)
        self.wait(1.2)

        cap3 = self.zh("t → 0：又无痕地回到原来的 T —— 极限的舞台已搭好",
                       font_size=36, color=ORANGE)
        cap3.move_to(cap_pos)
        self.play(tracker.animate.set_value(0.0), run_time=2.2,
                  rate_func=rate_functions.ease_in_out_sine)
        self.play(FadeOut(cap2, shift=UP * 0.2), FadeIn(cap3, shift=UP * 0.2),
                  run_time=0.5)
        self.wait(1.3)

        dots.clear_updaters()
        labels.clear_updaters()
        tnum.clear_updaters()
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------ 坏 t 有限
    def bad_t(self):
        bar = self.title_bar("摄动为什么总有效 · 坏的 t 只有有限个")
        self.play(Write(bar), run_time=0.8)

        l1 = self.mt(
            r"\lambda_i+i\,t=\lambda_j+j\,t\ \ (i\ne j)"
            r"\ \Longrightarrow\ t=\frac{\lambda_i-\lambda_j}{\,j-i\,}",
            font_size=50, color=INK,
        )
        l2 = self.mixed(
            ("text", "每一对 ", INK), ("math", r"(i,j)", INK),
            ("text", " 至多贡献一个坏 ", INK), ("math", r"t", INK),
            ("text", "，坏 ", INK), ("math", r"t", INK), ("text", " 至多 ", INK),
            ("math", r"\tbinom{n}{2}", YELLOW), ("text", " 个", INK),
        )
        l3 = self.mixed(
            ("text", "于是好 ", INK), ("math", r"t", INK),
            ("text", " 有无穷多个，且聚集在 ", INK), ("math", r"t=0", GREEN),
            ("text", " 附近 —— 极限引理的完美舞台", INK),
        )
        l4 = self.zh("例：λ = (1, 1, 3) 时，坏 t 只有 t = 0, -1, -2，其余全是好 t",
                     font_size=32, color=MUTED)

        content = self.layout_below(bar, l1, l2, l3, l4, buff=0.82)
        self.write_formula(l1, 1.0)
        self.write_formula(l2, 0.9)
        self.play(Write(l3), run_time=0.9)
        self.play(Circumscribe(l3, color=GREEN, buff=0.12), run_time=0.8)
        self.wait_formula()
        self.write_text(l4, 0.7)
        self.wait(1.6)
        self.clear_scene()

    # ------------------------------------------------------------------ Schur 上三角化
    def schur(self):
        bar = self.title_bar("引理 · 复方阵必可上三角化（Schur）")
        self.play(Write(bar), run_time=0.8)

        l1 = self.mixed(
            ("text", "存在可逆 ", INK), ("math", r"P", INK), ("text", "，使 ", INK),
            ("math", r"A=P\,T\,P^{-1}", INK),
        )
        tri = MathTex(
            r"\begin{pmatrix}"
            r"\lambda_1 & \ast & \ast & \cdots \\"
            r"0 & \lambda_2 & \ast & \cdots \\"
            r"\vdots & & \ddots & \\"
            r"0 & 0 & \cdots & \lambda_n"
            r"\end{pmatrix}",
            font_size=50, stroke_width=1,
            tex_to_color_map={
                r"\lambda_1": YELLOW, r"\lambda_2": YELLOW, r"\lambda_n": YELLOW,
                r"\ast": MUTED,
            },
        )
        self.fit(tri, height=2.9)
        l2 = self.mixed(
            ("text", "对角元恰为全部特征值（可以重复）。由预备 2，只需对 ", INK),
            ("math", r"T", INK), ("text", " 证明", INK),
        )
        l3 = self.zh("直观：取一个特征向量张成第一层，再在补空间里逐层归纳",
                     font_size=32, color=MUTED)

        content = self.layout_below(bar, l1, tri, l2, l3, buff=0.6)
        self.write_formula(l1, 0.8)
        self.play(FadeIn(tri, scale=0.9), run_time=0.8)
        yellows = [g for g in tri[0]
                   if g.get_fill_color().to_hex() == YELLOW
                   or g.get_stroke_color().to_hex() == YELLOW]
        yellows.sort(key=lambda g: -g.get_center()[1])
        clusters = []
        for g in yellows:
            for cl in clusters:
                if np.linalg.norm(cl[0].get_center() - g.get_center()) < 0.6:
                    cl.append(g)
                    break
            else:
                clusters.append([g])
        diag_boxes = VGroup(*[
            SurroundingRectangle(VGroup(*cl), color=YELLOW, buff=0.07,
                                 corner_radius=0.05)
            for cl in clusters
        ])
        self.play(Create(diag_boxes), run_time=0.7)
        self.wait(0.5)
        self.write_formula(l2, 0.9)
        self.write_text(l3, 0.7)
        self.wait(1.6)
        self.clear_scene()

    # ------------------------------------------------------------------ 终局
    def finale(self):
        bar = self.title_bar("终局 · 取极限，大功告成", color=GREEN)
        self.play(Write(bar), run_time=0.8)

        l1 = self.mixed(
            ("text", "对每个好 ", INK), ("math", r"t", INK),
            ("text", "：", INK), ("math", r"T_t", INK), ("text", " 的特征值 ", INK),
            ("math", r"\lambda_i+it", INK), ("text", " 互异，所以 ", INK),
            ("math", r"f_t(T_t)=O", YELLOW),
        )
        l2 = self.mt(r"f_t(\lambda)=\prod_{i=1}^{n}\left(\lambda-\lambda_i-it\right)",
                     font_size=48, color=INK)
        l3 = self.mixed(
            ("math", r"f_t", INK), ("text", " 的系数、", INK),
            ("math", r"f_t(T_t)", INK), ("text", " 的元素都是 ", INK),
            ("math", r"t", INK), ("text", " 的多项式；令好 ", INK),
            ("math", r"t\to 0", INK), ("text", "，由极限引理：", INK),
        )
        l4 = self.mt(r"f(T)=O\ \Longrightarrow\ f(A)=P\,f(T)\,P^{-1}=O",
                     font_size=54, color=GREEN)
        box4 = SurroundingRectangle(l4, color=GREEN, corner_radius=0.16, buff=0.26)
        done = self.zh("证毕", font_size=40, color=ORANGE, weight=BOLD)
        done.next_to(box4, RIGHT, buff=0.4)

        content = self.layout_below(bar, l1, l2, l3, VGroup(l4, box4, done), buff=0.72)
        self.write_formula(l1, 0.9)
        self.write_formula(l2, 0.9)
        self.write_formula(l3, 0.9)
        self.play(Write(l4), Create(box4), run_time=1.0)
        self.play(FadeIn(done, scale=1.4), Flash(done, color=ORANGE, flash_radius=0.8),
                  run_time=0.6)
        self.wait(2.0)
        self.clear_scene()

    # ------------------------------------------------------------------ 总结
    def summary(self):
        bar = self.title_bar("总结 · 摄动法三步舞", color=GREEN)
        self.play(Write(bar), run_time=0.8)

        def node(title_txt, sub_items, color, pos):
            box = RoundedRectangle(corner_radius=0.2, width=7.0, height=1.5,
                                   stroke_color=color, stroke_width=3,
                                   fill_color=color, fill_opacity=0.10)
            box.move_to(pos)
            head = self.zh(title_txt, font_size=33, color=color, weight=BOLD)
            head.move_to(box.get_center() + UP * 0.38)
            sub = self.mixed(*sub_items, text_size=27, math_size=31)
            self.fit(sub, width=6.5)
            sub.move_to(box.get_center() + DOWN * 0.28)
            return VGroup(box, head, sub)

        b1 = node("① 简单情形",
                  (("text", "特征值互异 → 可对角化 → ", INK), ("math", r"f(A)=O", INK)),
                  BLUE, UP * 1.5 + LEFT * 3.75)
        b2 = node("② 摄动推开重根",
                  (("math", r"T_t=T+tD", INK), ("text", "，好 ", INK),
                   ("math", r"t", INK), ("text", " 上特征值互异", INK)),
                  ORANGE, UP * 1.5 + RIGHT * 3.75)
        b3 = node("③ 极限引理",
                  (("text", "多项式在无穷多个 ", INK), ("math", r"t_k\to0", INK),
                   ("text", " 处为零 → 恒为零", INK)),
                  VIOLET, DOWN * 0.95 + RIGHT * 3.75)
        b4 = node("④ 相似不变性",
                  (("math", r"f(T)=O\Rightarrow f(A)=O", INK),),
                  GREEN, DOWN * 0.95 + LEFT * 3.75)

        a12 = Arrow(b1.get_right(), b2.get_left(), stroke_width=5, color=MUTED, buff=0.1)
        a23 = Arrow(b2.get_bottom(), b3.get_top(), stroke_width=5, color=MUTED, buff=0.1)
        a34 = Arrow(b3.get_left(), b4.get_right(), stroke_width=5, color=MUTED, buff=0.1)

        self.play(FadeIn(b1, shift=RIGHT * 0.3), run_time=0.5)
        self.play(GrowArrow(a12), FadeIn(b2, shift=RIGHT * 0.3), run_time=0.6)
        self.play(GrowArrow(a23), FadeIn(b3, shift=DOWN * 0.3), run_time=0.6)
        self.play(GrowArrow(a34), FadeIn(b4, shift=LEFT * 0.3), run_time=0.6)

        tail = self.zh("四步连环：任何方阵都逃不出自己的特征多项式",
                       font_size=38, color=GREEN, weight=BOLD)
        tail.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(tail, shift=UP * 0.2), run_time=0.6)
        self.wait(2.0)
        self.clear_scene()

    # ------------------------------------------------------------------ 展望
    def outlook(self):
        bar = self.title_bar("延伸与展望", color=VIOLET)
        self.play(Write(bar), run_time=0.8)

        o1 = self.bullet_line(BLUE,
            ("text", "求幂提速：", INK), ("math", r"A^{100}", INK),
            ("text", " 可化为低次多项式 —— 斐波那契矩阵 ", INK),
            ("math", r"\begin{pmatrix}1&1\\1&0\end{pmatrix}", INK),
            ("text", " 就满足 ", INK), ("math", r"x^2-x-1", INK),
            text_size=34, math_size=42,
        )
        o2 = self.bullet_line(GREEN,
            ("text", "求逆公式：", INK), ("math", r"f(0)=\det A\ne 0", INK),
            ("text", " 时，可从 ", INK), ("math", r"f(A)=O", INK),
            ("text", " 解出 ", INK), ("math", r"A^{-1}", INK),
            ("text", " 是 ", INK), ("math", r"A", INK), ("text", " 的多项式", INK),
            text_size=34, math_size=42,
        )
        o3 = self.bullet_line(ORANGE,
            ("text", "最小多项式：", INK), ("math", r"f", INK),
            ("text", " 的“最简满足版”，次数与若尔当块结构互相决定", INK),
            text_size=34, math_size=42,
        )
        o4 = self.bullet_line(VIOLET,
            ("text", "一般数域上没有极限怎么办？", INK),
            ("text", "改用“多项式恒等”技巧：先证含 ", INK), ("math", r"t", INK),
            ("text", " 的恒等式，再代 ", INK), ("math", r"t=0", INK),
            text_size=34, math_size=42,
        )
        content = self.layout_below(bar, o1, o2, o3, o4, buff=0.78)
        for line in [o1, o2, o3, o4]:
            self.play(Write(line), run_time=0.8)
            self.wait(0.35)
        self.wait(1.8)
        self.clear_scene()

    # ------------------------------------------------------------------ 结尾
    def ending(self):
        ghost = self.mt(r"f(A)=O", font_size=200, color=MUTED).set_opacity(0.08)
        ghost.move_to(UP * 0.3)
        big = self.zh("谢谢观看", font_size=64, color=INK, weight=BOLD)
        big.move_to(UP * 0.9)
        eq = self.mt(r"f(A)=O", font_size=84, color=YELLOW, stroke_width=1.5)
        eq.move_to(DOWN * 0.7)
        box = SurroundingRectangle(eq, color=YELLOW, corner_radius=0.16, buff=0.28)
        teaser = self.zh("下期预告：删掉分母带 9 的调和级数，竟然收敛？",
                         font_size=34, color=MUTED)
        teaser.to_edge(DOWN, buff=0.7)

        self.play(FadeIn(ghost), Write(big), run_time=0.9)
        self.play(GrowFromCenter(box), FadeIn(eq, scale=1.2), run_time=0.8)
        self.play(FadeIn(teaser, shift=UP * 0.2), run_time=0.6)
        self.wait(1.8)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.7)
        self.wait(0.3)
