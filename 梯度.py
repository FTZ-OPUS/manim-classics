from manim import *
from manim.utils import rate_functions
# ----------------------------------------------------
# 全局设置与排版常量
# ----------------------------------------------------
FONT_CN = "Hiragino Sans GB"
FONT_SIZE_TITLE = 30
FONT_SIZE_SUB = 22
FONT_SIZE_BODY = 20
FONT_SIZE_FORMULA = 24
class GradientBoundProofExtended(Scene):
    def construct(self):
        # ----------------------------------------------------
        # 场景 1: 引入问题与引理条件
        # ----------------------------------------------------
        # 顶部标题栏
        title_text = Text("多元函数偏导数估计与极值定位", font=FONT_CN, font_size=FONT_SIZE_TITLE, color=BLUE)
        title_text.to_edge(UP, buff=0.4)
        underline = Line(LEFT * 6.5, RIGHT * 6.5, color=BLUE_D, stroke_width=2).next_to(title_text, DOWN, buff=0.15)
        self.play(Write(title_text), Create(underline), run_time=1.2)
        # 题干条件卡片 (VGroup 拼接中文与公式)
        p1_t1 = Text("设函数", font=FONT_CN, font_size=FONT_SIZE_BODY)
        p1_m1 = MathTex(r"f(x, y)", font_size=FONT_SIZE_FORMULA, color=YELLOW)
        p1_t2 = Text("在闭单位圆盘", font=FONT_CN, font_size=FONT_SIZE_BODY)
        p1_m2 = MathTex(r"D = \{(x, y) \mid x^2 + y^2 \le 1\}", font_size=FONT_SIZE_FORMULA, color=BLUE_B)
        p1_t3 = Text("上具有连续偏导数", font=FONT_CN, font_size=FONT_SIZE_BODY)
        line1 = VGroup(p1_t1, p1_m1, p1_t2, p1_m2, p1_t3).arrange(RIGHT, buff=0.12)
        p2_t1 = Text("且满足有界性：对任意", font=FONT_CN, font_size=FONT_SIZE_BODY)
        p2_m1 = MathTex(r"(x, y) \in D", font_size=FONT_SIZE_FORMULA, color=BLUE_B)
        p2_t2 = Text("，均有", font=FONT_CN, font_size=FONT_SIZE_BODY)
        p2_m2 = MathTex(r"|f(x, y)| \le 1", font_size=FONT_SIZE_FORMULA, color=ORANGE)
        line2 = VGroup(p2_t1, p2_m1, p2_t2, p2_m2).arrange(RIGHT, buff=0.12)
        p3_t1 = Text("证明目标：存在开区域内部点", font=FONT_CN, font_size=FONT_SIZE_BODY, color=YELLOW)
        p3_m1 = MathTex(r"(x_0, y_0) \in D^\circ", font_size=FONT_SIZE_FORMULA, color=YELLOW)
        p3_t2 = Text("，使得", font=FONT_CN, font_size=FONT_SIZE_BODY, color=YELLOW)
        p3_m2 = MathTex(r"f_x^2(x_0, y_0) + f_y^2(x_0, y_0) < 16", font_size=FONT_SIZE_FORMULA, color=YELLOW)
        line3 = VGroup(p3_t1, p3_m1, p3_t2, p3_m2).arrange(RIGHT, buff=0.12)
        cond_box_content = VGroup(line1, line2, line3).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        cond_card = SurroundingRectangle(cond_box_content, color=GREY_B, buff=0.25, corner_radius=0.15)
        cond_group = VGroup(cond_card, cond_box_content).next_to(underline, DOWN, buff=0.3)
        self.play(Create(cond_card), run_time=0.8)
        self.play(FadeIn(line1, shift=UP * 0.1), run_time=0.7)
        self.play(FadeIn(line2, shift=UP * 0.1), run_time=0.7)
        self.play(FadeIn(line3, shift=UP * 0.1), run_time=0.9)
        self.wait(2)
        # ----------------------------------------------------
        # 场景 2: 核心构造与辅助函数引入
        # ----------------------------------------------------
        self.play(FadeOut(cond_group), run_time=0.8)
        # 对称性说明 (VGroup 拼接)
        sym_t1 = Text("不妨设", font=FONT_CN, font_size=FONT_SIZE_BODY, color=GREY_A)
        sym_m1 = MathTex(r"f(0, 0) \ge 0", font_size=FONT_SIZE_FORMULA, color=GREY_A)
        sym_t2 = Text("（若小于 0，则考虑", font=FONT_CN, font_size=FONT_SIZE_BODY, color=GREY_A)
        sym_m2 = MathTex(r"-f(x, y)", font_size=FONT_SIZE_FORMULA, color=GREY_A)
        sym_t3 = Text("，平方和保持一致）", font=FONT_CN, font_size=FONT_SIZE_BODY, color=GREY_A)
        sym_group = VGroup(sym_t1, sym_m1, sym_t2, sym_m2, sym_t3).arrange(RIGHT, buff=0.1)
        sym_group.next_to(underline, DOWN, buff=0.2)
        # 核心辅助函数
        aux_t1 = Text("构造神级辅助函数：", font=FONT_CN, font_size=FONT_SIZE_SUB, color=TEAL)
        aux_m1 = MathTex(r"g(x, y) = f(x, y) - 2(x^2 + y^2)", font_size=28, color=TEAL)
        aux_line = VGroup(aux_t1, aux_m1).arrange(RIGHT, buff=0.2).next_to(sym_group, DOWN, buff=0.25)
        self.play(FadeIn(sym_group))
        self.play(Write(aux_t1), Write(aux_m1), run_time=1.2)
        self.wait(1.5)
        # ----------------------------------------------------
        # 场景 3: 几何圆盘与数值边界压制动态演示 (双栏布局)
        # ----------------------------------------------------
        # 左侧坐标系与单位圆盘
        plane = Axes(
            x_range=[-1.4, 1.4, 1],
            y_range=[-1.4, 1.4, 1],
            x_length=4.4,
            y_length=4.4,
            axis_config={"color": GREY_C, "stroke_width": 2, "include_ticks": False}
        ).to_edge(LEFT, buff=0.8).shift(DOWN * 0.4)
        x_lbl = MathTex("x", font_size=18, color=GREY_C).next_to(plane.x_axis.get_end(), RIGHT, buff=0.1)
        y_lbl = MathTex("y", font_size=18, color=GREY_C).next_to(plane.y_axis.get_end(), UP, buff=0.1)
        # 区域填充与边界
        disk_fill = Circle(radius=1.55, color=BLUE_E, fill_opacity=0.35, stroke_opacity=0).move_to(plane.c2p(0, 0))
        boundary_circle = Circle(radius=1.55, color=RED, stroke_width=3.5).move_to(plane.c2p(0, 0))
        
        d_label = MathTex(r"D", font_size=24, color=BLUE_B).move_to(plane.c2p(-0.6, -0.6))
        partial_d_t = Text("边界", font=FONT_CN, font_size=18, color=RED)
        partial_d_m = MathTex(r"\partial D", font_size=20, color=RED)
        partial_d_group = VGroup(partial_d_t, partial_d_m).arrange(RIGHT, buff=0.08).next_to(boundary_circle, UP + RIGHT, buff=-0.2)
        center_dot = Dot(plane.c2p(0, 0), color=GREEN, radius=0.08)
        center_t = Text("原点", font=FONT_CN, font_size=18, color=GREEN)
        center_m = MathTex(r"(0, 0)", font_size=20, color=GREEN)
        center_label = VGroup(center_t, center_m).arrange(RIGHT, buff=0.08).next_to(center_dot, DOWN + LEFT, buff=0.08)
        self.play(Create(plane), Write(x_lbl), Write(y_lbl), run_time=1.0)
        self.play(FadeIn(disk_fill), Create(boundary_circle), Write(d_label), Write(partial_d_group))
        self.play(FadeIn(center_dot), Write(center_label))
        # 右侧：推导第一阶段（原点 vs 边界取值对比）
        # 1. 原点取值
        r1_t = Text("1. 中心原点处：", font=FONT_CN, font_size=FONT_SIZE_BODY, color=WHITE)
        r1_m = MathTex(r"g(0, 0) = f(0, 0) - 0 \ge 0", font_size=FONT_SIZE_FORMULA, color=GREEN)
        row1 = VGroup(r1_t, r1_m).arrange(RIGHT, buff=0.15)
        # 2. 边界取值
        r2_t = Text("2. 单位圆边界上：", font=FONT_CN, font_size=FONT_SIZE_BODY, color=WHITE)
        r2_m1 = MathTex(r"x^2 + y^2 = 1", font_size=FONT_SIZE_FORMULA, color=RED)
        row2_sub = VGroup(r2_t, r2_m1).arrange(RIGHT, buff=0.15)
        r2_m2 = MathTex(r"g|_{\partial D} = f(x, y) - 2(1) \le 1 - 2 = -1", font_size=FONT_SIZE_FORMULA, color=RED)
        # 3. 严格大小关系
        r3_m = MathTex(r"\max_{(x, y) \in D} g(x, y) \ge g(0, 0) \ge 0 > -1 \ge g|_{\partial D}", font_size=FONT_SIZE_FORMULA, color=YELLOW)
        # 4. 结论：最大值点在内部
        r4_t1 = Text("结论：最大值点", font=FONT_CN, font_size=FONT_SIZE_BODY, color=YELLOW)
        r4_m1 = MathTex(r"(x_0, y_0)", font_size=FONT_SIZE_FORMULA, color=YELLOW)
        r4_t2 = Text("必在内部", font=FONT_CN, font_size=FONT_SIZE_BODY, color=YELLOW)
        r4_m2 = MathTex(r"D^\circ", font_size=FONT_SIZE_FORMULA, color=YELLOW)
        r4_t3 = Text("取得！", font=FONT_CN, font_size=FONT_SIZE_BODY, color=YELLOW)
        row4 = VGroup(r4_t1, r4_m1, r4_t2, r4_m2, r4_t3).arrange(RIGHT, buff=0.08)
        right_col_1 = VGroup(row1, row2_sub, r2_m2, r3_m, row4).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        right_col_1.next_to(plane, RIGHT, buff=0.8).align_to(plane, UP)
        self.play(Write(row1), run_time=1.0)
        self.wait(0.8)
        self.play(Write(row2_sub), Write(r2_m2), run_time=1.2)
        self.wait(1)
        self.play(Write(r3_m), run_time=1.2)
        self.play(FadeIn(row4, shift=UP * 0.1), run_time=1.0)
        self.wait(1.5)
        # 几何区动态特效：高亮开区域内极值点
        ext_dot = Dot(plane.c2p(0.38, 0.42), color=YELLOW, radius=0.09)
        ext_t = Text("极值点", font=FONT_CN, font_size=18, color=YELLOW)
        ext_m = MathTex(r"(x_0, y_0)", font_size=20, color=YELLOW)
        ext_label = VGroup(ext_t, ext_m).arrange(RIGHT, buff=0.08).next_to(ext_dot, UR, buff=0.08)
        # 涟漪脉冲动效
        pulse_circle = Circle(radius=0.1, color=YELLOW, stroke_width=3).move_to(ext_dot.get_center())
        self.play(FadeIn(ext_dot), Write(ext_label))
        self.play(
            pulse_circle.animate.scale(3.5).set_opacity(0),
            run_time=1.3,
            rate_func=rate_functions.ease_out_sine
        )
        self.remove(pulse_circle)
        self.wait(1)
        # ----------------------------------------------------
        # 场景 4: 驻点一阶条件与不等式推导
        # ----------------------------------------------------
        # 移走第一阶段推导文本，展现偏导一阶条件
        self.play(FadeOut(right_col_1), run_time=0.8)
        # 费马引理叙述 (VGroup 拼接)
        fm_t1 = Text("由多元函数极值一阶条件（费马引理）：", font=FONT_CN, font_size=FONT_SIZE_BODY, color=WHITE)
        fm_eq = MathTex(
            r"\begin{cases} g_x(x_0, y_0) = f_x(x_0, y_0) - 4x_0 = 0 \\ g_y(x_0, y_0) = f_y(x_0, y_0) - 4y_0 = 0 \end{cases}",
            font_size=FONT_SIZE_FORMULA
        )
        fermat_group = VGroup(fm_t1, fm_eq).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        # 偏导解出
        trans_t = Text("移项整理即得偏导数表达式：", font=FONT_CN, font_size=FONT_SIZE_BODY, color=BLUE_B)
        trans_eq = MathTex(
            r"\begin{cases} f_x(x_0, y_0) = 4x_0 \\ f_y(x_0, y_0) = 4y_0 \end{cases}",
            font_size=FONT_SIZE_FORMULA,
            color=BLUE_B
        )
        trans_group = VGroup(trans_t, trans_eq).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        # 平方和计算
        sum_eq = MathTex(
            r"f_x^2(x_0, y_0) + f_y^2(x_0, y_0) = (4x_0)^2 + (4y_0)^2 = 16(x_0^2 + y_0^2)",
            font_size=FONT_SIZE_FORMULA
        )
        # 最终不等式收束
        fin_t1 = Text("因为点在开圆盘内部", font=FONT_CN, font_size=FONT_SIZE_BODY, color=GREEN)
        fin_m1 = MathTex(r"x_0^2 + y_0^2 < 1", font_size=FONT_SIZE_FORMULA, color=GREEN)
        fin_cond = VGroup(fin_t1, fin_m1).arrange(RIGHT, buff=0.1)
        final_ineq = MathTex(
            r"f_x^2(x_0, y_0) + f_y^2(x_0, y_0) = 16(x_0^2 + y_0^2) < 16 \times 1 = 16",
            font_size=26,
            color=YELLOW
        )
        right_col_2 = VGroup(fermat_group, trans_group, sum_eq, fin_cond, final_ineq).arrange(
            DOWN, aligned_edge=LEFT, buff=0.24
        )
        right_col_2.next_to(plane, RIGHT, buff=0.8).align_to(plane, UP)
        self.play(FadeIn(fm_t1), Write(fm_eq), run_time=1.3)
        self.wait(1.0)
        self.play(FadeIn(trans_t), Write(trans_eq), run_time=1.2)
        self.wait(1.0)
        self.play(Write(sum_eq), run_time=1.0)
        self.wait(0.8)
        self.play(FadeIn(fin_cond), run_time=0.8)
        self.play(Write(final_ineq), run_time=1.2)
        # 结论高亮方框与证毕标识
        qed_box = SurroundingRectangle(final_ineq, color=GREEN, buff=0.16, stroke_width=2.5)
        qed_t = Text("命题得证", font=FONT_CN, font_size=FONT_SIZE_SUB, color=GREEN)
        qed_m = MathTex(r"\text{Q.E.D.}", font_size=FONT_SIZE_FORMULA, color=GREEN)
        qed_badge = VGroup(qed_t, qed_m).arrange(RIGHT, buff=0.12).next_to(qed_box, DOWN, buff=0.15)
        self.play(Create(qed_box), Write(qed_badge), run_time=1.0)
        self.wait(3.5)
        # ----------------------------------------------------
        # 场景 5: 平滑淡出收尾
        # ----------------------------------------------------
        all_objects = [mob for mob in self.mobjects]
        self.play(*[FadeOut(mob) for mob in all_objects], run_time=1.2)
        self.wait(0.5)
