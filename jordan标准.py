# -*- coding: utf-8 -*-
"""
《若尔当标准型》复刻版 —— 逐帧逆向还原
原片：130.8s，米白网格底 + 宋体标题 + 彩色格子矩阵 + 白场转场
结构：0-97.5s 数学讲解（20 个场景段）+ 97.5-130.8s 情感段（原片为 3D/IP 素材，
      此处用 Manim 风格化近似：透视网格简笔狼 / 粒子心形 / 撕纸拼贴 / 指纹 / 球体矩阵）
"""
from manim import *
import numpy as np

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16.0
config.frame_height = 9.0
config.background_color = "#FBF6EF"

# ---------------- 调色板（抽帧取色） ----------------
RED = "#E8535A"
BLUE = "#4A9DE8"
GREEN = "#2BB89A"
PURPLE = "#8B7BE8"
GOLD = "#E8A84B"
CYAN2 = "#35B8B0"
INK = "#3A3A3C"
GRIDC = "#E8E0D6"
# 矩阵格
CB = "#4A9DE8"   # 蓝格边/字
CFB = "#EAF3FC"  # 蓝格底
CR = "#E8535A"
CFR = "#FBE9E9"
CG = "#2BB89A"
CFG = "#E9F7F1"
CGR = "#B8AFA5"  # 灰格
CFGR = "#F6F1EA"
CELL = 0.92      # 格子边长

SONG = "Songti SC"     # 宋体标题
HEI = "PingFang SC"    # 黑体字幕


# ---------------- 通用组件 ----------------
def cell(sym, edge, fill, sym_color=None, font_size=38):
    """单个矩阵格子：圆角方块 + 衬线字符"""
    sq = RoundedRectangle(corner_radius=0.14, width=CELL, height=CELL)
    sq.set_stroke(edge, 2.6).set_fill(fill, 1)
    t = MathTex(sym, font_size=font_size, color=sym_color or edge)
    t.move_to(sq.get_center())
    return VGroup(sq, t)


def bracket(h, color=BLUE, sw=3.5, w=0.0):
    """矩阵括号 [ ]：w 为矩阵宽度，左右括号分别放在两侧"""
    half = h / 2
    arm = 0.22
    ww = w if w > 0 else h * 0.42
    L = VGroup(
        Line([0, -half, 0], [0, half, 0]).set_stroke(color, sw),
        Line([0, half, 0], [arm, half, 0]).set_stroke(color, sw),
        Line([0, -half, 0], [arm, -half, 0]).set_stroke(color, sw),
    )
    L.move_to([-ww / 2, 0, 0])
    R = VGroup(
        Line([0, -half, 0], [0, half, 0]).set_stroke(color, sw),
        Line([0, half, 0], [-arm, half, 0]).set_stroke(color, sw),
        Line([0, -half, 0], [-arm, -half, 0]).set_stroke(color, sw),
    )
    R.move_to([ww / 2, 0, 0])
    return VGroup(L, R)


def grid_matrix(entries, size=3, cell_w=CELL, gap=0.06):
    """entries: n×n 的 (sym, edge, fill) 列表的列表；返回 (格子组, 括号组) 整体"""
    n = len(entries)
    cells = VGroup()
    for i in range(n):
        for j in range(n):
            sym, edge, fill = entries[i][j]
            c = cell(sym, edge, fill, font_size=int(38 * cell_w / CELL))
            c.move_to(np.array([(j - (n - 1) / 2) * (cell_w + gap),
                                ((n - 1) / 2 - i) * (cell_w + gap), 0]))
            cells.add(c)
    side = n * cell_w + (n - 1) * gap
    br = bracket(side + 0.18, w=side + 0.12)
    return VGroup(cells, br)


def sec_title(text, color, font_size=44, y=3.35):
    return Text(text, font=SONG, weight="BOLD", font_size=font_size,
                color=color).move_to([0, y, 0])


def subtitle(text, y=-3.62, size=27):
    """底部硬字幕：白字黑边"""
    return Text(text, font=HEI, weight="BOLD", font_size=size,
                color=WHITE).set_stroke(BLACK, 5, background=True).move_to([0, y, 0])


def rand_card(rng, n=2, color=None, scale=1.0):
    """随机数字小矩阵卡片"""
    colors = [BLUE, GREEN, RED, PURPLE, GOLD, CYAN2]
    col = color or colors[rng.integers(0, len(colors))]
    cells = VGroup()
    for i in range(n):
        for j in range(n):
            c = cell(str(rng.integers(0, 10)), col, WHITE,
                     font_size=int(30 * scale * cell_w() if False else 30 * scale))
            c.scale(scale * 0.62)
            c.move_to(np.array([(j - (n - 1) / 2) * 0.62 * scale,
                                ((n - 1) / 2 - i) * 0.62 * scale, 0]))
            cells.add(c)
    return cells


def cell_w():
    return CELL


def heart_points(n=260, seed=3):
    """心形曲线上的粒子点"""
    rng = np.random.default_rng(seed)
    dots = VGroup()
    cols = ["#F08A9B", "#E8535A", "#FBD3DC", "#F8B8C8", "#FFF0F0", "#E8A0B8"]
    for _ in range(n):
        t = rng.uniform(0, 2 * np.pi)
        # 心形参数方程
        x = 16 * np.sin(t) ** 3 / 16
        y = (13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t)
             - np.cos(4 * t)) / 16
        r = rng.uniform(0.88, 1.12)
        d = Dot([x * 2.6 * r, y * 2.6 * r + 0.25, 0],
                radius=rng.uniform(0.03, 0.075),
                color=cols[rng.integers(0, len(cols))])
        d.set_opacity(rng.uniform(0.5, 1.0))
        dots.add(d)
    return dots


def fingerprint(scale=1.0, color=GOLD, arcs_per=3):
    """指纹：多层带缺口的同心弧"""
    layers = VGroup()
    for i in range(6):
        r = 0.32 + i * 0.24
        k = 0
        while k < arcs_per:
            start = np.random.default_rng(i * 10 + k).uniform(0, TAU)
            span = 1.2 + np.random.default_rng(i * 7 + k * 3).uniform(0.5, 1.8)
            a = Arc(radius=r, start_angle=start, angle=min(span, TAU - 0.2),
                    stroke_width=3.2, color=color)
            layers.add(a)
            k += 1
    layers.scale(scale)
    glow = layers.copy().set_stroke(width=9, opacity=0.25)
    return VGroup(glow, layers)


def simple_wolf(scale=1.0, body="#8A8A92", cap=True):
    """简笔灰狼（正面坐姿剪影）"""
    g = VGroup()
    body_e = Ellipse(width=1.55 * scale, height=1.35 * scale)
    body_e.set_fill(body, 1).set_stroke(width=0)
    belly = Ellipse(width=0.95 * scale, height=0.85 * scale)
    belly.set_fill("#C8C4BE", 1).set_stroke(width=0).shift(UP * 0.12 * scale)
    head = Circle(radius=0.62 * scale).set_fill(body, 1).set_stroke(width=0)
    head.shift(UP * 1.15 * scale)
    e1 = Polygon(ORIGIN, UP * 0.42 * scale, RIGHT * 0.34 * scale,
                 ).set_fill(body, 1).set_stroke(width=0)
    e1.shift(UP * 1.55 * scale + LEFT * 0.38 * scale).rotate(-0.25)
    e2 = e1.copy().rotate(PI).shift(RIGHT * 0.76 * scale)
    eye1 = Arc(radius=0.10 * scale, start_angle=-PI, angle=PI,
               stroke_width=4, color="#2A2A2E").move_to(head.get_center() + LEFT * 0.22 * scale + UP * 0.08 * scale)
    eye2 = eye1.copy().shift(RIGHT * 0.44 * scale)
    nose = Dot(head.get_center() + DOWN * 0.12 * scale, radius=0.07 * scale,
               color="#2A2A2E")
    mouth = Arc(radius=0.22 * scale, start_angle=-PI * 0.85, angle=PI * 0.7,
                stroke_width=4, color="#2A2A2E").move_to(head.get_center() + DOWN * 0.28 * scale)
    g.add(body_e, belly, e1, e2, head, eye1, eye2, nose, mouth)
    if cap:
        cap_e = Ellipse(width=0.85 * scale, height=0.3 * scale)
        cap_e.set_fill("#7FC4E8", 1).set_stroke(width=0)
        cap_e.shift(UP * 1.72 * scale)
        brim = Ellipse(width=1.0 * scale, height=0.14 * scale)
        brim.set_fill("#5AA8D8", 1).set_stroke(width=0)
        brim.shift(UP * 1.6 * scale)
        g.add(cap_e, brim)
    return g


def glow_line(p1, p2, color=CYAN2, w=3):
    return VGroup(
        Line(p1, p2).set_stroke(color, w + 6, opacity=0.25),
        Line(p1, p2).set_stroke(color, w, opacity=0.95),
    )


# ---------------- 主场景 ----------------
class JordanRemix(Scene):
    def construct(self):
        rng = np.random.default_rng(42)
        self.rng = rng
        self.sub_mob = None
        self.make_bg()
        self.cur = []
        self.s0_open()          # 0-1.3
        self.s1_question()      # 1.3-4.9
        self.s2_algebra()       # 4.9-9.6
        self.s3_title()         # 9.6-14.6
        self.s4_condition()     # 14.6-28.6
        self.s5_diagonal()      # 28.6-34.6
        self.s6_fail()          # 34.6-40.6
        self.s7_entrance()      # 40.6-51.6
        self.s8_block()         # 51.6-57.6
        self.s9_classic()       # 57.6-64.6
        self.s10_eigen()        # 64.6-71.6
        self.s11_born()         # 71.6-76.6
        self.s12_theorem()      # 76.6-85.6
        self.s13_unique()       # 85.6-89.6
        self.s14_fingerprint()  # 89.6-97.6
        self.s15_grid_wolf()    # 97.6-105
        self.s16_heart()        # 105-109.5
        self.s17_photos()       # 109.5-117.5
        self.s18_wall()         # 117.5-125.5
        self.s19_spheres()      # 125.5-130.8

    # ---------- 基础设施 ----------
    def make_bg(self):
        """米白背景 + 浅网格（永驻）"""
        grid = VGroup()
        for x in np.arange(-8, 8.01, 0.8):
            grid.add(Line([x, -4.6, 0], [x, 4.6, 0]).set_stroke(GRIDC, 1.2, 0.8))
        for y in np.arange(-4.4, 4.61, 0.8):
            grid.add(Line([-8, y, 0], [8, y, 0]).set_stroke(GRIDC, 1.2, 0.8))
        self.add(grid)

    def reg(self, *mobs):
        self.cur.extend([m for m in mobs if m is not None])

    def wipe(self, t_out=0.28, t_in=0.0, keep=()):
        """白场过渡：清空当前场景元素"""
        if self.cur:
            self.play(*[FadeOut(m) for m in self.cur], run_time=t_out)
        self.cur = [m for m in self.cur if m in keep]
        if t_in:
            self.wait(t_in)

    def sub_in(self, text, run_time=0.3):
        if getattr(self, "sub_mob", None) is not None:
            self.play(FadeOut(self.sub_mob), run_time=0.18)
            if self.sub_mob in self.cur:
                self.cur.remove(self.sub_mob)
        s = subtitle(text)
        self.play(FadeIn(s), run_time=run_time)
        self.reg(s)
        self.sub_mob = s
        return s

    # ---------- S0 开场 0-1.3 ----------
    def s0_open(self):
        t1 = Text("矩阵分类的终极答案", font=SONG, weight="BOLD", font_size=40,
                  color=RED).move_to([0, 3.1, 0])
        t2 = Text("若尔当标准型", font=SONG, weight="BOLD", font_size=110,
                  color="#8B8BE8").move_to([0, 0.4, 0])
        t2.set_stroke(WHITE, 2, background=True)
        self.play(FadeIn(t1, lag_ratio=0.1), run_time=0.35)
        self.play(FadeIn(t2, scale=1.1), run_time=0.4)
        cards = VGroup(*[rand_card(self.rng, 2 if i % 2 else 3,
                                   scale=0.8 + self.rng.uniform(0, 0.5))
                         .move_to([self.rng.uniform(-6.5, 6.5),
                                   self.rng.uniform(-3.4, 2.2), 0])
                         .rotate(self.rng.uniform(-0.4, 0.4))
                         for i in range(14)])
        cards.set_opacity(0.85)
        self.play(LaggedStart(*[GrowFromCenter(c) for c in cards],
                              lag_ratio=0.04), run_time=0.5)
        self.reg(t1, t2, cards)
        self.sub_in("高等代数中都能相似对角化，对吗？", 0.2)

    # ---------- S1 提问 1.3-4.9 ----------
    def s1_question(self):
        ring = VGroup(*[Circle(radius=1.2 + i * 1.5)
                        .set_stroke(width=0).set_fill(RED, 0.22 - i * 0.05)
                        for i in range(4)])
        ring.move_to([0, 0.3, 0])
        self.play(LaggedStart(*[ring[i].animate.scale(1).set_opacity(1)
                                for i in range(4)], lag_ratio=0.12), run_time=0.5)
        q = Text("任意方阵都能相似对角化？", font=SONG, weight="BOLD",
                 font_size=62, color=INK).move_to([0, 0.4, 0])
        self.play(FadeIn(q, lag_ratio=0.08), run_time=0.55)
        self.reg(ring, q)
        m = grid_matrix([[("a", BLUE, CFB), ("1", CR, CFR)],
                         [("0", BLUE, CFB), ("a", BLUE, CFB)]], cell_w=0.8)
        m.move_to([0, -1.4, 0]).scale(0.95)
        self.play(FadeIn(m, scale=1.2), run_time=0.45)
        self.reg(m)
        self.wait(0.55)
        self.wipe(0.3)
        no = Text("当然不对！", font=SONG, weight="BOLD", font_size=96,
                  color=RED).move_to([0, -0.2, 0])
        self.play(FadeIn(no, scale=1.3), run_time=0.35)
        self.reg(no)
        self.sub_in("当然不对了", 0.2)
        self.wait(0.55)
        self.wipe(0.3)

    # ---------- S2 高等代数 4.9-9.6 ----------
    def s2_algebra(self):
        t = Text("高等代数", font=SONG, weight="BOLD", font_size=72,
                 color=INK).move_to([0, 3.0, 0])
        self.play(FadeIn(t), run_time=0.4)
        self.reg(t)
        cards = VGroup(*[rand_card(self.rng, 2 if i % 3 else 3,
                                   scale=0.7 + self.rng.uniform(0, 0.6))
                         .move_to([self.rng.uniform(-6.8, 6.8),
                                   self.rng.uniform(-3.2, 1.2), 0])
                         .rotate(self.rng.uniform(-0.35, 0.35))
                         for i in range(20)])
        self.play(LaggedStart(*[FadeIn(c, scale=0.5) for c in cards],
                              lag_ratio=0.05), run_time=0.9)
        self.reg(cards)
        self.play(*[c.animate.shift(self.rng.uniform(-0.5, 0.5) * RIGHT
                                    + self.rng.uniform(-0.3, 0.3) * UP)
                    for c in cards], run_time=1.4, rate_func=there_and_back)
        self.play(*[c.animate.scale(0.75).set_opacity(0.25) for c in cards],
                  run_time=0.7)
        self.play(FadeOut(cards), run_time=0.4)
        self.cur.remove(cards)
        self.sub_in("有一个被称为矩阵分类终极答案的工具", 0.3)
        self.wait(0.9)
        self.wipe(0.3)

    # ---------- S3 标题 9.6-14.6 ----------
    def s3_title(self):
        t = Text("若尔当标准型", font=SONG, weight="BOLD", font_size=96,
                 color="#8B8BE8").move_to([0, 1.3, 0])
        s = Text("矩阵分类终极答案", font=SONG, weight="BOLD", font_size=34,
                 color=RED).move_to([0, 0.15, 0])
        self.play(FadeIn(t, lag_ratio=0.08), run_time=0.5)
        self.play(FadeIn(s), run_time=0.35)
        m = grid_matrix([[(r"\lambda", CB, CFB), ("1", CR, CFR), ("0", CB, CFB)],
                         [("0", CB, CFB), (r"\lambda", CB, CFB), ("1", CR, CFR)],
                         [("0", CB, CFB), ("0", CB, CFB), (r"\lambda", CB, CFB)]],
                        cell_w=0.85)
        m.move_to([0, -1.85, 0]).scale(0.95)
        self.play(FadeIn(m, scale=1.15), run_time=0.5)
        self.reg(t, s, m)
        self.sub_in("叫做若尔当标准型", 0.25)
        self.wait(0.8)
        self.wipe(0.3)
        w = Text("研究矩阵的世界", font=SONG, weight="BOLD", font_size=54,
                 color=BLUE).move_to([0, 2.6, 0])
        self.play(FadeIn(w, lag_ratio=0.08), run_time=0.45)
        cards = VGroup()
        pos = [(-5.2, 0.4), (-3.4, -1.6), (-1.6, 0.2), (0.4, -1.9), (2.2, 0.1),
               (4.2, -1.4), (5.8, 0.3), (-4.4, -2.9), (1.2, 1.3), (5.0, 1.4),
               (-1.2, -2.6), (3.2, 1.5)]
        for i, p in enumerate(pos):
            c = rand_card(self.rng, 3 if i % 2 else 2,
                          scale=0.75 + self.rng.uniform(0, 0.4))
            c.move_to([p[0], p[1], 0]).rotate(self.rng.uniform(-0.3, 0.3))
            cards.add(c)
        self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in cards],
                              lag_ratio=0.04), run_time=0.7)
        self.reg(w, cards)
        self.sub_in("它处理的正是一类让对角化彻底失效的矩阵", 0.25)
        self.wait(1.0)
        self.wipe(0.3)

    # ---------- S4 充要条件 14.6-28.6 ----------
    def s4_condition(self):
        t = VGroup(Text("n", font=SONG, weight="BOLD", font_size=44,
                        color=INK, slant=ITALIC),
                   Text(" 阶方阵可对角化的充要条件", font=SONG, weight="BOLD",
                        font_size=44, color=INK)
                   ).arrange(RIGHT, buff=0.05).move_to([0, 3.3, 0])
        self.play(FadeIn(t, lag_ratio=0.06), run_time=0.5)
        self.reg(t)
        g1 = Text("几何重数", font=SONG, weight="BOLD", font_size=46,
                  color=GREEN).move_to([-3.3, 1.9, 0])
        g2 = Text("线性无关特征向量的个数", font=SONG, font_size=26,
                  color=GREEN).move_to([-3.3, 1.2, 0])
        self.play(FadeIn(g1, lag_ratio=0.08), run_time=0.45)
        self.play(FadeIn(g2), run_time=0.3)
        base_y = -1.9
        base1 = Line([-4.35, base_y, 0], [-2.25, base_y, 0]).set_stroke(INK, 3)
        bar1 = Rectangle(width=0.95, height=0.001).set_fill(GREEN, 1).set_stroke(width=0)
        bar1.move_to([-3.3, base_y, 0]).align_to(base1, DOWN).shift(UP * 0.02)
        n1 = DecimalNumber(0, num_decimal_places=0, font_size=42, color=GREEN).move_to([-3.3, base_y + 1.5, 0])
        self.play(FadeIn(base1), FadeIn(bar1), FadeIn(n1), run_time=0.3)
        self.wait(0.8)
        self.reg(g1, g2, base1, bar1, n1)
        tr = ValueTracker(0)
        bar1.add_updater(lambda m: m.become(
            Rectangle(width=0.95, height=max(tr.get_value() * 0.42, 0.001))
            .set_fill(GREEN, 1).set_stroke(width=0)
            .move_to([-3.3, base_y, 0]).align_to(base1, DOWN).shift(UP * 0.02)))
        n1.add_updater(lambda m: m.set_value(int(round(tr.get_value()))))
        self.play(tr.animate.set_value(3), run_time=1.0)
        bar1.clear_updaters(); n1.clear_updaters()
        self.sub_in("它的每个特征值的几何重数", 0.25)
        self.wait(0.6)
        a1 = Text("代数重数", font=SONG, weight="BOLD", font_size=46,
                  color=BLUE).move_to([3.3, 1.9, 0])
        a2 = Text("该特征值作为特征多项式根的重数", font=SONG, font_size=26,
                  color=BLUE).move_to([3.3, 1.2, 0])
        self.play(FadeIn(a1, lag_ratio=0.08), run_time=0.45)
        self.play(FadeIn(a2), run_time=0.3)
        base2 = Line([2.25, base_y, 0], [4.35, base_y, 0]).set_stroke(INK, 3)
        bar2 = Rectangle(width=0.95, height=0.001).set_fill(BLUE, 1).set_stroke(width=0)
        bar2.move_to([3.3, base_y, 0]).align_to(base2, DOWN).shift(UP * 0.02)
        n2 = DecimalNumber(0, num_decimal_places=0, font_size=42, color=BLUE).move_to([3.3, base_y + 1.5, 0])
        self.play(FadeIn(base2), FadeIn(bar2), FadeIn(n2), run_time=0.3)
        self.reg(a1, a2, base2, bar2, n2)
        tr2 = ValueTracker(0)
        bar2.add_updater(lambda m: m.become(
            Rectangle(width=0.95, height=max(tr2.get_value() * 0.42, 0.001))
            .set_fill(BLUE, 1).set_stroke(width=0)
            .move_to([3.3, base_y, 0]).align_to(base2, DOWN).shift(UP * 0.02)))
        n2.add_updater(lambda m: m.set_value(int(round(tr2.get_value()))))
        self.play(tr2.animate.set_value(3), run_time=1.0)
        bar2.clear_updaters(); n2.clear_updaters()
        self.wait(1.7)
        eq = MathTex("=", font_size=76, color=GREEN).move_to([0, base_y + 0.85, 0])
        self.play(FadeIn(eq, scale=1.4), run_time=0.3)
        self.reg(eq)
        self.sub_in("等于它的代数重数", 0.25)
        self.wait(0.7)
        fl1 = bar1.copy().set_stroke(GOLD, 4).set_fill(GOLD, 0.55)
        fl2 = bar2.copy().set_stroke(GOLD, 4).set_fill(GOLD, 0.55)
        self.play(FadeIn(fl1), FadeIn(fl2), run_time=0.35)
        self.reg(fl1, fl2)
        self.wait(2.4)
        self.wipe(0.3)

    # ---------- S5 完全对角化 28.6-34.6 ----------
    def s5_diagonal(self):
        t = sec_title("满足条件时：可以完全对角化", GREEN, y=3.2)
        self.play(FadeIn(t, lag_ratio=0.08), run_time=0.45)
        X = lambda i, j: ("X", CR, CFR)
        ent = [[(r"\lambda_1", CB, CFB), ("X", CGR, CFGR), ("X", CGR, CFGR)],
               [("X", CGR, CFGR), (r"\lambda_2", CB, CFB), ("X", CGR, CFGR)],
               [("X", CGR, CFGR), ("X", CGR, CFGR), (r"\lambda_3", CB, CFB)]]
        m = grid_matrix(ent)
        m.move_to([0, -0.85, 0])
        self.play(FadeIn(m, scale=1.1), run_time=0.5)
        self.reg(t, m)
        self.sub_in("当所有特征值都满足这个条件时", 0.25)
        # X -> 红
        new = [[(r"\lambda_1", CB, CFB), ("X", CR, CFR), ("X", CR, CFR)],
               [("X", CR, CFR), (r"\lambda_2", CB, CFB), ("X", CR, CFR)],
               [("X", CR, CFR), ("X", CR, CFR), (r"\lambda_3", CB, CFB)]]
        m2 = grid_matrix(new).move_to(m.get_center())
        self.play(ReplacementTransform(m, m2), run_time=0.45)
        self.cur[self.cur.index(m)] = m2
        self.wait(0.4)
        # X -> O
        new2 = [[(r"\lambda_1", CB, CFB), ("O", CB, CFB), ("O", CB, CFB)],
                [("O", CB, CFB), (r"\lambda_2", CB, CFB), ("O", CB, CFB)],
                [("O", CB, CFB), ("O", CB, CFB), (r"\lambda_3", CB, CFB)]]
        m3 = grid_matrix(new2).move_to(m.get_center())
        self.play(ReplacementTransform(m2, m3), run_time=0.45)
        self.cur[self.cur.index(m2)] = m3
        # 对角元绿色高亮
        hi = VGroup()
        for k in range(3):
            c = m3[0][k * 3 + k]
            hl = RoundedRectangle(corner_radius=0.14, width=CELL, height=CELL)
            hl.set_stroke(GREEN, 3.5).set_fill(GREEN, 0.25)
            hl.move_to(c.get_center())
            hi.add(hl)
        self.play(LaggedStart(*[FadeIn(h, scale=1.15) for h in hi], lag_ratio=0.15),
                  run_time=0.5)
        self.reg(hi)
        d = Text("对角阵", font=SONG, weight="BOLD", font_size=44,
                 color=GREEN).move_to([0, -3.0, 0])
        self.play(FadeIn(d), run_time=0.3)
        self.reg(d)
        self.sub_in("变成干干净净的对角阵", 0.25)
        self.wait(1.5)
        self.wipe(0.3)

    # ---------- S6 失败 34.6-40.6 ----------
    def s6_fail(self):
        t = sec_title("一旦几何重数 < 代数重数", RED, y=3.2)
        self.play(FadeIn(t, lag_ratio=0.08), run_time=0.45)
        self.reg(t)
        base_y = -1.8
        base = Line([-3.6, base_y, 0], [0.2, base_y, 0]).set_stroke(INK, 3)
        b1 = Rectangle(width=0.95, height=2 * 0.42).set_fill(BLUE, 1).set_stroke(width=0)
        b1.move_to([-2.8, base_y, 0]).align_to(base, DOWN).shift(UP * 0.02)
        b2 = Rectangle(width=0.95, height=1 * 0.42).set_fill(GREEN, 1).set_stroke(width=0)
        b2.move_to([-1.3, base_y, 0]).align_to(base, DOWN).shift(UP * 0.02)
        n1 = Text("2", font=SONG, font_size=40, color=BLUE).move_to([-2.8, base_y + 1.0, 0])
        n2 = Text("1", font=SONG, font_size=40, color=GREEN).move_to([-1.3, base_y + 0.58, 0])
        l1 = Text("代数重数", font=SONG, font_size=28, color=BLUE).move_to([-2.8, base_y - 0.45, 0])
        l2 = Text("几何重数", font=SONG, font_size=28, color=GREEN).move_to([-1.3, base_y - 0.45, 0])
        neq = Text("2 ≠ 1", font=SONG, weight="BOLD", font_size=64,
                   color=RED).move_to([-2.0, 1.5, 0])
        self.play(FadeIn(base), FadeIn(b1), FadeIn(b2), FadeIn(n1), FadeIn(n2),
                  FadeIn(l1), FadeIn(l2), run_time=0.6)
        self.play(FadeIn(neq, scale=1.2), run_time=0.3)
        self.reg(base, b1, b2, n1, n2, l1, l2, neq)
        m = grid_matrix([[(r"\lambda", CGR, CFGR), ("1", CR, CFR)],
                         [("o", CGR, CFGR), (r"\lambda", CGR, CFGR)]], cell_w=0.95)
        m.move_to([3.3, -0.7, 0])
        bracket_side = bracket(2.1, color=CGR, sw=3)
        self.play(FadeIn(m), run_time=0.45)
        self.reg(m)
        cross = VGroup(Line(ORIGIN, (1.8, 1.6, 0)), Line(ORIGIN, (1.8, -1.6, 0)))
        cross.set_stroke(RED, 8).move_to(m.get_center())
        self.play(Create(cross), run_time=0.4)
        f = Text("对角化失败", font=SONG, weight="BOLD", font_size=44,
                 color=RED).move_to([3.3, -2.75, 0])
        self.play(FadeIn(f), run_time=0.3)
        self.reg(cross, f)
        self.sub_in("但一旦某个特征值的几何重数小于代数重数", 0.25)
        self.wait(0.5)
        self.sub_in("对角化就失败了", 0.25)
        self.wait(1.4)
        self.wipe(0.3)

    # ---------- S7 登场 40.6-51.6 ----------
    def s7_entrance(self):
        t = sec_title("若尔当标准型登场", PURPLE, y=3.3)
        self.play(FadeIn(t, lag_ratio=0.08), run_time=0.45)
        self.reg(t)
        ent = [[(r"\lambda", CB, CFB), ("O", CB, CFB), ("O", CB, CFB)],
               [("O", CB, CFB), (r"\lambda", CB, CFB), ("O", CB, CFB)],
               [("O", CB, CFB), ("O", CB, CFB), (r"\lambda", CB, CFB)]]
        m = grid_matrix(ent)
        m.move_to([0, -0.8, 0]).scale(1.05)
        self.play(FadeIn(m, scale=1.15), run_time=0.5)
        self.reg(m)
        s = Text("允许在对角线上方出现 1", font=SONG, weight="BOLD", font_size=38,
                 color=RED).move_to([0, 2.25, 0])
        self.play(FadeIn(s, lag_ratio=0.08), run_time=0.4)
        self.reg(s)
        self.sub_in("这时若尔当标准型登场", 0.25)
        # 红色 1 出现
        ones = []
        for (i, j) in ((0, 1), (1, 2)):
            c = m[0][i * 3 + j]
            nc = cell("1", CR, CFR, font_size=38).move_to(c.get_center())
            hl = RoundedRectangle(corner_radius=0.14, width=CELL, height=CELL)
            hl.set_stroke("#E88A4B", 3.5).set_fill(CFR, 0.9).move_to(c.get_center())
            ones.append(VGroup(hl, nc))
        self.play(LaggedStart(*[ReplacementTransform(c.copy(), g)
                                for c, g in zip([m[0][1], m[0][5]], ones)],
                                lag_ratio=0.2), run_time=0.55)
        self.reg(*ones)
        self.sub_in("而是允许在主对角线上方出现一些 1", 0.25)
        self.wait(0.6)
        # 金色缝合折线 (1,1)->(1,2)->(2,2)->(2,3)->(3,3)
        pts = [m[0][0].get_center(), m[0][1].get_center(), m[0][4].get_center(),
               m[0][5].get_center(), m[0][8].get_center()]
        poly = VMobject().set_points_as_corners(pts).set_stroke(GOLD, 4.5)
        self.play(Create(poly), run_time=1.0)
        self.reg(poly)
        w1 = Text("把特征值缝合起来", font=SONG, weight="BOLD", font_size=40,
                  color=GOLD).move_to([3.6, -1.0, 0])
        self.play(FadeIn(w1), run_time=0.3)
        self.reg(w1)
        w2 = Text("一个若尔当块", font=SONG, weight="BOLD", font_size=48,
                  color=PURPLE).move_to([3.6, -2.0, 0])
        self.play(FadeIn(w2), run_time=0.3)
        self.reg(w2)
        self.sub_in("这些 1 把单个的特征值缝合成一个若尔当块", 0.25)
        self.wait(3.2)
        self.wipe(0.3)

    # ---------- S8 若尔当块 51.6-57.6 ----------
    def s8_block(self):
        t = sec_title("若尔当块是什么？", PURPLE, y=3.3)
        self.play(FadeIn(t, lag_ratio=0.08), run_time=0.45)
        self.reg(t)
        ent = [[(r"\lambda", CB, CFB), ("1", CR, CFR), ("o", CGR, CFGR), ("o", CGR, CFGR)],
               [("o", CGR, CFGR), (r"\lambda", CB, CFB), ("1", CR, CFR), ("o", CGR, CFGR)],
               [("o", CGR, CFGR), ("o", CGR, CFGR), (r"\lambda", CB, CFB), ("1", CR, CFR)],
               [("o", CGR, CFGR), ("o", CGR, CFGR), ("o", CGR, CFGR), (r"\lambda", CB, CFB)]]
        m = grid_matrix(ent, cell_w=0.92)
        m.move_to([-2.4, -0.8, 0]).scale(0.98)
        # 高亮描边：λ 对角蓝框、1 橙框
        hl = VGroup()
        for k in range(4):
            hl.add(RoundedRectangle(corner_radius=0.14, width=CELL, height=CELL)
                   .set_stroke(BLUE, 3).set_fill(opacity=0)
                   .move_to(m[0][k * 5].get_center()))
        for k in range(3):
            hl.add(RoundedRectangle(corner_radius=0.14, width=CELL, height=CELL)
                   .set_stroke("#E88A4B", 3).set_fill(opacity=0)
                   .move_to(m[0][k * 5 + 1].get_center()))
        self.play(FadeIn(m), run_time=0.5)
        self.play(FadeIn(hl), run_time=0.4)
        self.reg(t, m, hl)
        arrow = Arrow([-0.4, 1.7, 0], [2.4, 2.15, 0], buff=0, stroke_width=6,
                      color=GOLD)
        lab = VGroup(Text("超对角线：全是 ", font=SONG, font_size=34, color=RED),
                     MathTex("1", font_size=40, color=RED)
                     ).arrange(RIGHT, buff=0.05).move_to([3.5, 2.35, 0])
        self.play(GrowArrow(arrow), FadeIn(lab), run_time=0.5)
        self.reg(arrow, lab)
        box = VGroup(RoundedRectangle(corner_radius=0.12, width=2.9, height=2.5)
                     .set_stroke(INK, 2.5).set_fill(WHITE, 0.7))
        box[0].move_to([3.7, -0.6, 0])
        lines = VGroup(Text("几乎对角", font=SONG, font_size=32, color=BLUE),
                       Text("+", font=SONG, font_size=32, color=INK),
                       Text("超对角线全为 1", font=SONG, font_size=32, color=RED),
                       Text("+", font=SONG, font_size=32, color=INK),
                       Text("上三角矩阵", font=SONG, font_size=32, color=GREEN),
                       ).arrange(DOWN, buff=0.22).move_to([3.7, -0.6, 0])
        box.add(lines)
        self.play(FadeIn(box), run_time=0.5)
        self.reg(box)
        self.sub_in("一个若尔当块就是一个几乎对角", 0.25)
        self.wait(0.5)
        self.sub_in("但超对角线上全是 1 的上三角矩阵", 0.25)
        w = Text("若尔当块", font=SONG, weight="BOLD", font_size=52,
                 color=PURPLE).move_to([-2.4, 1.9, 0])
        self.play(FadeIn(w), run_time=0.3)
        self.reg(w)
        self.wait(1.6)
        self.wipe(0.3)

    # ---------- S9 经典例子 57.6-64.6 ----------
    def s9_classic(self):
        t = sec_title("最经典的例子", INK, y=3.3)
        self.play(FadeIn(t, lag_ratio=0.08), run_time=0.4)
        m = grid_matrix([[("a", CGR, CFGR), ("1", CR, CFR)],
                         [("o", CGR, CFGR), ("a", CGR, CFGR)]], cell_w=1.0)
        m.move_to([0, 0.5, 0])
        self.play(FadeIn(m), run_time=0.5)
        self.reg(t, m)
        self.sub_in("最经典的例子是矩阵 [[a, 1], [0, a]]", 0.25)
        l1 = Text("特征多项式:", font=SONG, font_size=34, color=INK).move_to([-1.8, -1.6, 0])
        self.play(FadeIn(l1), run_time=0.3)
        e1 = MathTex(r"(\mathbf{a}-\lambda)^2", font_size=56,
                     color="#6A5AE8").move_to([1.0, -1.6, 0])
        self.play(FadeIn(e1, scale=1.2), run_time=0.4)
        self.reg(l1, e1)
        self.wait(0.6)
        l2 = Text("代数重数 =", font=SONG, font_size=34, color=BLUE).move_to([-1.4, -2.5, 0])
        n2 = DecimalNumber(0, num_decimal_places=0, font_size=40, color=BLUE).move_to([0.4, -2.5, 0])
        self.play(FadeIn(l2), FadeIn(n2), run_time=0.3)
        self.play(ChangeDecimalToValue(n2, 2), run_time=0.7)
        self.reg(l2, n2)
        self.sub_in("它的特征多项式是 (a 减 λ) 的平方，代数重数是 2", 0.25)
        self.wait(1.8)
        self.wipe(0.3)

    # ---------- S10 特征向量 64.6-71.6 ----------
    def s10_eigen(self):
        t = sec_title("求解特征向量", INK, y=3.3)
        e = MathTex(r"(\mathbf{A}-\lambda\mathbf{I})\mathbf{v}=\mathbf{o}",
                    font_size=54, color="#6A5AE8").move_to([0, 2.3, 0])
        self.play(FadeIn(t, lag_ratio=0.08), FadeIn(e, scale=1.15), run_time=0.5)
        self.reg(t, e)
        ax = VGroup(Line([-4.6, 0, 0], [4.6, 0, 0]).set_stroke(GRIDC, 2),
                    Line([0, -2.8, 0], [0, 2.8, 0]).set_stroke(GRIDC, 2))
        ax.move_to([0, -0.5, 0])
        ax[0].shift(DOWN * 0.0)
        rng = np.random.default_rng(7)
        dots = VGroup(*[Dot([rng.uniform(-3.9, 3.9), -0.5 + rng.uniform(-2.1, 2.1), 0],
                            radius=0.045, color=CYAN2).set_opacity(0.85)
                        for _ in range(26)])
        self.play(FadeIn(ax), LaggedStart(*[GrowFromCenter(d) for d in dots],
                                          lag_ratio=0.02), run_time=0.7)
        self.reg(ax, dots)
        line = Line([-4.1, -2.55, 0], [4.1, 1.55, 0]).set_stroke(GREEN, 4)
        self.play(Create(line), run_time=0.8)
        self.reg(line)
        arr = Arrow([0, -0.5, 0], [1.35, 0.02, 0], buff=0, stroke_width=7,
                    color=GREEN, max_tip_length_to_length_ratio=0.25)
        self.play(GrowArrow(arr), run_time=0.35)
        self.reg(arr)
        s1 = Text("只有一个线性无关的解", font=SONG, font_size=34,
                  color=INK).move_to([0, -3.0, 0])
        self.play(FadeIn(s1), run_time=0.35)
        self.reg(s1)
        l = Text("几何重数 =", font=SONG, font_size=32, color=GREEN).move_to([1.4, -2.35, 0])
        n = DecimalNumber(0, num_decimal_places=0, font_size=38, color=GREEN).move_to([3.2, -2.35, 0])
        self.play(FadeIn(l), FadeIn(n), run_time=0.3)
        self.play(ChangeDecimalToValue(n, 1), run_time=0.6)
        self.reg(l, n)
        self.sub_in("你会发现它只有一个线性无关的解，几何重数是 1", 0.25)
        self.wait(2.2)
        self.wipe(0.3)

    # ---------- S11 天生若尔当块 71.6-76.6 ----------
    def s11_born(self):
        t = sec_title("没有任何办法被对角化", RED, y=3.2)
        self.play(FadeIn(t, lag_ratio=0.08), run_time=0.45)
        ent = [[("a", CGR, CFGR), ("1", CR, CFR)],
               [("o", CGR, CFGR), ("a", CGR, CFGR)]]
        m = grid_matrix(ent, cell_w=1.0)
        m.move_to([0, -0.4, 0])
        self.play(FadeIn(m), run_time=0.5)
        self.reg(t, m)
        tr = Text("尝试对角化...", font=SONG, font_size=32,
                  color=CGR).move_to([0, -2.2, 0])
        self.play(FadeIn(tr), run_time=0.3)
        self.reg(tr)
        self.sub_in("这个矩阵没有任何办法被对角化", 0.25)
        # 1 闪蓝色（尝试中）
        c1 = m[0][1]
        self.play(c1.animate.set_stroke(BLUE, 4).set_fill(CFB, 1), run_time=0.25)
        self.play(c1.animate.set_stroke(CR, 2.6).set_fill(CFR, 1), run_time=0.25)
        w1 = Text("它天生就是", font=SONG, weight="BOLD", font_size=44,
                  color=PURPLE).move_to([-2.6, 1.6, 0])
        self.play(FadeIn(w1), run_time=0.3)
        self.reg(w1)
        w2 = Text("一个若尔当块", font=SONG, weight="BOLD", font_size=52,
                  color=PURPLE).move_to([0.6, 1.6, 0])
        hl = RoundedRectangle(corner_radius=0.14, width=CELL, height=CELL)
        hl.set_stroke(PURPLE, 3.5).set_fill(PURPLE, 0.28).move_to(m[0][1].get_center())
        self.play(FadeIn(w2, lag_ratio=0.1), FadeIn(hl), run_time=0.5)
        self.reg(w2, hl)
        self.sub_in("它天生就是一个若尔当块", 0.25)
        self.wait(1.2)
        self.wipe(0.3)

    # ---------- S12 定理 76.6-85.6 ----------
    def s12_theorem(self):
        t = sec_title("若尔当标准型定理", PURPLE, y=3.3)
        s = Text("在复数域上", font=SONG, weight="BOLD", font_size=36,
                 color=GREEN).move_to([0, 2.4, 0])
        self.play(FadeIn(t, lag_ratio=0.08), run_time=0.45)
        self.play(FadeIn(s), run_time=0.3)
        self.reg(t, s)
        digits = [["6", "8", "7", "4"], ["8", "8", "8", "0"],
                  ["4", "5", "2", "3"], ["5", "7", "5", "1"]]
        ent = [[(d, CB, CFB) for d in row] for row in digits]
        m = grid_matrix(ent, cell_w=0.98)
        m.move_to([1.1, -0.6, 0])
        self.play(FadeIn(m), run_time=0.55)
        self.reg(m)
        sim = Text("相似", font=SONG, weight="BOLD", font_size=40,
                   color=RED).move_to([-3.4, -0.3, 0])
        ar = Arrow([-2.6, -0.3, 0], [-1.55, -0.3, 0], buff=0, stroke_width=6,
                   color=RED)
        self.play(FadeIn(sim), GrowArrow(ar), run_time=0.4)
        self.reg(sim, ar)
        any_a = VGroup(Text("任何方阵", font=SONG, font_size=36, color=BLUE),
                       MathTex(r"\mathbf{A}", font_size=44, color=BLUE)
                       ).arrange(RIGHT, buff=0.15).move_to([1.1, -2.75, 0])
        self.play(FadeIn(any_a), run_time=0.3)
        self.reg(any_a)
        self.sub_in("若尔当标准型定理断言：在复数域上", 0.25)
        # 数字矩阵 → 若尔当分块
        ent2 = [[(r"\lambda", "#8B7BE8", "#EFEFFB"), ("1", CR, CFR), ("O", CGR, CFGR), ("O", CGR, CFGR)],
                [("O", CGR, CFGR), (r"\lambda", "#8B7BE8", "#EFEFFB"), ("O", CGR, CFGR), ("O", CGR, CFGR)],
                [("O", CGR, CFGR), ("O", CGR, CFGR), (r"\lambda", "#8B7BE8", "#EFEFFB"), ("1", CR, CFR)],
                [("O", CGR, CFGR), ("O", CGR, CFGR), ("O", CGR, CFGR), (r"\lambda", "#8B7BE8", "#EFEFFB")]]
        m2 = grid_matrix(ent2, cell_w=0.98).move_to(m.get_center())
        self.play(ReplacementTransform(m, m2),
                  FadeOut(any_a), FadeOut(sim), FadeOut(ar), run_time=0.9)
        self.cur[self.cur.index(m)] = m2
        self.cur.remove(any_a); self.cur.remove(sim); self.cur.remove(ar)
        self.wait(0.5)
        d = Text("由若干个若尔当块拼成的分块对角矩阵", font=SONG, weight="BOLD",
                 font_size=36, color=INK).move_to([0, -3.0, 0])
        self.play(FadeIn(d, lag_ratio=0.06), run_time=0.4)
        self.reg(d)
        self.sub_in("任何方阵都相似于一个由若干个若尔当块拼成的分块对角矩阵", 0.25)
        self.wait(3.1)
        self.wipe(0.3)

    # ---------- S13 唯一性 85.6-89.6 ----------
    def s13_unique(self):
        t = sec_title("块的大小唯一确定", PURPLE, y=3.3)
        self.play(FadeIn(t, lag_ratio=0.08), run_time=0.4)
        ent = [[(r"\lambda", "#8B7BE8", "#EFEFFB"), ("1", CR, CFR), ("O", CGR, CFGR)],
               [("O", CGR, CFGR), (r"\lambda", "#8B7BE8", "#EFEFFB"), ("O", CGR, CFGR)],
               [("O", CGR, CFGR), ("O", CGR, CFGR), (r"\lambda", GREEN, CFG)]]
        m = grid_matrix(ent)
        m.move_to([0.6, -0.7, 0])
        self.play(FadeIn(m), run_time=0.5)
        self.reg(t, m)
        lab1 = Text("大小 2", font=SONG, font_size=34, color="#8B7BE8").move_to([-2.8, 0.9, 0])
        lab2 = Text("大小 1", font=SONG, font_size=34, color=GREEN).move_to([3.4, -1.7, 0])
        box1 = SurroundingRectangle(m[0][0], buff=0.08).set_stroke("#8B7BE8", 3)
        box1.stretch_to_fit_height(2 * CELL + 0.1).move_to(
            [(m[0][0].get_center()[0] + m[0][4].get_center()[0]) / 2,
             (m[0][0].get_center()[1] + m[0][4].get_center()[1]) / 2, 0])
        box2 = SurroundingRectangle(m[0][8], buff=0.08).set_stroke(GREEN, 3)
        self.play(FadeIn(box1), FadeIn(lab1), FadeIn(box2), FadeIn(lab2), run_time=0.5)
        self.reg(lab1, lab2, box1, box2)
        self.sub_in("并且这些块的大小，在忽略块的排列次序后是唯一确定的", 0.25)
        # 重排
        ent3 = [[(r"\lambda", GREEN, CFG), ("O", CGR, CFGR), ("O", CGR, CFGR)],
                [("O", CGR, CFGR), (r"\lambda", "#8B7BE8", "#EFEFFB"), ("1", CR, CFR)],
                [("O", CGR, CFGR), ("O", CGR, CFGR), (r"\lambda", "#8B7BE8", "#EFEFFB")]]
        m3 = grid_matrix(ent3).move_to(m.get_center())
        lab1b = Text("大小 1", font=SONG, font_size=34, color=GREEN).move_to([-2.8, 1.1, 0])
        lab2b = Text("大小 2", font=SONG, font_size=34, color="#8B7BE8").move_to([3.4, -1.5, 0])
        self.play(ReplacementTransform(m, m3), ReplacementTransform(lab1, lab1b),
                  ReplacementTransform(lab2, lab2b), run_time=0.7)
        self.cur[self.cur.index(m)] = m3
        self.cur[self.cur.index(lab1)] = lab1b
        self.cur[self.cur.index(lab2)] = lab2b
        ok = Text("✓ 忽略排列次序后，大小唯一确定", font=SONG, weight="BOLD",
                  font_size=36, color=GREEN).move_to([0, -3.0, 0])
        self.play(FadeIn(ok), run_time=0.35)
        self.reg(ok)
        self.wait(0.8)
        self.wipe(0.3)

    # ---------- S14 指纹 89.6-97.6 ----------
    def s14_fingerprint(self):
        t = Text("可用的，而且是唯一的", font=SONG, weight="BOLD", font_size=58,
                 color="#8B8BE8").move_to([0, 3.0, 0])
        self.play(FadeIn(t, lag_ratio=0.08), run_time=0.5)
        self.reg(t)
        rip = fingerprint(scale=1.15, color="#7A6AE0")
        rip.move_to([0, -0.4, 0])
        self.play(Create(rip[1]), run_time=1.1)
        self.add(rip[0])
        self.reg(rip)
        J = MathTex(r"\mathbf{J}", font_size=80, color=RED).move_to([0, -0.4, 0])
        self.play(FadeIn(J, scale=1.4), run_time=0.4)
        self.reg(J)
        self.sub_in("这意味着若尔当标准型不仅是可用的", 0.25)
        self.wait(0.6)
        self.wipe(0.15)
        t2 = VGroup(Text("若尔当标准型不仅是", font=SONG, weight="BOLD", font_size=40,
                         color=INK),
                    Text("可用的", font=SONG, weight="BOLD", font_size=40, color=BLUE),
                    Text("，而且是", font=SONG, weight="BOLD", font_size=40, color=INK),
                    Text("唯一的", font=SONG, weight="BOLD", font_size=40, color=RED),
                    ).arrange(RIGHT, buff=0.08).move_to([0, 1.1, 0])
        self.play(FadeIn(t2), run_time=0.4)
        self.reg(t2)
        t3 = VGroup(Text("它是矩阵在这个", font=SONG, font_size=36, color=INK),
                    Text("相似", font=SONG, weight="BOLD", font_size=36, color=BLUE),
                    Text("意义下的", font=SONG, font_size=36, color=INK),
                    Text("精确指纹", font=SONG, weight="BOLD", font_size=36, color=RED),
                    ).arrange(RIGHT, buff=0.08).move_to([0, 0.15, 0])
        self.play(FadeIn(t3), run_time=0.4)
        self.reg(t3)
        rip2 = fingerprint(scale=0.9, color="#7A6AE0").move_to([0, -1.9, 0])
        self.play(Create(rip2[1]), run_time=0.9)
        self.add(rip2[0])
        self.reg(rip2)
        self.sub_in("它是矩阵在这个相似意义下的精确指纹", 0.25)
        self.wait(1.9)
        self.wipe(0.35)

    # ---------- S15 3D 网格狼 97.6-105 ----------
    def s15_grid_wolf(self):
        bg = Rectangle(width=16.4, height=9.4).set_fill("#F2E3C0", 1).set_stroke(width=0)
        self.add(bg)
        self.reg(bg)
        vp = [0, -1.1, 0]     # 灭点
        glow = VGroup()
        # 放射线
        for k in range(-7, 8):
            p_top = [k * 1.35, 4.2, 0]
            glow.add(glow_line(vp, p_top, "#5FD8C8", 2.2))
        # 横线（透视：靠近灭点密）
        for i in range(14):
            f = (i + 1) / 14.0
            y = -1.1 + (5.3 * f * f)
            glow.add(glow_line([-8 * (0.25 + 0.75 * f), y, 0],
                               [8 * (0.25 + 0.75 * f), y, 0], "#5FD8C8", 2.2))
        dark = Rectangle(width=9.2, height=4.6).set_fill("#4A4A52", 0.92)
        dark.set_stroke(width=0)
        dark.move_to([0, 0.6, 0])
        self.play(FadeIn(dark), LaggedStart(*[FadeIn(g) for g in glow[:8]],
                                            lag_ratio=0.03), run_time=0.7)
        self.play(*[FadeIn(g) for g in glow[8:]], run_time=0.5)
        self.reg(dark, glow)
        wolf = simple_wolf(scale=1.15).move_to([0, 0.4, 0])
        self.play(FadeIn(wolf, scale=0.8), run_time=0.5)
        self.reg(wolf)
        for txt in ("我的意思是", "不是所有矩阵都能对角化",
                    "正如不是所有人都能整理成干净的对角线"):
            s = self.sub_in(txt, 0.3)
            self.wait(1.35)
            self.play(FadeOut(s), run_time=0.2)
            self.cur.remove(s)
        self.wipe(0.4)

    # ---------- S16 烟花心形 105-109.5 ----------
    def s16_heart(self):
        bg = Rectangle(width=16.4, height=9.4).set_fill("#1A1216", 1).set_stroke(width=0)
        self.add(bg)
        self.reg(bg)
        dots = heart_points()
        twentyone = Text("21", font=SONG, weight="BOLD", font_size=150,
                         color="#E8535A").move_to([0, 0.25, 0])
        twentyone.set_stroke("#FFD3DC", 1.5, background=True)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots[::3]],
                              lag_ratio=0.008), run_time=1.2)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots[1::3]],
                              lag_ratio=0.008), run_time=0.5)
        self.play(FadeIn(twentyone, scale=1.6), run_time=0.5)
        self.reg(dots, twentyone)
        self.sub_in("有些爱，代数重数很深", 0.3)
        self.wait(0.9)
        self.sub_in("几何重数却只有一个出口", 0.3)
        self.wait(1.0)
        self.wipe(0.4)

    # ---------- S17 撕纸拼贴 109.5-117.5 ----------
    def s17_photos(self):
        bg = Rectangle(width=16.4, height=9.4).set_fill("#2E2418", 1).set_stroke(width=0)
        self.add(bg)
        self.reg(bg)
        rng = np.random.default_rng(11)
        nums_bg = VGroup()
        for _ in range(90):
            d = Text(str(rng.integers(1, 4)), font=SONG, font_size=40,
                     color="#C8A860").move_to([rng.uniform(-7.6, 7.6),
                                               rng.uniform(-4.2, 4.2), 0])
            d.set_opacity(rng.uniform(0.25, 0.6))
            nums_bg.add(d)
        self.play(FadeIn(nums_bg), run_time=0.6)
        self.reg(nums_bg)
        # 2x2 撕纸照片：1 2 / 2 2
        photos = VGroup()
        labels = [("1", -1.15, 1.15), ("2", 1.15, 1.15),
                  ("2", -1.15, -1.15), ("2", 1.15, -1.15)]
        for txt, x, y in labels:
            ph = RoundedRectangle(corner_radius=0.1, width=2.0, height=1.75)
            ph.set_fill("#F5EFE2", 1).set_stroke("#D8CBB2", 2)
            ph.move_to([x, y, 0]).rotate(rng.uniform(-0.08, 0.08))
            num = Text(txt, font=SONG, weight="BOLD", font_size=88,
                       color="#B8923E").move_to(ph.get_center())
            photos.add(VGroup(ph, num))
        self.play(LaggedStart(*[FadeIn(p, scale=0.7, shift=DOWN * 0.4) for p in photos],
                              lag_ratio=0.18), run_time=1.1)
        self.reg(photos)
        self.sub_in("那个孤零零的 1，留在主对角线上方", 0.3)
        self.wait(0.9)
        self.sub_in("像无法删除的旧事", 0.3)
        self.wait(0.8)
        self.sub_in("把同一个名字缝成若尔当块", 0.3)
        self.wait(2.0)
        self.wipe(0.4)

    # ---------- S18 石墙指纹 117.5-125.5 ----------
    def s18_wall(self):
        bg = Rectangle(width=16.4, height=9.4).set_fill("#5A5A60", 1).set_stroke(width=0)
        self.add(bg)
        self.reg(bg)
        # 石墙砖缝
        bricks = VGroup()
        for row, y in enumerate(np.arange(-4.2, 4.3, 0.85)):
            off = 0.6 if row % 2 else 0.0
            for x in np.arange(-7.8 + off, 8.0, 1.7):
                bricks.add(Line([x, y - 0.42, 0], [x, y + 0.42, 0])
                           .set_stroke("#4A4A50", 2))
            bricks.add(Line([-8, y + 0.42, 0], [8, y + 0.42, 0])
                       .set_stroke("#4A4A50", 2))
        self.play(FadeIn(bricks), run_time=0.5)
        self.reg(bricks)
        wolf = simple_wolf(scale=1.5, body="#6E6E76").move_to([0, -0.5, 0])
        self.play(FadeIn(wolf, scale=0.85), run_time=0.5)
        self.reg(wolf)
        fp = fingerprint(scale=0.85, color="#E8B84B").move_to([0, -0.7, 0])
        self.play(Create(fp[1]), run_time=1.0)
        self.add(fp[0])
        self.reg(fp)
        self.sub_in("你可以被相似变换", 0.3)
        self.wait(0.8)
        self.sub_in("却不能因此变成另一个人", 0.3)
        self.wait(0.8)
        self.wipe(0.4)
        # 裂纹 + 发光指纹
        dark = Rectangle(width=16.4, height=9.4).set_fill("#23262E", 1).set_stroke(width=0)
        self.add(dark)
        self.reg(dark)
        rng = np.random.default_rng(5)
        cracks = VGroup()
        for k in range(6):
            ang = k * TAU / 6 + rng.uniform(-0.2, 0.2)
            p = ORIGIN
            pts = [p]
            for step in range(5):
                p = p + np.array([np.cos(ang), np.sin(ang), 0]) * 1.1
                p = p + np.array([rng.uniform(-0.2, 0.2), rng.uniform(-0.2, 0.2), 0])
                pts.append(p)
            cracks.add(VMobject().set_points_as_corners(pts).set_stroke("#101216", 4))
        fp2 = fingerprint(scale=1.25, color="#F0C860").move_to([0, 0, 0])
        eyes = VGroup(Ellipse(width=1.3, height=0.5).set_fill("#F8E8B0", 1)
                      .set_stroke(width=0).move_to([-2.9, 0.3, 0]).rotate(0.25),
                      Ellipse(width=1.3, height=0.5).set_fill("#F8E8B0", 1)
                      .set_stroke(width=0).move_to([2.9, 0.3, 0]).rotate(-0.25))
        self.play(FadeIn(cracks), run_time=0.5)
        self.play(Create(fp2[1]), FadeIn(eyes), run_time=0.9)
        self.add(fp2[0])
        self.reg(cracks, fp2, eyes)
        self.sub_in("那些纯粹、不漂亮、不可约化的部分", 0.3)
        self.wait(0.9)
        self.sub_in("恰恰是你唯一的指纹", 0.3)
        self.wait(1.1)
        self.wipe(0.4)

    # ---------- S19 球体矩阵 125.5-130.8 ----------
    def s19_spheres(self):
        bg = Rectangle(width=16.4, height=9.4).set_fill("#F5EBD8", 1).set_stroke(width=0)
        self.add(bg)
        self.reg(bg)
        rng = np.random.default_rng(21)
        col_labels = ["1", "2", "2", "3", "4", "3"]
        row_labels = ["100", "100", "100", "100", "200"]
        cols = ["#C85A6A", "#4A6AB8", "#5FBFB0", "#C85A6A", "#4A6AB8", "#5FBFB0"]
        spheres = VGroup()
        for r in range(5):
            for c in range(6):
                x = -3.9 + c * 1.56
                y = 1.85 - r * 1.3
                col = cols[(r + c) % 6 if False else c % 6]
                base = Circle(radius=0.52).set_fill(col, 1).set_stroke(width=0)
                base.move_to([x, y, 0])
                shine = Circle(radius=0.15).set_fill(WHITE, 0.85).set_stroke(width=0)
                shine.move_to(base.get_center() + UP * 0.18 + LEFT * 0.18)
                sym = MathTex(r"\pi", font_size=40, color=WHITE).move_to(base.get_center() + DOWN * 0.04)
                spheres.add(VGroup(base, shine, sym))
        rl = VGroup(*[Text(t, font=SONG, font_size=30, color=INK)
                      .move_to([-5.6, 1.85 - r * 1.3, 0]) for r, t in enumerate(row_labels)])
        cl = VGroup(*[Text(t, font=SONG, font_size=30, color=INK)
                      .move_to([-3.9 + c * 1.56, 2.85, 0]) for c, t in enumerate(col_labels)])
        self.play(LaggedStart(*[FadeIn(s, scale=0.5) for s in spheres],
                              lag_ratio=0.015), FadeIn(rl), FadeIn(cl), run_time=1.2)
        self.reg(spheres, rl, cl)
        self.sub_in("不能对角化，却仍然完整", 0.3)
        self.wait(1.1)
        self.sub_in("不能简化，却足够真实", 0.3)
        self.wait(1.4)
        self.play(*[FadeOut(m) for m in self.cur], run_time=0.5)
        self.cur = []
