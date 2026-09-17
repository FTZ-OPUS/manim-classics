# -*- coding: utf-8 -*-
"""
《有理标准型》—— 仿《若尔当标准型》同风格制作
结构/节奏/配色与复刻版完全对齐（130.8s，20 段），内容替换为有理标准型：
  友矩阵 C(p)（转置约定，超对角线全 1，末行为系数）→ 特征多项式 = p(x)
  经典例子 p(x)=x²+1 → C=[[0,1],[-1,0]]（实数域不可约、无实特征值）
  有理标准型定理：任意域上任何方阵相似于友矩阵块的分块对角阵，
  不变因子整除链 d₁|d₂|⋯ 忽略次序后唯一确定。
"""
from manim import *
import numpy as np

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16.0
config.frame_height = 9.0
config.background_color = "#FBF6EF"

RED = "#E8535A"
BLUE = "#4A9DE8"
GREEN = "#2BB89A"
PURPLE = "#8B7BE8"
GOLD = "#E8A84B"
CYAN2 = "#35B8B0"
INK = "#3A3A3C"
GRIDC = "#E8E0D6"
CB = "#4A9DE8"
CFB = "#EAF3FC"
CR = "#E8535A"
CFR = "#FBE9E9"
CG = "#2BB89A"
CFG = "#E9F7F1"
CGR = "#B8AFA5"
CFGR = "#F6F1EA"
CELL = 0.92

SONG = "Songti SC"
HEI = "PingFang SC"


def cell(sym, edge, fill, sym_color=None, font_size=38):
    sq = RoundedRectangle(corner_radius=0.14, width=CELL, height=CELL)
    sq.set_stroke(edge, 2.6).set_fill(fill, 1)
    t = MathTex(sym, font_size=font_size, color=sym_color or edge)
    t.move_to(sq.get_center())
    return VGroup(sq, t)


def bracket(h, color=BLUE, sw=3.5, w=0.0):
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


def grid_matrix(entries, cell_w=CELL, gap=0.06):
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
    return Text(text, font=HEI, weight="BOLD", font_size=size,
                color=WHITE).set_stroke(BLACK, 5, background=True).move_to([0, y, 0])


def rand_card(rng, n=2, color=None, scale=1.0):
    colors = [BLUE, GREEN, RED, PURPLE, GOLD, CYAN2]
    col = color or colors[rng.integers(0, len(colors))]
    cells = VGroup()
    for i in range(n):
        for j in range(n):
            c = cell(str(rng.integers(0, 10)), col, WHITE,
                     font_size=int(30 * scale))
            c.scale(scale * 0.62)
            c.move_to(np.array([(j - (n - 1) / 2) * 0.62 * scale,
                                ((n - 1) / 2 - i) * 0.62 * scale, 0]))
            cells.add(c)
    return cells


def heart_points(n=260, seed=3):
    rng = np.random.default_rng(seed)
    dots = VGroup()
    cols = ["#F08A9B", "#E8535A", "#FBD3DC", "#F8B8C8", "#FFF0F0", "#E8A0B8"]
    for _ in range(n):
        t = rng.uniform(0, 2 * np.pi)
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
    layers = VGroup()
    for i in range(6):
        r = 0.32 + i * 0.24
        for k in range(arcs_per):
            start = np.random.default_rng(i * 10 + k).uniform(0, TAU)
            span = 1.2 + np.random.default_rng(i * 7 + k * 3).uniform(0.5, 1.8)
            a = Arc(radius=r, start_angle=start, angle=min(span, TAU - 0.2),
                    stroke_width=3.2, color=color)
            layers.add(a)
    layers.scale(scale)
    glow = layers.copy().set_stroke(width=9, opacity=0.25)
    return VGroup(glow, layers)


def simple_wolf(scale=1.0, body="#8A8A92", cap=True):
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


class RationalForm(Scene):
    def construct(self):
        rng = np.random.default_rng(42)
        self.rng = rng
        self.sub_mob = None
        self.make_bg()
        self.cur = []
        self.s0_open()
        self.s1_question()
        self.s2_algebra()
        self.s3_title()
        self.s4_condition()
        self.s5_jordan_ok()
        self.s6_fail()
        self.s7_entrance()
        self.s8_block()
        self.s9_classic()
        self.s10_parabola()
        self.s11_born()
        self.s12_theorem()
        self.s13_unique()
        self.s14_fingerprint()
        self.s15_grid_wolf()
        self.s16_heart()
        self.s17_photos()
        self.s18_wall()
        self.s19_spheres()

    # ---------- 基础设施 ----------
    def make_bg(self):
        grid = VGroup()
        for x in np.arange(-8, 8.01, 0.8):
            grid.add(Line([x, -4.6, 0], [x, 4.6, 0]).set_stroke(GRIDC, 1.2, 0.8))
        for y in np.arange(-4.4, 4.61, 0.8):
            grid.add(Line([-8, y, 0], [8, y, 0]).set_stroke(GRIDC, 1.2, 0.8))
        self.add(grid)

    def reg(self, *mobs):
        self.cur.extend([m for m in mobs if m is not None])

    def wipe(self, t_out=0.28, t_in=0.0):
        if self.cur:
            self.play(*[FadeOut(m) for m in self.cur], run_time=t_out)
        self.cur = []
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

    # ---------- S0 开场 ----------
    def s0_open(self):
        t1 = Text("矩阵分类的另一个终极答案", font=SONG, weight="BOLD", font_size=38,
                  color=RED).move_to([0, 3.1, 0])
        t2 = Text("有理标准型", font=SONG, weight="BOLD", font_size=110,
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
        self.sub_in("实数域上也能这样给矩阵分类吗？", 0.2)

    # ---------- S1 提问 ----------
    def s1_question(self):
        ring = VGroup(*[Circle(radius=1.2 + i * 1.5)
                        .set_stroke(width=0).set_fill(RED, 0.22 - i * 0.05)
                        for i in range(4)])
        ring.move_to([0, 0.3, 0])
        self.play(LaggedStart(*[ring[i].animate.scale(1).set_opacity(1)
                                for i in range(4)], lag_ratio=0.12), run_time=0.5)
        q = Text("任意方阵都有若尔当标准型？", font=SONG, weight="BOLD",
                 font_size=58, color=INK).move_to([0, 0.4, 0])
        self.play(FadeIn(q, lag_ratio=0.08), run_time=0.55)
        self.reg(ring, q)
        m = grid_matrix([[("0", BLUE, CFB), ("1", CR, CFR)],
                         [("-1", BLUE, CFB), ("0", BLUE, CFB)]], cell_w=0.8)
        m.move_to([0, -1.4, 0]).scale(0.95)
        self.play(FadeIn(m, scale=1.2), run_time=0.45)
        self.reg(m)
        self.wait(0.55)
        self.wipe(0.3)
        no = Text("复数域之外，未必！", font=SONG, weight="BOLD", font_size=88,
                  color=RED).move_to([0, -0.2, 0])
        self.play(FadeIn(no, scale=1.3), run_time=0.35)
        self.reg(no)
        self.sub_in("若尔当标准型只在复数域上成立", 0.2)
        self.wait(0.55)
        self.wipe(0.3)

    # ---------- S2 高等代数 ----------
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
        self.sub_in("还有一个完全不依赖特征值的工具", 0.3)
        self.wait(0.9)
        self.wipe(0.3)

    # ---------- S3 标题 ----------
    def s3_title(self):
        t = Text("有理标准型", font=SONG, weight="BOLD", font_size=110,
                 color="#8B8BE8").move_to([0, 1.3, 0])
        s = Text("不分解特征多项式，也能分类", font=SONG, weight="BOLD", font_size=34,
                 color=RED).move_to([0, 0.15, 0])
        self.play(FadeIn(t, lag_ratio=0.08), run_time=0.5)
        self.play(FadeIn(s), run_time=0.35)
        m = grid_matrix([[("0", CB, CFB), ("1", CR, CFR), ("0", CB, CFB)],
                         [("0", CB, CFB), ("0", CB, CFB), ("1", CR, CFR)],
                         [("-a_0", CB, CFB), ("-a_1", CB, CFB), ("-a_2", CB, CFB)]],
                        cell_w=0.95)
        m.move_to([0, -1.8, 0]).scale(0.92)
        self.play(FadeIn(m, scale=1.15), run_time=0.5)
        self.reg(t, s, m)
        self.sub_in("叫做有理标准型", 0.25)
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
        self.sub_in("它处理的正是一类特征值不在域内的矩阵", 0.25)
        self.wait(1.0)
        self.wipe(0.3)

    # ---------- S4 前提（对齐原片充要条件段） ----------
    def s4_condition(self):
        t = VGroup(Text("若尔当标准型的", font=SONG, weight="BOLD", font_size=44,
                        color=INK),
                   Text("隐含前提", font=SONG, weight="BOLD", font_size=44,
                        color=RED),
                   ).arrange(RIGHT, buff=0.12).move_to([0, 3.3, 0])
        self.play(FadeIn(t, lag_ratio=0.06), run_time=0.5)
        self.reg(t)
        g1 = Text("特征多项式完全分解", font=SONG, weight="BOLD", font_size=42,
                  color=GREEN).move_to([-3.3, 1.9, 0])
        g2 = Text("分解出的一次因式个数", font=SONG, font_size=26,
                  color=GREEN).move_to([-3.3, 1.2, 0])
        self.play(FadeIn(g1, lag_ratio=0.08), run_time=0.45)
        self.play(FadeIn(g2), run_time=0.3)
        base_y = -1.9
        base1 = Line([-4.35, base_y, 0], [-2.25, base_y, 0]).set_stroke(INK, 3)
        bar1 = Rectangle(width=0.95, height=0.001).set_fill(GREEN, 1).set_stroke(width=0)
        bar1.move_to([-3.3, base_y, 0]).align_to(base1, DOWN).shift(UP * 0.02)
        n1 = DecimalNumber(0, num_decimal_places=0, font_size=42,
                           color=GREEN).move_to([-3.3, base_y + 1.5, 0])
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
        self.sub_in("在复数域上：三次多项式总能分出三个一次因式", 0.25)
        self.wait(1.6)
        a1 = Text("多项式的次数", font=SONG, weight="BOLD", font_size=42,
                  color=BLUE).move_to([3.3, 1.9, 0])
        a2 = Text("以三次多项式为例", font=SONG, font_size=26,
                  color=BLUE).move_to([3.3, 1.2, 0])
        self.play(FadeIn(a1, lag_ratio=0.08), run_time=0.45)
        self.play(FadeIn(a2), run_time=0.3)
        base2 = Line([2.25, base_y, 0], [4.35, base_y, 0]).set_stroke(INK, 3)
        bar2 = Rectangle(width=0.95, height=0.001).set_fill(BLUE, 1).set_stroke(width=0)
        bar2.move_to([3.3, base_y, 0]).align_to(base2, DOWN).shift(UP * 0.02)
        n2 = DecimalNumber(0, num_decimal_places=0, font_size=42,
                           color=BLUE).move_to([3.3, base_y + 1.5, 0])
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
        self.wait(0.4)
        eq = MathTex("=", font_size=76, color=GREEN).move_to([0, base_y + 0.85, 0])
        self.play(FadeIn(eq, scale=1.4), run_time=0.3)
        self.reg(eq)
        self.sub_in("代数基本定理保证：永远相等", 0.25)
        fl1 = bar1.copy().set_stroke(GOLD, 4).set_fill(GOLD, 0.55)
        fl2 = bar2.copy().set_stroke(GOLD, 4).set_fill(GOLD, 0.55)
        self.play(FadeIn(fl1), FadeIn(fl2), run_time=0.35)
        self.reg(fl1, fl2)
        self.wait(2.4)
        self.wipe(0.3)

    # ---------- S5 满足前提 ----------
    def s5_jordan_ok(self):
        t = sec_title("满足前提时：若尔当标准型存在", GREEN, y=3.2)
        self.play(FadeIn(t, lag_ratio=0.08), run_time=0.45)
        ent = [[(r"\lambda_1", CB, CFB), ("O", CB, CFB), ("O", CB, CFB)],
               [("O", CB, CFB), (r"\lambda_2", CB, CFB), ("O", CB, CFB)],
               [("O", CB, CFB), ("O", CB, CFB), (r"\lambda_3", CB, CFB)]]
        m = grid_matrix(ent)
        m.move_to([0, -0.85, 0])
        self.play(FadeIn(m, scale=1.1), run_time=0.5)
        self.reg(t, m)
        self.sub_in("在复数域上，每个方阵都能化成若尔当块", 0.25)
        hi = VGroup()
        for k in range(3):
            c = m[0][k * 3 + k]
            hl = RoundedRectangle(corner_radius=0.14, width=CELL, height=CELL)
            hl.set_stroke(GREEN, 3.5).set_fill(GREEN, 0.25)
            hl.move_to(c.get_center())
            hi.add(hl)
        self.play(LaggedStart(*[FadeIn(h, scale=1.15) for h in hi], lag_ratio=0.15),
                  run_time=0.5)
        self.reg(hi)
        d = Text("分块对角的若尔当形", font=SONG, weight="BOLD", font_size=44,
                 color=GREEN).move_to([0, -3.0, 0])
        self.play(FadeIn(d), run_time=0.3)
        self.reg(d)
        self.sub_in("但它的每一块都依赖特征值 λ", 0.25)
        self.wait(1.5)
        self.wipe(0.3)

    # ---------- S6 实数域失效 ----------
    def s6_fail(self):
        t = sec_title("但特征值可能落在域外", RED, y=3.2)
        self.play(FadeIn(t, lag_ratio=0.08), run_time=0.45)
        self.reg(t)
        base_y = -1.8
        base = Line([-3.6, base_y, 0], [0.2, base_y, 0]).set_stroke(INK, 3)
        b2 = Rectangle(width=0.95, height=2 * 0.42).set_fill(BLUE, 1).set_stroke(width=0)
        b2.move_to([-2.8, base_y, 0]).align_to(base, DOWN).shift(UP * 0.02)
        b1 = Rectangle(width=0.95, height=0.001).set_fill(GREEN, 1).set_stroke(width=0)
        b1.move_to([-1.3, base_y, 0]).align_to(base, DOWN).shift(UP * 0.02)
        n2 = Text("2", font=SONG, font_size=40, color=BLUE).move_to([-2.8, base_y + 1.0, 0])
        n1 = Text("0", font=SONG, font_size=40, color=GREEN).move_to([-1.3, base_y + 0.16, 0])
        l1 = Text("实数根的个数", font=SONG, font_size=28, color=GREEN).move_to([-1.3, base_y - 0.45, 0])
        l2 = Text("多项式次数", font=SONG, font_size=28, color=BLUE).move_to([-2.8, base_y - 0.45, 0])
        neq = Text("x² + 1：0 ≠ 2", font=SONG, weight="BOLD", font_size=52,
                   color=RED).move_to([-2.0, 1.5, 0])
        self.play(FadeIn(base), FadeIn(b2), FadeIn(b1), FadeIn(n2), FadeIn(n1),
                  FadeIn(l1), FadeIn(l2), run_time=0.6)
        self.play(FadeIn(neq, scale=1.2), run_time=0.3)
        self.reg(base, b2, b1, n2, n1, l1, l2, neq)
        m = grid_matrix([[("0", CGR, CFGR), ("1", CR, CFR)],
                         [("-1", CGR, CFGR), ("0", CGR, CFGR)]], cell_w=0.95)
        m.move_to([3.3, -0.7, 0])
        self.play(FadeIn(m), run_time=0.45)
        self.reg(m)
        cross = VGroup(Line(ORIGIN, (1.8, 1.6, 0)), Line(ORIGIN, (1.8, -1.6, 0)))
        cross.set_stroke(RED, 8).move_to(m.get_center())
        self.play(Create(cross), run_time=0.4)
        f = Text("若尔当失效", font=SONG, weight="BOLD", font_size=44,
                 color=RED).move_to([3.3, -2.75, 0])
        self.play(FadeIn(f), run_time=0.3)
        self.reg(cross, f)
        self.sub_in("但一旦特征值落在了域外", 0.25)
        self.wait(0.5)
        self.sub_in("若尔当化就失败了", 0.25)
        self.wait(1.4)
        self.wipe(0.3)

    # ---------- S7 登场 ----------
    def s7_entrance(self):
        t = sec_title("有理标准型登场", PURPLE, y=3.3)
        self.play(FadeIn(t, lag_ratio=0.08), run_time=0.45)
        self.reg(t)
        ent = [[("0", CB, CFB), ("1", CR, CFR), ("0", CB, CFB)],
               [("0", CB, CFB), ("0", CB, CFB), ("1", CR, CFR)],
               [("-a_0", CB, CFB), ("-a_1", CB, CFB), ("-a_2", CB, CFB)]]
        m = grid_matrix(ent, cell_w=0.98)
        m.move_to([0, -0.8, 0]).scale(1.05)
        self.play(FadeIn(m, scale=1.15), run_time=0.5)
        self.reg(m)
        s = Text("不分解多项式，把整个 p(x) 装进矩阵", font=SONG, weight="BOLD",
                 font_size=36, color=RED).move_to([0, 2.25, 0])
        self.play(FadeIn(s, lag_ratio=0.08), run_time=0.4)
        self.reg(s)
        self.sub_in("这时有理标准型登场", 0.25)
        self.wait(0.6)
        # 金色缝合折线 (1,2)->(2,2)->(2,3)->(3,3)
        pts = [m[0][1].get_center(), m[0][4].get_center(),
               m[0][5].get_center(), m[0][8].get_center()]
        poly = VMobject().set_points_as_corners(pts).set_stroke(GOLD, 4.5)
        self.play(Create(poly), run_time=0.9)
        self.reg(poly)
        w1 = Text("把多项式缝进矩阵", font=SONG, weight="BOLD", font_size=40,
                  color=GOLD).move_to([4.0, -1.0, 0])
        self.play(FadeIn(w1), run_time=0.3)
        self.reg(w1)
        w2 = Text("一个友矩阵块", font=SONG, weight="BOLD", font_size=48,
                  color=PURPLE).move_to([4.0, -2.0, 0])
        self.play(FadeIn(w2), run_time=0.3)
        self.reg(w2)
        self.sub_in("这些 1 和系数把多项式缝成一个友矩阵块", 0.25)
        self.wait(3.1)
        self.wipe(0.3)

    # ---------- S8 友矩阵 ----------
    def s8_block(self):
        t = sec_title("友矩阵是什么？", PURPLE, y=3.3)
        self.play(FadeIn(t, lag_ratio=0.08), run_time=0.45)
        self.reg(t)
        ent = [[("0", CB, CFB), ("1", CR, CFR), ("0", CB, CFB), ("0", CB, CFB)],
               [("0", CB, CFB), ("0", CB, CFB), ("1", CR, CFR), ("0", CB, CFB)],
               [("0", CB, CFB), ("0", CB, CFB), ("0", CB, CFB), ("1", CR, CFR)],
               [("-a_0", CB, CFB), ("-a_1", CB, CFB), ("-a_2", CB, CFB), ("-a_3", CB, CFB)]]
        m = grid_matrix(ent, cell_w=0.92)
        m.move_to([-2.4, -0.8, 0]).scale(0.98)
        hl = VGroup()
        for j in range(3):
            hl.add(RoundedRectangle(corner_radius=0.14, width=CELL, height=CELL)
                   .set_stroke("#E88A4B", 3).set_fill(opacity=0)
                   .move_to(m[0][j * 4 + j + 1].get_center()))
        for j in range(4):
            hl.add(RoundedRectangle(corner_radius=0.14, width=CELL, height=CELL)
                   .set_stroke(BLUE, 3).set_fill(opacity=0)
                   .move_to(m[0][12 + j].get_center()))
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
        lab2 = Text("末行：多项式的系数", font=SONG, font_size=32,
                    color=BLUE).move_to([3.6, 1.35, 0])
        arrow2 = Arrow([0.2, -2.6, 0], [1.7, 1.1, 0], buff=0, stroke_width=5,
                       color=BLUE)
        self.play(FadeIn(lab2), GrowArrow(arrow2), run_time=0.5)
        self.reg(lab2, arrow2)
        box = RoundedRectangle(corner_radius=0.12, width=2.9, height=2.5)
        box.set_stroke(INK, 2.5).set_fill(WHITE, 0.7).move_to([3.7, -1.1, 0])
        lines = VGroup(Text("几乎为零", font=SONG, font_size=32, color=BLUE),
                       Text("+", font=SONG, font_size=32, color=INK),
                       Text("超对角线全为 1", font=SONG, font_size=32, color=RED),
                       Text("+", font=SONG, font_size=32, color=INK),
                       Text("末行装系数", font=SONG, font_size=32, color=GREEN),
                       ).arrange(DOWN, buff=0.22).move_to([3.7, -1.1, 0])
        self.play(FadeIn(box), FadeIn(lines), run_time=0.5)
        self.reg(box, lines)
        self.sub_in("一个友矩阵就是一个几乎为零", 0.25)
        self.wait(0.5)
        self.sub_in("但超对角线全是 1、末行装着系数的矩阵", 0.25)
        w = Text("友矩阵", font=SONG, weight="BOLD", font_size=52,
                 color=PURPLE).move_to([-2.4, 1.9, 0])
        self.play(FadeIn(w), run_time=0.3)
        self.reg(w)
        self.wait(1.2)
        self.wipe(0.3)

    # ---------- S9 经典例子 ----------
    def s9_classic(self):
        t = sec_title("最经典的例子", INK, y=3.3)
        self.play(FadeIn(t, lag_ratio=0.08), run_time=0.4)
        m = grid_matrix([[("0", CGR, CFGR), ("1", CR, CFR)],
                         [("-1", CGR, CFGR), ("0", CGR, CFGR)]], cell_w=1.0)
        m.move_to([0, 0.5, 0])
        self.play(FadeIn(m), run_time=0.5)
        self.reg(t, m)
        self.sub_in("取多项式 p(x) = x² + 1，它的友矩阵长这样", 0.25)
        l1 = Text("特征多项式:", font=SONG, font_size=34, color=INK).move_to([-1.6, -1.6, 0])
        self.play(FadeIn(l1), run_time=0.3)
        e1 = MathTex(r"x^2+1", font_size=60,
                     color="#6A5AE8").move_to([0.8, -1.6, 0])
        self.play(FadeIn(e1, scale=1.2), run_time=0.4)
        self.reg(l1, e1)
        self.wait(0.6)
        l2 = Text("在实数域上", font=SONG, font_size=34, color=INK).move_to([-1.9, -2.5, 0])
        l3 = Text("不可约", font=SONG, weight="BOLD", font_size=38,
                  color=RED).move_to([0.1, -2.5, 0])
        self.play(FadeIn(l2), FadeIn(l3), run_time=0.35)
        self.reg(l2, l3)
        self.sub_in("它在实数域上不可约，没有任何一次因式", 0.25)
        self.wait(1.8)
        self.wipe(0.3)

    # ---------- S10 抛物线 ----------
    def s10_parabola(self):
        t = sec_title("画出来看看", INK, y=3.3)
        e = MathTex(r"y = x^2 + 1", font_size=54,
                    color="#6A5AE8").move_to([0, 2.3, 0])
        self.play(FadeIn(t, lag_ratio=0.08), FadeIn(e, scale=1.15), run_time=0.5)
        self.reg(t, e)
        ax = VGroup(Line([-4.6, 0, 0], [4.6, 0, 0]).set_stroke(GRIDC, 2),
                    Line([0, -2.9, 0], [0, 1.9, 0]).set_stroke(GRIDC, 2))
        ax.move_to([0, -0.7, 0])
        self.play(FadeIn(ax), run_time=0.4)
        self.reg(ax)

        def pf(t):
            return np.array([t * 1.35, -0.7 + (t * t + 1) * 0.52, 0])
        curve = ParametricFunction(pf, t_range=[-1.9, 1.9], color=GREEN,
                                   stroke_width=4.5)
        self.play(Create(curve), run_time=0.9)
        self.reg(curve)
        gap = MathTex(r"\times", font_size=46, color=RED).move_to([0, -0.68, 0])
        self.play(FadeIn(gap, scale=1.5), run_time=0.3)
        self.reg(gap)
        s1 = Text("抛物线与 x 轴没有交点", font=SONG, font_size=34,
                  color=INK).move_to([0, -3.0, 0])
        self.play(FadeIn(s1), run_time=0.35)
        self.reg(s1)
        l = Text("实数根 =", font=SONG, font_size=32, color=GREEN).move_to([1.4, -2.4, 0])
        n = DecimalNumber(0, num_decimal_places=0, font_size=38,
                          color=GREEN).move_to([3.1, -2.4, 0])
        self.play(FadeIn(l), FadeIn(n), run_time=0.3)
        self.reg(l, n)
        self.sub_in("没有实数根，特征多项式却完好无损", 0.25)
        self.wait(2.2)
        self.wipe(0.3)

    # ---------- S11 天生友矩阵 ----------
    def s11_born(self):
        t = sec_title("在实数域上没有任何办法若尔当化", RED, y=3.2, font_size=40)
        self.play(FadeIn(t, lag_ratio=0.08), run_time=0.45)
        ent = [[("0", CGR, CFGR), ("1", CR, CFR)],
               [("-1", CGR, CFGR), ("0", CGR, CFGR)]]
        m = grid_matrix(ent, cell_w=1.0)
        m.move_to([0, -0.4, 0])
        self.play(FadeIn(m), run_time=0.5)
        self.reg(t, m)
        tr = Text("尝试若尔当化...（需要 ±i）", font=SONG, font_size=30,
                  color=CGR).move_to([0, -2.2, 0])
        self.play(FadeIn(tr), run_time=0.3)
        self.reg(tr)
        self.sub_in("这个矩阵在实数域上没有任何办法若尔当化", 0.25)
        c1 = m[0][1]
        self.play(c1.animate.set_stroke(BLUE, 4).set_fill(CFB, 1), run_time=0.25)
        self.play(c1.animate.set_stroke(CR, 2.6).set_fill(CFR, 1), run_time=0.25)
        w1 = Text("它天生就是", font=SONG, weight="BOLD", font_size=44,
                  color=PURPLE).move_to([-2.6, 1.6, 0])
        self.play(FadeIn(w1), run_time=0.3)
        self.reg(w1)
        w2 = Text("一个友矩阵", font=SONG, weight="BOLD", font_size=56,
                  color=PURPLE).move_to([0.7, 1.6, 0])
        hl = RoundedRectangle(corner_radius=0.14, width=CELL, height=CELL)
        hl.set_stroke(PURPLE, 3.5).set_fill(PURPLE, 0.28).move_to(m[0][0].get_center())
        hl2 = hl.copy().move_to(m[0][1].get_center())
        hl3 = hl.copy().move_to(m[0][2].get_center())
        hl4 = hl.copy().move_to(m[0][3].get_center())
        self.play(FadeIn(w2, lag_ratio=0.1), FadeIn(hl), FadeIn(hl2),
                  FadeIn(hl3), FadeIn(hl4), run_time=0.5)
        self.reg(w2, hl, hl2, hl3, hl4)
        self.sub_in("它天生就是一个友矩阵", 0.25)
        self.wait(1.2)
        self.wipe(0.3)

    # ---------- S12 定理 ----------
    def s12_theorem(self):
        t = sec_title("有理标准型定理", PURPLE, y=3.3)
        s = Text("在任意域上", font=SONG, weight="BOLD", font_size=36,
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
        self.sub_in("有理标准型定理断言：在任意域上", 0.25)
        ent2 = [[("0", "#8B7BE8", "#EFEFFB"), ("1", CR, CFR),
                 ("0", CGR, CFGR), ("0", CGR, CFGR)],
                [("0", CGR, CFGR), ("0", "#8B7BE8", "#EFEFFB"),
                 ("1", CR, CFR), ("0", CGR, CFGR)],
                [("-c_0", "#8B7BE8", "#EFEFFB"), ("-c_1", "#8B7BE8", "#EFEFFB"),
                 ("-c_2", "#8B7BE8", "#EFEFFB"), ("0", CGR, CFGR)],
                [("0", CGR, CFGR), ("0", CGR, CFGR),
                 ("0", CGR, CFGR), ("-d_0", "#8B7BE8", "#EFEFFB")]]
        m2 = grid_matrix(ent2, cell_w=0.98).move_to(m.get_center())
        self.play(ReplacementTransform(m, m2),
                  FadeOut(any_a), FadeOut(sim), FadeOut(ar), run_time=0.9)
        self.cur[self.cur.index(m)] = m2
        self.cur.remove(any_a); self.cur.remove(sim); self.cur.remove(ar)
        self.wait(0.5)
        d = VGroup(Text("由若干个友矩阵块拼成的分块对角矩阵", font=SONG,
                        weight="BOLD", font_size=32, color=INK),
                   Text("每块对应一个不变因子", font=SONG, font_size=26,
                        color=BLUE),
                   ).arrange(DOWN, buff=0.14).move_to([0, -3.55, 0])
        self.play(FadeIn(d, lag_ratio=0.06), run_time=0.4)
        self.reg(d)
        self.sub_in("任何方阵都相似于一个由友矩阵块拼成的分块对角矩阵", 0.25)
        self.wait(2.6)
        self.wipe(0.3)

    # ---------- S13 唯一性 ----------
    def s13_unique(self):
        t = sec_title("不变因子唯一确定", PURPLE, y=3.3)
        self.play(FadeIn(t, lag_ratio=0.08), run_time=0.4)
        ent = [[("0", "#8B7BE8", "#EFEFFB"), ("1", CR, CFR), ("0", CGR, CFGR)],
               [("0", CGR, CFGR), ("0", "#8B7BE8", "#EFEFFB"), ("1", CR, CFR)],
               [("-c_0", "#8B7BE8", "#EFEFFB"), ("-c_1", "#8B7BE8", "#EFEFFB"),
                ("-c_2", "#8B7BE8", "#EFEFFB")]]
        m = grid_matrix(ent)
        m.move_to([0.6, -0.7, 0])
        self.play(FadeIn(m), run_time=0.5)
        self.reg(t, m)
        lab1 = Text("次数 3", font=SONG, font_size=34, color="#8B7BE8").move_to([-2.8, 0.3, 0])
        box1 = SurroundingRectangle(m[0], buff=0.06).set_stroke("#8B7BE8", 3)
        ent1 = cell("-d_0", GREEN, CFG, font_size=36)
        ent1.move_to([3.4, -1.4, 0])
        lab2 = Text("次数 1", font=SONG, font_size=34, color=GREEN).move_to([3.4, -0.5, 0])
        self.play(FadeIn(box1), FadeIn(lab1), FadeIn(ent1), FadeIn(lab2), run_time=0.5)
        self.reg(lab1, lab2, box1, ent1)
        self.sub_in("这些块的次数，就是不变因子的次数", 0.25)
        self.wait(0.6)
        # 重排（1x1 块移到左上）
        g = ent1.copy().move_to([-2.0, 1.0, 0])
        lab1b = Text("次数 1", font=SONG, font_size=34, color=GREEN).move_to([-2.0, 0.3, 0])
        lab2b = Text("次数 3", font=SONG, font_size=34, color="#8B7BE8").move_to([3.4, 0.3, 0])
        self.play(ent1.animate.move_to(g.get_center()), FadeOut(lab1), FadeIn(lab1b),
                  ReplacementTransform(lab2, lab2b), run_time=0.7)
        self.cur[self.cur.index(lab2)] = lab2b
        ok = VGroup(Text("✓ 整除链 ", font=SONG, weight="BOLD", font_size=36,
                         color=GREEN),
                    MathTex(r"d_1 \mid d_2 \mid \cdots", font_size=40, color=GREEN),
                    Text(" 唯一确定", font=SONG, weight="BOLD", font_size=36,
                         color=GREEN),
                    ).arrange(RIGHT, buff=0.08).move_to([0, -3.0, 0])
        self.play(FadeIn(ok), run_time=0.35)
        self.reg(ok)
        self.wait(0.8)
        self.wipe(0.3)

    # ---------- S14 指纹 ----------
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
        F = MathTex(r"\mathbf{F}", font_size=80, color=RED).move_to([0, -0.4, 0])
        self.play(FadeIn(F, scale=1.4), run_time=0.4)
        self.reg(F)
        self.sub_in("这意味着有理标准型不仅是可用的", 0.25)
        self.wait(0.6)
        self.wipe(0.15)
        t2 = VGroup(Text("有理标准型不仅是", font=SONG, weight="BOLD", font_size=40,
                         color=INK),
                    Text("可用的", font=SONG, weight="BOLD", font_size=40, color=BLUE),
                    Text("，而且是", font=SONG, weight="BOLD", font_size=40, color=INK),
                    Text("唯一的", font=SONG, weight="BOLD", font_size=40, color=RED),
                    ).arrange(RIGHT, buff=0.08).move_to([0, 1.1, 0])
        self.play(FadeIn(t2), run_time=0.4)
        self.reg(t2)
        t3 = VGroup(Text("它是矩阵在", font=SONG, font_size=36, color=INK),
                    Text("任意域上", font=SONG, weight="BOLD", font_size=36, color=BLUE),
                    Text("的", font=SONG, font_size=36, color=INK),
                    Text("精确指纹", font=SONG, weight="BOLD", font_size=36, color=RED),
                    ).arrange(RIGHT, buff=0.08).move_to([0, 0.15, 0])
        self.play(FadeIn(t3), run_time=0.4)
        self.reg(t3)
        rip2 = fingerprint(scale=0.9, color="#7A6AE0").move_to([0, -1.9, 0])
        self.play(Create(rip2[1]), run_time=0.9)
        self.add(rip2[0])
        self.reg(rip2)
        self.sub_in("它是矩阵在任意域上的精确指纹", 0.25)
        self.wait(1.9)
        self.wipe(0.35)

    # ---------- S15 网格狼 ----------
    def s15_grid_wolf(self):
        bg = Rectangle(width=16.4, height=9.4).set_fill("#F2E3C0", 1).set_stroke(width=0)
        self.add(bg)
        self.reg(bg)
        vp = [0, -1.1, 0]
        glow = VGroup()
        for k in range(-7, 8):
            glow.add(glow_line(vp, [k * 1.35, 4.2, 0], "#5FD8C8", 2.2))
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
        for txt in ("我的意思是", "不是所有矩阵都能遇见自己的特征值",
                    "正如不是所有方程都有实数解"):
            s = self.sub_in(txt, 0.3)
            self.wait(1.35)
            self.play(FadeOut(s), run_time=0.2)
            self.cur.remove(s)
        self.wipe(0.4)

    # ---------- S16 心形 Q ----------
    def s16_heart(self):
        bg = Rectangle(width=16.4, height=9.4).set_fill("#1A1216", 1).set_stroke(width=0)
        self.add(bg)
        self.reg(bg)
        dots = heart_points()
        q = Text("Q", font=SONG, weight="BOLD", font_size=150,
                 color="#E8535A").move_to([0, 0.25, 0])
        q.set_stroke("#FFD3DC", 1.5, background=True)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots[::3]],
                              lag_ratio=0.008), run_time=1.2)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots[1::3]],
                              lag_ratio=0.008), run_time=0.5)
        self.play(FadeIn(q, scale=1.6), run_time=0.5)
        self.reg(dots, q)
        self.sub_in("有些根，躲在复数的世界里", 0.3)
        self.wait(1.1)
        self.sub_in("实数轴上，找不到它们的出口", 0.3)
        self.wait(1.0)
        self.wipe(0.4)

    # ---------- S17 撕纸拼贴 ----------
    def s17_photos(self):
        bg = Rectangle(width=16.4, height=9.4).set_fill("#2E2418", 1).set_stroke(width=0)
        self.add(bg)
        self.reg(bg)
        rng = np.random.default_rng(11)
        nums_bg = VGroup()
        for _ in range(90):
            d = Text(str(rng.integers(0, 2)), font=SONG, font_size=40,
                     color="#C8A860").move_to([rng.uniform(-7.6, 7.6),
                                               rng.uniform(-4.2, 4.2), 0])
            d.set_opacity(rng.uniform(0.25, 0.6))
            nums_bg.add(d)
        self.play(FadeIn(nums_bg), run_time=0.6)
        self.reg(nums_bg)
        photos = VGroup()
        labels = [("0", -1.15, 1.15), ("1", 1.15, 1.15),
                  ("-1", -1.15, -1.15), ("0", 1.15, -1.15)]
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
        self.sub_in("那颗每转 90° 就翻面的心，就是 0 1 / -1 0", 0.3)
        self.wait(1.3)
        self.sub_in("不用分解，也能相认", 0.3)
        self.wait(0.8)
        self.sub_in("把同一个多项式，缝成友矩阵", 0.3)
        self.wait(1.4)
        self.wipe(0.4)

    # ---------- S18 石墙指纹 ----------
    def s18_wall(self):
        bg = Rectangle(width=16.4, height=9.4).set_fill("#5A5A60", 1).set_stroke(width=0)
        self.add(bg)
        self.reg(bg)
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
        self.sub_in("那些不依赖特征值的部分", 0.3)
        self.wait(0.9)
        self.sub_in("恰恰是你唯一的指纹", 0.3)
        self.wait(1.1)
        self.wipe(0.4)

    # ---------- S19 球体矩阵 ----------
    def s19_spheres(self):
        bg = Rectangle(width=16.4, height=9.4).set_fill("#F5EBD8", 1).set_stroke(width=0)
        self.add(bg)
        self.reg(bg)
        col_labels = ["d\u2081", "d\u2082", "d\u2083", "d\u2084", "d\u2085", "d\u2086"]
        row_labels = ["3", "2", "1", "1", "1"]
        cols = ["#C85A6A", "#4A6AB8", "#5FBFB0", "#C85A6A", "#4A6AB8", "#5FBFB0"]
        spheres = VGroup()
        for r in range(5):
            for c in range(6):
                x = -3.9 + c * 1.56
                y = 1.85 - r * 1.3
                col = cols[c % 6]
                base = Circle(radius=0.52).set_fill(col, 1).set_stroke(width=0)
                base.move_to([x, y, 0])
                shine = Circle(radius=0.15).set_fill(WHITE, 0.85).set_stroke(width=0)
                shine.move_to(base.get_center() + UP * 0.18 + LEFT * 0.18)
                sym = MathTex(r"\lambda", font_size=38, color=WHITE)
                sym.move_to(base.get_center() + DOWN * 0.04)
                spheres.add(VGroup(base, shine, sym))
        rl = VGroup(*[Text(t, font=SONG, font_size=30, color=INK)
                      .move_to([-5.6, 1.85 - r * 1.3, 0]) for r, t in enumerate(row_labels)])
        cl = VGroup(*[Text(t, font=SONG, font_size=30, color=INK)
                      .move_to([-3.9 + c * 1.56, 2.85, 0]) for c, t in enumerate(col_labels)])
        self.play(LaggedStart(*[FadeIn(s, scale=0.5) for s in spheres],
                              lag_ratio=0.015), FadeIn(rl), FadeIn(cl), run_time=1.2)
        self.reg(spheres, rl, cl)
        self.sub_in("不能若尔当化，却仍然完整", 0.3)
        self.wait(1.1)
        self.sub_in("不需要特征值，却足够真实", 0.3)
        self.wait(1.4)
        self.play(*[FadeOut(m) for m in self.cur], run_time=0.5)
        self.cur = []
