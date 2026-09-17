# -*- coding: utf-8 -*-
"""
《埃尔伯格悖论（模糊厌恶）》复刻版 —— 逐帧逆向还原
原片 ~131.5s，米白底 + 宋体标题 + 章节标记（01/06）+ 简笔火柴人/罐子/印章 + 白场转场
结构：悖论提问 → 期望值陷阱 → 两罐实验 → 两问投票 → 逻辑矛盾 → 模糊厌恶
     → 两家店类比 → 情感隐喻（已知拒绝 / 未知回应 / 抱紧确定罐 / 遗憾与圆满）
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
INK = "#3A3A3C"
GRAY = "#B8AFA5"
DARK = "#3A3A3C"
PINK = "#F08A9B"
SONG = "Songti SC"
CFB = "#EAF3FC"
CFR = "#FBE9E9"
CFG = "#E9F7F1"
HEI = "PingFang SC"


# ---------------- 组件库 ----------------
def chapter(n, total):
    """左上角章节标记 01 / 06"""
    return Text(f"{n:02d} / {total:02d}", font=HEI, font_size=26,
                color="#B0A89E").move_to([-7.0, 3.9, 0])


def sec_title(text, color=INK, font_size=46, y=3.15):
    return Text(text, font=SONG, weight="BOLD", font_size=font_size,
                color=color).move_to([0, y, 0])


def subtitle(text, y=-3.62, size=27):
    return Text(text, font=HEI, weight="BOLD", font_size=size,
                color=WHITE).set_stroke(BLACK, 5, background=True).move_to([0, y, 0])


def stamp(text, color=RED, size=56, rot=-0.06, pad=0.28):
    """红框印章"""
    t = Text(text, font=SONG, weight="BOLD", font_size=size, color=color)
    box = RoundedRectangle(corner_radius=0.12,
                           width=t.width + pad * 2, height=t.height + pad * 1.1)
    box.set_stroke(color, 4.5).set_fill(WHITE, 0.85)
    g = VGroup(box, t).rotate(rot)
    return g


def jar(scale=1.0, lid=True):
    """简笔罐子：圆角方形容器 + 盖子"""
    body = RoundedRectangle(corner_radius=0.38 * scale,
                            width=2.35 * scale, height=2.7 * scale)
    body.set_stroke(INK, 3.2).set_fill(WHITE, 0.95)
    g = VGroup(body)
    if lid:
        ld = RoundedRectangle(corner_radius=0.08 * scale,
                              width=1.05 * scale, height=0.26 * scale)
        ld.set_stroke(INK, 3.2).set_fill(WHITE, 1)
        ld.move_to(body.get_top() + UP * 0.13 * scale)
        g.add(ld)
    return g


def dot_grid(rows, cols, color_fn, region_w=1.95, region_h=2.1, r=0.062):
    """罐内点阵：color_fn(i, j) -> 颜色"""
    dots = VGroup()
    dx = region_w / max(cols - 1, 1)
    dy = region_h / max(rows - 1, 1)
    for i in range(rows):
        for j in range(cols):
            d = Dot(radius=r, color=color_fn(i, j))
            d.move_to([(j - (cols - 1) / 2) * dx, ((rows - 1) / 2 - i) * dy, 0])
            dots.add(d)
    return dots


def gray_grid(jar_g, seed=1, red_ratio=0.0, red_color=RED, dark_ratio=0.0):
    """在罐子里填 10×10 点阵；red_ratio/dark_ratio 控制红/黑比例，其余灰"""
    rng = np.random.default_rng(seed)
    body = jar_g[0]

    def cf(i, j):
        u = rng.uniform()
        if u < red_ratio:
            return red_color
        if u < red_ratio + dark_ratio:
            return DARK
        return GRAY
    g = dot_grid(10, 10, cf)
    g.move_to(body.get_center() + DOWN * 0.12 * (body.height / 2.7))
    return g


def stickman(scale=1.0, pose="stand", color=INK):
    """简笔火柴人 pose: stand / open / hug / raised"""
    s = scale
    g = VGroup()
    head = Circle(radius=0.20 * s).set_stroke(color, 3.5).set_fill(WHITE, 1)
    body = Line([0, -0.20 * s, 0], [0, -0.85 * s, 0]).set_stroke(color, 3.5)
    g.add(head, body)
    if pose == "stand":
        g.add(Line([-0.05 * s, -0.42 * s, 0], [-0.34 * s, -0.62 * s, 0]).set_stroke(color, 3.2))
        g.add(Line([0.05 * s, -0.42 * s, 0], [0.34 * s, -0.62 * s, 0]).set_stroke(color, 3.2))
    elif pose == "open":
        g.add(Line([0, -0.55 * s, 0], [-0.45 * s, -0.10 * s, 0]).set_stroke(color, 3.2))
        g.add(Line([0, -0.55 * s, 0], [0.45 * s, -0.10 * s, 0]).set_stroke(color, 3.2))
    elif pose == "hug":
        a1 = Arc(radius=0.30 * s, start_angle=PI * 0.15, angle=PI * 0.7,
                 arc_center=[0, -0.45 * s, 0]).set_stroke(color, 3.2)
        g.add(a1)
    elif pose == "raised":
        g.add(Line([0, -0.42 * s, 0], [-0.30 * s, -0.05 * s, 0]).set_stroke(color, 3.2))
        g.add(Line([0, -0.42 * s, 0], [0.30 * s, -0.05 * s, 0]).set_stroke(color, 3.2))
    g.add(Line([0, -0.85 * s, 0], [-0.26 * s, -1.45 * s, 0]).set_stroke(color, 3.5))
    g.add(Line([0, -0.85 * s, 0], [0.26 * s, -1.45 * s, 0]).set_stroke(color, 3.5))
    return g


def bead_ring(radius=1.55, n=26, color="#C9C4EE", r=0.115):
    """珠链圆环"""
    dots = VGroup()
    for i in range(n):
        a = i * TAU / n
        d = Dot(radius=r, color=color)
        d.move_to([radius * np.cos(a), radius * np.sin(a), 0])
        dots.add(d)
    return dots


def blob(n=16, color="#8B7BE8", seed=7, spread=1.1):
    """模糊圆团"""
    rng = np.random.default_rng(seed)
    g = VGroup()
    for _ in range(n):
        c = Circle(radius=rng.uniform(0.25, 0.62)).set_stroke(width=0)
        c.set_fill(color, rng.uniform(0.10, 0.26))
        c.move_to([rng.uniform(-spread, spread), rng.uniform(-0.7, 0.7), 0])
        g.add(c)
    return g


def seg_bar(segs, w=4.6, h=0.55, y=0.0, x=0.0, gap=0.0):
    """分段进度条 segs: [(color, frac)]"""
    total = sum(f for _, f in segs)
    g = VGroup()
    cx = x - w / 2
    for col, f in segs:
        r = Rectangle(width=w * f / total - gap, height=h)
        r.set_fill(col, 1).set_stroke(width=0)
        r.move_to([cx + w * f / total / 2, y, 0])
        cx += w * f / total
        g.add(r)
    return g


def grad_bar(w=7.2, h=0.6, c1=RED, c2="#2E2E30", n=28):
    """红→黑渐变条（近似）"""
    g = VGroup()
    for i in range(n):
        col = interpolate_color(ManimColor(c1), ManimColor(c2), i / (n - 1))
        r = Rectangle(width=w / n + 0.005, height=h).set_fill(col, 1).set_stroke(width=0)
        r.move_to([-w / 2 + w / n * (i + 0.5), 0, 0])
        g.add(r)
    return g


def shop(scale=1.0, awning=BLUE):
    """简笔小店：遮阳棚 + 橱窗"""
    g = VGroup()
    body = RoundedRectangle(corner_radius=0.1, width=2.5 * scale, height=1.7 * scale)
    body.set_stroke(INK, 3).set_fill(WHITE, 1)
    win = RoundedRectangle(corner_radius=0.08, width=1.6 * scale, height=0.95 * scale)
    win.set_stroke(awning, 3).set_fill(awning, 0.18)
    win.move_to(body.get_center() + UP * 0.12 * scale)
    base = Rectangle(width=2.1 * scale, height=0.22 * scale)
    base.set_stroke(GRAY, 2).set_fill("#F1EAE0", 1)
    base.move_to(body.get_bottom() + DOWN * 0.25 * scale)
    g.add(body, win, base)
    # 遮阳棚条纹
    aw = VGroup()
    seg = 0.3125 * scale
    for i in range(8):
        c = awning if i % 2 == 0 else WHITE
        s = Rectangle(width=seg, height=0.34 * scale).set_fill(c, 1).set_stroke(width=0)
        s.move_to([-3.5 * seg / 2 * 1.0 + seg * (i + 0.5) * 0.995, 0, 0])
        aw.add(s)
    aw.move_to(body.get_top() + UP * 0.17 * scale)
    g.add(aw)
    return g


class EllsbergRemake(Scene):
    def construct(self):
        rng = np.random.default_rng(9)
        self.rng = rng
        self.sub_mob = None
        self.make_bg()
        self.cur = []
        self.s0_open()        # 0-1.2
        self.s1_ring()        # 1.2-5.2
        self.s2_wrong()       # 5.2-6.2
        self.s3_expect()      # 6.2-11.8
        self.s4_core()        # 11.8-14.8
        self.s5_two_jars()    # 14.8-18.8
        self.s6_jar1()        # 18.8-22.8
        self.s7_jar2()        # 22.8-30.8
        self.s8_draw()        # 30.8-35.5
        self.s9_q1()          # 35.5-41.8
        self.s10_q2()         # 41.8-49.5
        self.s11_problem()    # 49.5-50.8
        self.s12_red()        # 50.8-57
        self.s13_black()      # 57-64.5
        self.s14_100()        # 64.5-70
        self.s15_conflict()   # 70-75
        self.s16_utility()    # 75-82.5
        self.s17_shops()      # 82.5-94.5
        self.s18_avoid()      # 94.5-98.5
        self.s19_dark()       # 98.5-99.5
        self.s20_love()       # 99.5-110.5
        self.s21_refuse()     # 110.5-113.5
        self.s22_unknown()    # 113.5-120.5
        self.s23_hug()        # 120.5-126.5
        self.s24_ending()     # 126.5-131.5

    # ---------- 基础设施 ----------
    def make_bg(self):
        grid = VGroup()
        for x in np.arange(-8, 8.01, 1.05):
            grid.add(Line([x, -4.6, 0], [x, 4.6, 0]).set_stroke("#EFE8DE", 1.0, 0.55))
        for y in np.arange(-4.4, 4.61, 1.05):
            grid.add(Line([-8, y, 0], [8, y, 0]).set_stroke("#EFE8DE", 1.0, 0.55))
        self.add(grid)

    def reg(self, *mobs):
        self.cur.extend([m for m in mobs if m is not None])

    def wipe(self, t_out=0.28):
        if self.cur:
            self.play(*[FadeOut(m) for m in self.cur], run_time=t_out)
        self.cur = []

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

    def chapter_in(self, n, total):
        c = chapter(n, total)
        self.play(FadeIn(c), run_time=0.2)
        self.reg(c)
        return c

    # ---------- S0 开场 0-1.2 ----------
    def s0_open(self):
        top = Text("—— 模糊厌恶 ——", font=SONG, weight="BOLD", font_size=40,
                   color=RED).move_to([0, 3.4, 0])
        t = Text("埃尔斯伯格悖论", font=SONG, weight="BOLD", font_size=92,
                 color=INK).move_to([0, 2.1, 0])
        self.play(FadeIn(top), run_time=0.2)
        self.play(FadeIn(t, lag_ratio=0.08), run_time=0.35)
        j1 = jar(0.72).move_to([-4.4, -1.0, 0])
        j2 = jar(0.72).move_to([4.4, -1.0, 0])
        g1 = gray_grid(j1, seed=2, red_ratio=0.10).scale(0.72).move_to(j1[0].get_center() + DOWN * 0.09)
        g2 = gray_grid(j2, seed=3).scale(0.72).move_to(j2[0].get_center() + DOWN * 0.09)
        l1 = Text("已知概率", font=SONG, weight="BOLD", font_size=32,
                  color=BLUE).move_to([-4.4, -2.55, 0])
        l2 = Text("未知概率", font=SONG, weight="BOLD", font_size=32,
                  color=RED).move_to([4.4, -2.55, 0])
        m1 = stickman(0.9).move_to([-1.6, -1.35, 0])
        m2 = stickman(0.9).move_to([1.6, -1.35, 0])
        heart = ParametricFunction(
            lambda t: np.array([16 * np.sin(t) ** 3 * 0.075,
                                (13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t)
                                 - np.cos(4 * t)) * 0.075 - 1.05, 0]),
            t_range=[0, TAU], color=RED, fill_opacity=1, stroke_width=0).scale(0.9)
        heart.set_fill(RED, 1).set_stroke(width=0)
        self.play(FadeIn(j1), FadeIn(j2), FadeIn(g1), FadeIn(g2),
                  FadeIn(l1), FadeIn(l2), FadeIn(m1), FadeIn(m2),
                  FadeIn(heart, scale=0.6), run_time=0.45)
        self.reg(top, t, j1, j2, g1, g2, l1, l2, m1, m2, heart)
        self.sub_in("从数学，到爱情", 0.2)

    # ---------- S1 圆环 0/1 1.2-5.2 ----------
    def s1_ring(self):
        self.wipe(0.25)
        ring_d = DashedVMobject(Circle(radius=2.75).set_stroke(PURPLE, 3), num_dashes=40)
        ring_s = Circle(radius=2.45).set_stroke(BLUE, 3.5)
        cards = VGroup()
        for i in range(16):
            a = i * TAU / 16 + TAU / 32
            sym = "0" if i % 2 == 0 else "1"
            col = BLUE if i % 2 == 0 else RED
            f = CFB if i % 2 == 0 else CFR
            c = RoundedRectangle(corner_radius=0.1, width=0.5, height=0.5)
            c.set_stroke(col, 2.5).set_fill(f, 1)
            tx = MathTex(sym, font_size=34, color=col).move_to(c.get_center())
            c.add(tx)
            c.move_to([2.6 * np.cos(a), 2.6 * np.sin(a) + 0.15, 0])
            cards.add(c)
        self.play(Create(ring_d), Create(ring_s),
                  LaggedStart(*[FadeIn(c, scale=0.6) for c in cards], lag_ratio=0.04),
                  run_time=0.8)
        self.reg(ring_d, ring_s, cards)
        pct = DecimalNumber(29, unit="%", num_decimal_places=0, font_size=96,
                            color="#8A8A8E").move_to([0, 0.15, 0])
        self.play(FadeIn(pct), run_time=0.35)
        self.play(ChangeDecimalToValue(pct, 50), pct.animate.set_color(RED), run_time=0.8)
        arc = Arc(radius=2.0, start_angle=-PI * 0.15, angle=PI * 0.7,
                  stroke_width=6, color=RED)
        self.play(Create(arc), run_time=0.6)
        self.reg(pct, arc)
        self.sub_in("面对未知概率", 0.2)
        self.wait(0.5)
        self.sub_in("我们都会像算机器一样绝对理性", 0.2)
        q = MathTex("?", font_size=110, color=PURPLE).move_to([0, 1.7, 0])
        self.play(FadeIn(q, scale=1.4), run_time=0.35)
        self.reg(q)
        self.wait(0.4)

    # ---------- S2 当然不对 5.2-6.2 ----------
    def s2_wrong(self):
        self.wipe(0.25)
        self.chapter_in(1, 6)
        t = Text("当然不对了。", font=SONG, weight="BOLD", font_size=110,
                 color=PINK).move_to([0, 0.2, 0])
        self.play(FadeIn(t, lag_ratio=0.1), run_time=0.4)
        self.reg(t)
        self.sub_in("当然不对了", 0.2)
        self.wait(0.35)

    # ---------- S3 只算期望值 6.2-11.8 ----------
    def s3_expect(self):
        self.wipe(0.25)
        self.chapter_in(1, 6)
        t = Text("只算期望值", font=SONG, weight="BOLD", font_size=48,
                 color=BLUE).move_to([-3.4, 2.2, 0])
        box = RoundedRectangle(corner_radius=0.15, width=4.3, height=2.3)
        box.set_stroke(BLUE, 3).set_fill("#EAF3FC", 0.9).move_to([-3.4, -0.2, 0])
        e1 = MathTex(r"50\% \times 100 \, =", font_size=44, color=INK).move_to([-3.4, 0.35, 0])
        n = DecimalNumber(0, num_decimal_places=0, font_size=72,
                          color=BLUE).move_to([-3.4, -0.85, 0])
        self.play(FadeIn(t, lag_ratio=0.08), run_time=0.4)
        self.play(FadeIn(box), FadeIn(e1), run_time=0.4)
        self.play(FadeIn(n), run_time=0.2)
        self.play(ChangeDecimalToValue(n, 38), run_time=0.4)
        self.play(ChangeDecimalToValue(n, 50), run_time=0.4)
        self.reg(t, box, e1, n)
        self.sub_in("我们面对未知概率时", 0.2)
        self.wait(0.4)
        pz = Text("比例未知", font=SONG, weight="BOLD", font_size=44,
                  color=PURPLE).move_to([4.0, 1.9, 0])
        bl = blob(seed=7).move_to([4.0, 0.0, 0])
        self.play(FadeIn(pz, lag_ratio=0.08), run_time=0.35)
        self.play(FadeIn(bl), run_time=0.5)
        self.reg(pz, bl)
        st = stamp("厌恶", color=RED, size=60).move_to([4.0, 0.0, 0]).rotate(-0.1)
        self.play(FadeIn(st, scale=1.6), run_time=0.3)
        self.reg(st)
        self.sub_in("并不是只算期望值", 0.2)
        self.wait(0.4)
        self.sub_in("还会厌恶模糊本身", 0.2)
        self.wait(0.7)

    # ---------- S4 核心 11.8-14.8 ----------
    def s4_core(self):
        self.wipe(0.25)
        self.chapter_in(2, 6)
        t = Text("埃尔伯格悖论 · 核心", font=SONG, weight="BOLD", font_size=54,
                 color=INK).move_to([0, 2.4, 0])
        self.play(FadeIn(t, lag_ratio=0.08), run_time=0.45)
        self.reg(t)
        ring = bead_ring(radius=1.9, n=24)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in ring], lag_ratio=0.05),
                  run_time=0.7)
        self.reg(ring)
        st = stamp("模糊厌恶", color=RED, size=76).move_to([0, -0.2, 0]).rotate(-0.05)
        self.play(FadeIn(st, scale=1.5), run_time=0.35)
        self.reg(st)
        self.sub_in("埃尔伯格悖论的核心是模糊厌恶", 0.2)
        self.wait(1.2)

    # ---------- S5 两个罐子 14.8-18.8 ----------
    def s5_two_jars(self):
        self.wipe(0.25)
        self.chapter_in(3, 6)
        t1 = Text("第一个罐子", font=SONG, weight="BOLD", font_size=42,
                  color=BLUE).move_to([-3.6, 2.5, 0])
        t2 = Text("第二个罐子", font=SONG, weight="BOLD", font_size=42,
                  color=RED).move_to([3.6, 2.5, 0])
        j1 = jar(0.95).move_to([-3.6, -0.6, 0])
        j2 = jar(0.95).move_to([3.6, -0.6, 0])
        self.play(FadeIn(t1, lag_ratio=0.08), FadeIn(t2, lag_ratio=0.08),
                  FadeIn(j1), FadeIn(j2), run_time=0.5)
        self.reg(t1, t2, j1, j2)
        self.sub_in("实验很简单：两个罐子，各装100个球", 0.2)
        g1 = gray_grid(j1, seed=11).scale(0.95).move_to(j1[0].get_center() + DOWN * 0.12)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in g1[::2]], lag_ratio=0.01),
                  run_time=0.6)
        self.reg(g1)
        g2 = gray_grid(j2, seed=12).scale(0.95).move_to(j2[0].get_center() + DOWN * 0.12)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in g2[::2]], lag_ratio=0.01),
                  run_time=0.6)
        self.reg(g2)
        n1 = DecimalNumber(0, num_decimal_places=0, font_size=52,
                           color=BLUE).move_to([-3.6, -2.75, 0])
        n2 = DecimalNumber(0, num_decimal_places=0, font_size=52,
                           color=RED).move_to([3.6, -2.75, 0])
        self.play(FadeIn(n1), FadeIn(n2), run_time=0.2)
        self.play(ChangeDecimalToValue(n1, 100), ChangeDecimalToValue(n2, 100),
                  run_time=0.8)
        self.reg(n1, n2)
        self.wait(1.5)

    # ---------- S6 第一个罐子 18.8-22.8 ----------
    def s6_jar1(self):
        self.wipe(0.25)
        self.chapter_in(4, 6)
        t = Text("第一个罐子", font=SONG, weight="BOLD", font_size=44,
                 color=BLUE).move_to([-3.7, 2.7, 0])
        j = jar(1.0).move_to([-3.7, -0.4, 0])
        g = dot_grid(10, 10,
                     lambda i, jj: RED if (i * 10 + jj) % 2 == 0 else DARK)
        g.move_to(j[0].get_center() + DOWN * 0.12).scale(0.98)
        self.play(FadeIn(t, lag_ratio=0.08), FadeIn(j), run_time=0.4)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in g], lag_ratio=0.008),
                  run_time=0.7)
        self.reg(t, j, g)
        l = Text("已知概率", font=SONG, weight="BOLD", font_size=40,
                 color=BLUE).move_to([3.6, 1.9, 0])
        bar = seg_bar([(RED, 0.5), (DARK, 0.5)], w=4.4, h=0.6, y=0.6, x=3.6)
        lab = VGroup(Text("红 50%", font=SONG, font_size=26, color=RED).move_to([2.7, -0.05, 0]),
                     Text("黑 50%", font=SONG, font_size=26, color=DARK).move_to([4.5, -0.05, 0]))
        self.play(FadeIn(l, lag_ratio=0.08), run_time=0.35)
        self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in bar], lag_ratio=0.15),
                  run_time=0.5)
        self.play(FadeIn(lab), run_time=0.25)
        self.reg(l, bar, lab)
        self.sub_in("第一个罐子明确有50个红球", 0.2)
        self.wait(0.5)
        self.sub_in("50个黑球", 0.2)
        self.wait(0.8)

    # ---------- S7 第二个罐子 22.8-30.8 ----------
    def s7_jar2(self):
        self.wipe(0.25)
        self.chapter_in(5, 6)
        t = Text("第二个罐子", font=SONG, weight="BOLD", font_size=44,
                 color=RED).move_to([3.7, 2.7, 0])
        j = jar(1.0).move_to([3.7, -0.4, 0])
        rng = np.random.default_rng(23)
        g = dot_grid(10, 10, lambda i, jj: RED if rng.uniform() < 0.55 else DARK)
        g.move_to(j[0].get_center() + DOWN * 0.12).scale(0.98)
        self.play(FadeIn(t, lag_ratio=0.08), FadeIn(j), run_time=0.4)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in g], lag_ratio=0.008),
                  run_time=0.7)
        self.reg(t, j, g)
        self.sub_in("第二个罐子也有100个球", 0.2)
        self.wait(0.5)
        self.sub_in("但红球和黑球的比例完全未知", 0.2)
        l = Text("未知概率", font=SONG, weight="BOLD", font_size=40,
                 color=RED).move_to([-3.7, 1.9, 0])
        bar = seg_bar([(RED, 0.42), ("#E8DCD2", 0.58)], w=4.4, h=0.6, y=0.6, x=-3.7)
        q = MathTex("?", font_size=76, color=RED).move_to([-1.25, 0.6, 0])
        self.play(FadeIn(l, lag_ratio=0.08), run_time=0.35)
        self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in bar], lag_ratio=0.15),
                  run_time=0.5)
        self.play(FadeIn(q, scale=1.4), run_time=0.25)
        self.reg(l, bar, q)
        p1 = Text("比例完全未知", font=SONG, weight="BOLD", font_size=34,
                  color=RED).move_to([-3.7, -0.35, 0])
        ax = DoubleArrow([-5.6, -1.35, 0], [-1.8, -1.35, 0], buff=0,
                         stroke_width=5, color=RED)
        l0 = Text("0%", font=SONG, font_size=26, color=RED).move_to([-5.95, -1.35, 0])
        l1 = Text("100%", font=SONG, font_size=26, color=RED).move_to([-1.45, -1.35, 0])
        self.play(FadeIn(p1), run_time=0.3)
        self.play(GrowArrow(ax), FadeIn(l0), FadeIn(l1), run_time=0.5)
        self.reg(p1, ax, l0, l1)
        self.sub_in("可能全是红球，也可能全是黑球", 0.2)
        self.wait(1.4)

    # ---------- S8 摸球 30.8-35.5 ----------
    def s8_draw(self):
        self.wipe(0.25)
        self.chapter_in(6, 6)
        j = jar(1.0).move_to([-3.7, -0.4, 0])
        g = dot_grid(10, 10,
                     lambda i, jj: RED if (i * 10 + jj) % 2 == 0 else DARK)
        g.move_to(j[0].get_center() + DOWN * 0.12)
        self.play(FadeIn(j), run_time=0.4)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in g[::2]], lag_ratio=0.01),
                  run_time=0.6)
        self.reg(j, g)
        ball = Dot(radius=0.14, color=RED).move_to(j[0].get_center() + UP * 0.2)
        self.play(ball.animate.move_to([-1.7, 0.4, 0]), run_time=0.45,
                  rate_func=rush_from)
        self.reg(ball)
        box = RoundedRectangle(corner_radius=0.15, width=3.3, height=1.9)
        box.set_stroke(BLUE, 3).set_fill("#EAF3FC", 0.9).move_to([3.3, 0.3, 0])
        self.play(FadeIn(box), run_time=0.35)
        t1 = Text("猜中颜色", font=SONG, weight="BOLD", font_size=38,
                  color=INK).move_to([3.3, 0.75, 0])
        n = DecimalNumber(0, num_decimal_places=0, font_size=64,
                          color=BLUE).move_to([3.3, -0.15, 0])
        yuan = Text("元", font=SONG, font_size=38, color=BLUE).move_to([4.35, -0.15, 0])
        self.play(FadeIn(t1), run_time=0.25)
        self.play(FadeIn(n), FadeIn(yuan), run_time=0.2)
        self.play(ChangeDecimalToValue(n, 100), run_time=0.6)
        self.reg(box, t1, n, yuan)
        self.sub_in("你从罐中随机摸一个球", 0.2)
        self.wait(0.4)
        self.sub_in("猜中颜色就赢100元", 0.2)
        self.wait(1.4)

    # ---------- S9 第一问 35.5-41.8 ----------
    def s9_q1(self):
        self.wipe(0.25)
        self.chapter_in(1, 8)
        t = Text("第一问：赌哪个罐子出红球？", font=SONG, weight="BOLD", font_size=46,
                 color=INK).move_to([0, 3.15, 0])
        self.play(FadeIn(t, lag_ratio=0.08), run_time=0.45)
        self.reg(t)
        t1 = Text("第一个罐子", font=SONG, weight="BOLD", font_size=36,
                  color=BLUE).move_to([-3.6, 2.15, 0])
        t2 = Text("第二个罐子", font=SONG, weight="BOLD", font_size=36,
                  color=RED).move_to([3.6, 2.15, 0])
        j1 = jar(0.92).move_to([-3.6, -0.5, 0])
        j2 = jar(0.92).move_to([3.6, -0.5, 0])
        g1 = dot_grid(10, 10, lambda i, jj: RED if (i * 10 + jj) % 2 == 0 else DARK)
        g1.move_to(j1[0].get_center() + DOWN * 0.12).scale(0.96)
        g2 = gray_grid(j2, seed=31).scale(0.96).move_to(j2[0].get_center() + DOWN * 0.12)
        self.play(FadeIn(t1), FadeIn(t2), FadeIn(j1), FadeIn(j2), run_time=0.45)
        self.play(FadeIn(g1), run_time=0.5)
        self.reg(t1, t2, j1, j2, g1)
        self.sub_in("先问：赌第一个罐子出红球", 0.2)
        g2b = gray_grid(j2, seed=32).scale(0.96).move_to(j2[0].get_center() + DOWN * 0.12)
        self.play(FadeIn(g2b), run_time=0.5)
        self.reg(g2b)
        self.sub_in("还是赌第二个罐子出红球？", 0.2)
        ball = Dot(radius=0.16, color=RED).move_to([0, 0.3, 0])
        glow = Dot(radius=0.34, color=RED).set_opacity(0.35).move_to(ball.get_center())
        a1 = Arrow([0, 0.1, 0], [-1.3, -0.25, 0], buff=0, stroke_width=6, color=RED)
        a2 = Arrow([0, 0.1, 0], [1.3, -0.25, 0], buff=0, stroke_width=6, color=RED)
        self.play(FadeIn(glow), FadeIn(ball), GrowArrow(a1), GrowArrow(a2), run_time=0.6)
        self.reg(ball, glow, a1, a2)
        self.wait(0.4)
        self.sub_in("多数人选第一个罐子", 0.2)
        box = SurroundingRectangle(VGroup(j1, t1), buff=0.12).set_stroke(GREEN, 4)
        self.play(Create(box), run_time=0.4)
        self.reg(box)
        pick = Text("多数人选它", font=SONG, weight="BOLD", font_size=36,
                    color=GREEN).move_to([-3.6, -2.85, 0])
        self.play(FadeIn(pick), run_time=0.3)
        self.reg(pick)
        self.wait(1.0)

    # ---------- S10 第二问 41.8-49.5 ----------
    def s10_q2(self):
        self.wipe(0.25)
        self.chapter_in(2, 8)
        t = Text("第二问：赌哪个罐子出黑球？", font=SONG, weight="BOLD", font_size=46,
                 color=INK).move_to([0, 3.15, 0])
        self.play(FadeIn(t, lag_ratio=0.08), run_time=0.45)
        self.reg(t)
        t1 = Text("第一个罐子", font=SONG, weight="BOLD", font_size=36,
                  color=BLUE).move_to([-3.6, 2.15, 0])
        t2 = Text("第二个罐子", font=SONG, weight="BOLD", font_size=36,
                  color=RED).move_to([3.6, 2.15, 0])
        j1 = jar(0.92).move_to([-3.6, -0.5, 0])
        j2 = jar(0.92).move_to([3.6, -0.5, 0])
        g1 = dot_grid(10, 10, lambda i, jj: RED if (i * 10 + jj) % 2 == 0 else DARK)
        g1.move_to(j1[0].get_center() + DOWN * 0.12).scale(0.96)
        g2 = gray_grid(j2, seed=31).scale(0.96).move_to(j2[0].get_center() + DOWN * 0.12)
        self.play(FadeIn(t1), FadeIn(t2), FadeIn(j1), FadeIn(j2), FadeIn(g1),
                  run_time=0.45)
        self.play(FadeIn(g2), run_time=0.5)
        self.reg(t1, t2, j1, j2, g1, g2)
        self.sub_in("再问：赌第一个罐子出黑球", 0.2)
        self.wait(0.5)
        self.sub_in("还是赌第二个罐子出黑球？", 0.2)
        ball = Dot(radius=0.16, color=DARK).move_to([0, 0.3, 0])
        glow = Dot(radius=0.34, color=DARK).set_opacity(0.3).move_to(ball.get_center())
        a1 = Arrow([0, 0.1, 0], [-1.3, -0.25, 0], buff=0, stroke_width=6, color=INK)
        a2 = Arrow([0, 0.1, 0], [1.3, -0.25, 0], buff=0, stroke_width=6, color=GRAY)
        self.play(FadeIn(glow), FadeIn(ball), GrowArrow(a1), GrowArrow(a2), run_time=0.6)
        self.reg(ball, glow, a1, a2)
        self.wait(0.4)
        self.sub_in("多数人还是选第一个罐子", 0.2)
        box = SurroundingRectangle(VGroup(j1, t1), buff=0.12).set_stroke(GREEN, 4)
        self.play(Create(box), run_time=0.4)
        self.reg(box)
        pick = Text("多数人还是选它", font=SONG, weight="BOLD", font_size=36,
                    color=GREEN).move_to([-3.6, -2.85, 0])
        self.play(FadeIn(pick), run_time=0.3)
        self.reg(pick)
        self.wait(1.2)

    # ---------- S11 问题来了 49.5-50.8 ----------
    def s11_problem(self):
        self.wipe(0.25)
        j1 = jar(0.9).move_to([-5.6, -0.3, 0]).set_opacity(0.25)
        j2 = jar(0.9).move_to([5.6, -0.3, 0]).set_opacity(0.25)
        q = MathTex("?", font_size=150, color=PURPLE).move_to([0, 0.6, 0]).set_opacity(0.3)
        self.reg(j1, j2, q)
        t = Text("问题来了。", font=SONG, weight="BOLD", font_size=110,
                 color=RED).move_to([0.6, -0.4, 0])
        self.play(FadeIn(t, scale=1.2), run_time=0.35)
        self.reg(t)
        self.sub_in("问题来了", 0.2)
        self.wait(0.4)

    # ---------- S12 红球<50 50.8-57 ----------
    def s12_red(self):
        self.wipe(0.25)
        self.chapter_in(4, 8)
        t = Text("第二个罐子", font=SONG, weight="BOLD", font_size=44,
                 color=RED).move_to([-3.7, 2.7, 0])
        j = jar(1.0).move_to([-3.7, -0.4, 0])
        rng = np.random.default_rng(23)
        g = dot_grid(10, 10, lambda i, jj: RED if rng.uniform() < 0.55 else DARK)
        g.move_to(j[0].get_center() + DOWN * 0.12).scale(0.98)
        self.play(FadeIn(t, lag_ratio=0.08), FadeIn(j), FadeIn(g), run_time=0.5)
        self.reg(t, j, g)
        self.sub_in("如果认为第二个罐子出红不如第一个罐子出红", 0.2)
        base = Line([0.3, 0.3, 0], [6.8, 0.3, 0]).set_stroke(GRAY, 2)
        bg = Rectangle(width=6.5, height=0.55).set_fill("#F1EAE0", 1).set_stroke(width=0)
        bg.move_to([3.55, 0.58, 0])
        mid = Line([3.55, 0.15, 0], [3.55, 1.0, 0]).set_stroke(INK, 2.5)
        red = Rectangle(width=0.01, height=0.55).set_fill(RED, 1).set_stroke(width=0)
        red.move_to([0.31, 0.58, 0]).align_to(bg, LEFT)
        self.play(FadeIn(bg), FadeIn(base), FadeIn(mid), run_time=0.35)
        self.play(red.animate.stretch_to_fit_width(3.2).move_to(
            [0.31 + 1.6, 0.58, 0]).align_to(bg, LEFT), run_time=0.8)
        self.reg(base, bg, mid, red)
        fifty = Text("50", font=SONG, font_size=30, color=INK).move_to([3.85, 0.58, 0])
        self.play(FadeIn(fifty), run_time=0.2)
        self.reg(fifty)
        l = VGroup(Text("红球", font=SONG, weight="BOLD", font_size=40, color=RED),
                   MathTex("<", font_size=48, color=RED),
                   Text("50", font=SONG, weight="BOLD", font_size=44, color=RED),
                   ).arrange(RIGHT, buff=0.18).move_to([3.55, -0.7, 0])
        self.play(FadeIn(l, scale=1.2), run_time=0.3)
        self.reg(l)
        self.sub_in("就等于认为第二个罐子的红球少于50个", 0.2)
        self.wait(1.6)

    # ---------- S13 黑球<50 57-64.5 ----------
    def s13_black(self):
        self.wipe(0.25)
        self.chapter_in(5, 8)
        t = Text("第二个罐子", font=SONG, weight="BOLD", font_size=44,
                 color=RED).move_to([-3.7, 2.7, 0])
        j = jar(1.0).move_to([-3.7, -0.4, 0])
        rng = np.random.default_rng(23)
        g = dot_grid(10, 10, lambda i, jj: RED if rng.uniform() < 0.55 else DARK)
        g.move_to(j[0].get_center() + DOWN * 0.12).scale(0.98)
        self.play(FadeIn(t, lag_ratio=0.08), FadeIn(j), FadeIn(g), run_time=0.5)
        self.reg(t, j, g)
        self.sub_in("如果认为第二个罐子出黑不如第一个罐子出黑", 0.2)
        bar_r = seg_bar([(RED, 0.5), ("#F1EAE0", 0.5)], w=4.4, h=0.55, y=0.95, x=3.9)
        l_r = VGroup(Text("红球", font=SONG, weight="BOLD", font_size=36, color=RED),
                     MathTex("<", font_size=42, color=RED),
                     Text("50", font=SONG, weight="BOLD", font_size=40, color=RED),
                     ).arrange(RIGHT, buff=0.15).move_to([3.9, 0.1, 0])
        bar_b = seg_bar([(DARK, 0.5), ("#F1EAE0", 0.5)], w=4.4, h=0.55, y=-1.0, x=3.9)
        l_b = VGroup(Text("黑球", font=SONG, weight="BOLD", font_size=36, color=DARK),
                     MathTex("<", font_size=42, color=DARK),
                     Text("50", font=SONG, weight="BOLD", font_size=40, color=DARK),
                     ).arrange(RIGHT, buff=0.15).move_to([3.9, -1.95, 0])
        self.play(FadeIn(bar_r), FadeIn(l_r), run_time=0.45)
        self.play(FadeIn(bar_b), FadeIn(l_b), run_time=0.45)
        self.reg(bar_r, l_r, bar_b, l_b)
        self.sub_in("就等于认为第二个罐子的黑球也少于50个", 0.2)
        self.wait(1.8)

    # ---------- S14 总共100个球 64.5-70 ----------
    def s14_100(self):
        self.wipe(0.25)
        self.chapter_in(6, 8)
        t = Text("第二个罐子里总共只有", font=SONG, font_size=38,
                 color=INK).move_to([0, 2.2, 0])
        n = DecimalNumber(55, num_decimal_places=0, font_size=130,
                          color=BLUE).move_to([-0.7, 0.4, 0])
        ge = Text("个球", font=SONG, weight="BOLD", font_size=72,
                  color=BLUE).move_to([1.9, 0.4, 0])
        self.play(FadeIn(t), FadeIn(n), FadeIn(ge), run_time=0.4)
        self.play(ChangeDecimalToValue(n, 100), run_time=0.7)
        self.reg(t, n, ge)
        self.sub_in("可第二个罐子总共只有100个球", 0.2)
        bar = grad_bar().move_to([0, -1.6, 0])
        l1 = Text("红球", font=SONG, weight="BOLD", font_size=30,
                  color=RED).move_to([-3.1, -2.25, 0])
        l2 = Text("黑球", font=SONG, weight="BOLD", font_size=30,
                  color=DARK).move_to([3.1, -2.25, 0])
        self.play(FadeIn(bar), FadeIn(l1), FadeIn(l2), run_time=0.5)
        self.reg(bar, l1, l2)
        e = VGroup(Text("红球", font=SONG, weight="BOLD", font_size=34, color=RED),
                   Text("+", font=SONG, font_size=38, color=INK),
                   Text("黑球", font=SONG, weight="BOLD", font_size=34, color=DARK),
                   MathTex("=", font_size=44, color=INK),
                   Text("100", font=SONG, weight="BOLD", font_size=44, color=BLUE),
                   ).arrange(RIGHT, buff=0.16).move_to([0, -2.9, 0])
        self.play(FadeIn(e), run_time=0.35)
        self.reg(e)
        self.sub_in("红球加黑球必须等于100", 0.2)
        self.wait(1.4)

    # ---------- S15 矛盾 70-75 ----------
    def s15_conflict(self):
        self.wipe(0.25)
        self.chapter_in(7, 8)
        bar = seg_bar([(RED, 0.49), (DARK, 0.49), ("#F1EAE0", 0.02)],
                      w=7.6, h=1.0, y=-0.6)
        l1 = Text("红球 < 50", font=SONG, weight="BOLD", font_size=34,
                  color=RED).move_to([-2.3, 0.55, 0])
        l2 = Text("黑球 < 50", font=SONG, weight="BOLD", font_size=34,
                  color=DARK).move_to([1.4, 0.55, 0])
        self.play(FadeIn(bar), FadeIn(l1), FadeIn(l2), run_time=0.5)
        self.reg(bar, l1, l2)
        q = Text("？", font=SONG, weight="BOLD", font_size=52,
                 color=RED).move_to([3.35, -0.6, 0])
        qb = RoundedRectangle(corner_radius=0.12, width=1.15, height=1.15)
        qb.set_stroke(RED, 3).set_fill("#FBE9E9", 1).move_to([3.35, -0.6, 0])
        lt = Text("少于 100", font=SONG, font_size=30, color=RED).move_to([3.5, -1.5, 0])
        self.play(FadeIn(qb), FadeIn(q), FadeIn(lt), run_time=0.4)
        self.reg(qb, q, lt)
        self.sub_in("两个都少于50，总和就少于100，矛盾", 0.2)
        br = Arc(radius=1.35, start_angle=-PI * 0.42, angle=-PI * 0.16,
                 stroke_width=3.5, color=RED).move_to([-0.5, 0.35, 0])
        st = stamp("矛盾", color=RED, size=72).move_to([0.9, -0.6, 0]).rotate(-0.06)
        self.play(Create(br), run_time=0.35)
        self.play(FadeIn(st, scale=1.6), run_time=0.35)
        self.reg(br, st)
        self.sub_in("也就是说", 0.2)
        self.wait(0.9)

    # ---------- S16 违背效用 75-82.5 ----------
    def s16_utility(self):
        self.wipe(0.25)
        self.chapter_in(8, 8)
        t = VGroup(Text("人的选择", font=SONG, weight="BOLD", font_size=48, color=INK),
                   Text("违背", font=SONG, weight="BOLD", font_size=48, color=RED),
                   Text("了主观期望效用", font=SONG, weight="BOLD", font_size=48,
                        color=INK),
                   ).arrange(RIGHT, buff=0.1).move_to([0, 3.0, 0])
        self.play(FadeIn(t, lag_ratio=0.06), run_time=0.5)
        self.reg(t)
        lt = Text("只按概率算", font=SONG, weight="BOLD", font_size=36,
                  color=BLUE).move_to([-3.9, 1.9, 0])
        bar = seg_bar([(BLUE, 0.5), ("#F1EAE0", 0.5)], w=4.6, h=1.1, y=0.4, x=-3.9)
        self.play(FadeIn(lt, lag_ratio=0.08), run_time=0.35)
        self.play(FadeIn(bar), run_time=0.4)
        self.reg(lt, bar)
        cross = Line([-6.2, 0.95, 0], [-1.6, -0.15, 0]).set_stroke(RED, 6)
        self.play(Create(cross), run_time=0.4)
        self.reg(cross)
        self.sub_in("人的选择违背了主观期望效用：", 0.2)
        pz = Text("概率未知", font=SONG, weight="BOLD", font_size=36,
                  color=PURPLE).move_to([4.0, 1.9, 0])
        bl = blob(seed=13).move_to([4.0, 0.4, 0])
        st = stamp("厌恶", color=RED, size=56).move_to([4.0, 0.4, 0]).rotate(-0.1)
        self.play(FadeIn(pz, lag_ratio=0.08), run_time=0.3)
        self.play(FadeIn(bl), run_time=0.4)
        self.play(FadeIn(st, scale=1.5), run_time=0.3)
        self.reg(pz, bl, st)
        self.sub_in("我们不是单纯按概率做决定", 0.2)
        self.wait(0.6)
        big = Text("而是厌恶概率未知", font=SONG, weight="BOLD", font_size=72,
                   color=RED).move_to([0, -2.35, 0])
        self.play(FadeIn(big, lag_ratio=0.06), run_time=0.45)
        self.reg(big)
        self.sub_in("而是厌恶概率未知这件事", 0.2)
        self.wait(1.2)

    # ---------- S17 两家店 82.5-94.5 ----------
    def s17_shops(self):
        self.wipe(0.25)
        self.chapter_in(1, 6)
        t = Text("通俗类比：两家店", font=SONG, weight="BOLD", font_size=48,
                 color=INK).move_to([0, 3.15, 0])
        self.play(FadeIn(t, lag_ratio=0.08), run_time=0.4)
        self.reg(t)
        s1 = shop(1.0, BLUE).move_to([-3.6, -0.3, 0])
        s2 = shop(1.0, RED).move_to([3.6, -0.3, 0])
        l1 = Text("第一家店", font=SONG, weight="BOLD", font_size=34,
                  color=BLUE).move_to([-3.6, -2.4, 0])
        l2 = Text("第二家店", font=SONG, weight="BOLD", font_size=34,
                  color=RED).move_to([3.6, -2.4, 0])
        self.play(FadeIn(s1), FadeIn(s2), FadeIn(l1), FadeIn(l2), run_time=0.5)
        self.reg(s1, s2, l1, l2)
        self.sub_in("通俗类比：两家店", 0.2)
        t2 = Text("一家明确告诉你：中奖率一半", font=SONG, weight="BOLD",
                  font_size=40, color=INK).move_to([0, 2.3, 0])
        _c1 = RoundedRectangle(corner_radius=0.1, width=1.6, height=0.95)
        _c1.set_stroke(BLUE, 2.5).set_fill(WHITE, 1).move_to([-3.6, 0.3, 0])
        c1 = VGroup(_c1,
                    Text("中奖率", font=SONG, font_size=24, color=INK)
                    .move_to(_c1.get_center() + UP * 0.22),
                    Text("50%", font=SONG, weight="BOLD", font_size=40, color=BLUE)
                    .move_to(_c1.get_center() + DOWN * 0.16))
        bar1 = seg_bar([(BLUE, 0.5), ("#F1EAE0", 0.5)], w=2.6, h=0.3, y=-1.05, x=-3.6)
        self.play(FadeIn(t2, lag_ratio=0.08), run_time=0.35)
        self.reg(t2)
        self.play(FadeIn(c1), FadeIn(bar1), run_time=0.4)
        self.reg(c1, bar1)
        self.chapter_in(2, 6)
        self.sub_in("一家明确告诉你中奖率一半", 0.2)
        self.wait(0.7)
        t3 = Text("另一家只说：可能中，也可能不中", font=SONG, weight="BOLD",
                  font_size=40, color=INK).move_to([0, 2.3, 0])
        _c2 = RoundedRectangle(corner_radius=0.1, width=1.9, height=1.05)
        _c2.set_stroke(PURPLE, 2.5).set_fill(WHITE, 1).move_to([3.6, 0.35, 0])
        c2 = VGroup(_c2,
                    Text("可能中", font=SONG, font_size=26, color=RED)
                    .move_to(_c2.get_center() + UP * 0.24),
                    Text("也可能不中", font=SONG, font_size=26, color=RED)
                    .move_to(_c2.get_center() + DOWN * 0.24))
        ring = SurroundingRectangle(c2, buff=0.1).set_stroke(PURPLE, 3)
        bar2 = seg_bar([(RED, 0.55), ("#F1EAE0", 0.45)], w=2.6, h=0.3, y=-1.05, x=3.6)
        q = MathTex("?", font_size=52, color=PURPLE).move_to([5.05, -0.9, 0])
        self.play(ReplacementTransform(t2, t3), FadeIn(c2), FadeIn(ring),
                  FadeIn(bar2), FadeIn(q), run_time=0.55)
        self.cur[self.cur.index(t2)] = t3
        self.reg(c2, ring, bar2, q)
        self.sub_in("另一家只说可能中，也可能不中", 0.2)
        self.wait(0.8)
        self.wipe(0.25)
        self.chapter_in(4, 6)
        t4 = Text("很多人会选第一家", font=SONG, weight="BOLD", font_size=48,
                  color=GREEN).move_to([0, 3.0, 0])
        s1 = shop(1.0, BLUE).move_to([-3.6, -0.2, 0])
        _c1b = RoundedRectangle(corner_radius=0.1, width=1.7, height=0.8)
        _c1b.set_stroke(BLUE, 2.5).set_fill(WHITE, 1).move_to([-3.6, 0.25, 0])
        c1 = VGroup(_c1b, Text("中奖率 50%", font=SONG, weight="BOLD", font_size=28,
                               color=BLUE).move_to(_c1b.get_center()))
        bar1 = seg_bar([(BLUE, 0.5), ("#F1EAE0", 0.5)], w=2.6, h=0.3, y=-1.0, x=-3.6)
        l1 = Text("第一家店", font=SONG, weight="BOLD", font_size=34,
                  color=BLUE).move_to([-3.6, -2.15, 0])
        s2 = shop(1.0, RED).move_to([3.6, -0.2, 0]).set_opacity(0.35)
        l2 = Text("第二家店", font=SONG, weight="BOLD", font_size=34,
                  color=RED).move_to([3.6, -2.15, 0]).set_opacity(0.35)
        arrow = Arrow([1.9, 0.3, 0], [-1.9, 0.3, 0], buff=0, stroke_width=6,
                      color=GREEN)
        pick = Text("很多人选它", font=SONG, weight="BOLD", font_size=34,
                    color=GREEN).move_to([3.55, 0.62, 0])
        box = SurroundingRectangle(VGroup(s1, c1), buff=0.12).set_stroke(GREEN, 4)
        self.play(FadeIn(t4, lag_ratio=0.08), run_time=0.4)
        self.play(FadeIn(s1), FadeIn(c1), FadeIn(bar1), FadeIn(l1),
                  FadeIn(s2), FadeIn(l2), run_time=0.5)
        self.play(GrowArrow(arrow), FadeIn(pick), Create(box), run_time=0.5)
        self.reg(t4, s1, c1, bar1, l1, s2, l2, arrow, pick, box)
        self.sub_in("很多人会选第一家", 0.2)
        self.wait(0.9)
        self.wipe(0.25)
        self.chapter_in(5, 6)
        _c2b = RoundedRectangle(corner_radius=0.1, width=1.9, height=1.05)
        _c2b.set_stroke(PURPLE, 2.5).set_fill(WHITE, 1).move_to([-2.2, 0.9, 0])
        c2b = VGroup(_c2b,
                     Text("可能中", font=SONG, font_size=26, color=RED)
                     .move_to(_c2b.get_center() + UP * 0.24),
                     Text("也可能不中", font=SONG, font_size=26, color=RED)
                     .move_to(_c2b.get_center() + DOWN * 0.24))
        l2b = Text("第二家店", font=SONG, weight="BOLD", font_size=34,
                   color=RED).move_to([-2.2, -0.55, 0])
        bar2b = seg_bar([(RED, 0.55), ("#F1EAE0", 0.45)], w=2.6, h=0.35, y=-1.25, x=-2.2)
        t5 = Text("哪怕第二家的真实中奖率可能更高", font=SONG, font_size=34,
                  color=INK).move_to([2.3, 2.2, 0])
        bar3 = seg_bar([(RED, 0.62), (GREEN, 0.14), ("#F1EAE0", 0.24)],
                       w=4.6, h=0.55, y=0.4, x=2.7)
        fifty = Text("50%", font=SONG, font_size=26, color=INK).move_to([2.45, 0.4, 0])
        arr = Arrow([3.9, 1.05, 0], [4.6, 0.75, 0], buff=0, stroke_width=5,
                    color=GREEN)
        ghi = Text("可能更高", font=SONG, weight="BOLD", font_size=30,
                   color=GREEN).move_to([5.1, 1.15, 0])
        real = Text("真实中奖率可能更高", font=SONG, weight="BOLD", font_size=38,
                    color=GREEN).move_to([2.7, -0.45, 0])
        self.play(FadeIn(c2b), FadeIn(l2b), FadeIn(bar2b), run_time=0.4)
        self.play(FadeIn(t5, lag_ratio=0.06), run_time=0.3)
        self.play(FadeIn(bar3), FadeIn(fifty), run_time=0.4)
        self.play(GrowArrow(arr), FadeIn(ghi), FadeIn(real), run_time=0.45)
        self.reg(c2b, l2b, bar2b, t5, bar3, fifty, arr, ghi, real)
        self.sub_in("哪怕第二家的真实中奖率可能更高", 0.2)
        self.wait(2.6)

    # ---------- S18 对模糊的回避 94.5-98.5 ----------
    def s18_avoid(self):
        self.wipe(0.25)
        self.chapter_in(6, 6)
        bl = VGroup()
        rng = np.random.default_rng(19)
        for _ in range(14):
            c = Circle(radius=rng.uniform(0.5, 1.0)).set_stroke(width=0)
            c.set_fill(PURPLE, rng.uniform(0.08, 0.2))
            c.move_to([rng.uniform(-6.5, 6.5), rng.uniform(-2.8, 2.8), 0])
            bl.add(c)
        self.play(FadeIn(bl), run_time=0.7)
        self.reg(bl)
        star = VGroup(*[Line(ORIGIN, np.array([np.cos(a), np.sin(a), 0]) * 0.5)
                        .set_stroke(RED, 3) for a in np.arange(0, TAU, TAU / 8)])
        star.move_to([0, 0.2, 0])
        rings = VGroup(*[Circle(radius=0.7 + i * 0.65).set_stroke(RED, 2.5, opacity=0.7)
                         .move_to([0, 0.2, 0]) for i in range(3)])
        self.play(FadeIn(star), Create(rings), run_time=0.5)
        self.reg(star, rings)
        e = VGroup(Text("对模糊的回避", font=SONG, weight="BOLD", font_size=56,
                        color=BLUE),
                   MathTex("=", font_size=60, color=INK),
                   Text("埃尔斯伯格悖论", font=SONG, weight="BOLD", font_size=56,
                        color=RED),
                   ).arrange(RIGHT, buff=0.2).move_to([0, 0.2, 0])
        self.play(FadeIn(e, scale=1.15), run_time=0.45)
        self.reg(e)
        self.sub_in("这种对模糊的回避", 0.2)
        self.wait(0.5)
        self.sub_in("就是埃尔伯格悖论", 0.2)
        self.wait(0.8)

    # ---------- S19 黑场 98.5-99.5 ----------
    def s19_dark(self):
        self.wipe(0.35)
        bg = Rectangle(width=16.4, height=9.4).set_fill("#141014", 1).set_stroke(width=0)
        self.add(bg)
        self.reg(bg)
        rose = VGroup(Circle(radius=0.8).set_stroke(PINK, 3).set_fill(PINK, 0.5))
        rose.move_to([0, 0.3, 0]).set_opacity(0.25)
        t = Text("从数学，到爱情", font=SONG, weight="BOLD", font_size=44,
                 color="#F0C8C8").move_to([0, -1.6, 0]).set_opacity(0.4)
        self.play(FadeIn(rose), FadeIn(t), run_time=0.3)
        self.reg(rose, t)
        self.wait(0.35)

    # ---------- S20 从数学到爱情 99.5-110.5 ----------
    def s20_love(self):
        self.wipe(0.3)
        self.chapter_in(1, 7)
        t = VGroup(Text("从数学，到", font=SONG, weight="BOLD", font_size=54, color=INK),
                   Text("爱情", font=SONG, weight="BOLD", font_size=54, color=RED),
                   ).arrange(RIGHT, buff=0.08).move_to([0, 2.6, 0])
        m1 = stickman(1.05).move_to([-3.3, -0.9, 0])
        m2 = stickman(1.05).move_to([3.3, -0.9, 0])
        heart = ParametricFunction(
            lambda tt: np.array([16 * np.sin(tt) ** 3 * 0.085,
                                 (13 * np.cos(tt) - 5 * np.cos(2 * tt)
                                  - 2 * np.cos(3 * tt) - np.cos(4 * tt)) * 0.085, 0]),
            t_range=[0, TAU], color=RED).set_fill(RED, 1).set_stroke(width=0)
        heart.move_to([0, -0.6, 0])
        floor = Line([-7.2, -2.55, 0], [7.2, -2.55, 0]).set_stroke(GRAY, 2)
        self.play(FadeIn(t, lag_ratio=0.08), run_time=0.4)
        self.play(FadeIn(m1), FadeIn(m2), FadeIn(heart, scale=0.5), FadeIn(floor),
                  run_time=0.5)
        self.reg(t, m1, m2, heart, floor)
        self.sub_in("从数学到爱情", 0.2)
        self.wait(0.7)
        t2 = VGroup(Text("埃尔伯格式", font=SONG, weight="BOLD", font_size=50,
                         color=RED),
                    Text("的选择", font=SONG, weight="BOLD", font_size=50, color=INK),
                    ).arrange(RIGHT, buff=0.1).move_to([0, 2.6, 0])
        self.play(ReplacementTransform(t, t2), run_time=0.5)
        self.cur[self.cur.index(t)] = t2
        self.sub_in("我们常做埃尔斯伯格式选择", 0.2)
        self.wait(0.6)
        # 两个人头顶卡片
        _c1 = RoundedRectangle(corner_radius=0.1, width=1.55, height=1.3)
        _c1.set_stroke(BLUE, 2.5).set_fill("#EAF3FC", 1).move_to([-3.3, 0.3, 0])
        c1 = VGroup(_c1,
                    Text("五成", font=SONG, font_size=22, color=INK)
                    .move_to(_c1.get_center() + UP * 0.3),
                    Text("50%", font=SONG, weight="BOLD", font_size=38, color=BLUE)
                    .move_to(_c1.get_center() + DOWN * 0.22))
        _c2 = RoundedRectangle(corner_radius=0.1, width=1.55, height=1.3)
        _c2.set_stroke(RED, 2.5).set_fill("#FBE9E9", 1).move_to([3.3, 0.3, 0])
        c2 = VGroup(_c2,
                    Text("说不清", font=SONG, font_size=22, color=RED)
                    .move_to(_c2.get_center() + UP * 0.3),
                    MathTex("?", font_size=36, color=RED)
                    .move_to(_c2.get_center() + DOWN * 0.22))
        l1 = Text("明确表达五成好感", font=SONG, font_size=30,
                  color=BLUE).move_to([-3.3, -2.95, 0])
        l2 = Text("心意模糊但可能更深", font=SONG, font_size=30,
                  color=RED).move_to([3.3, -2.95, 0])
        self.play(FadeIn(c1, scale=0.8), run_time=0.35)
        self.play(FadeIn(c2, scale=0.8), run_time=0.35)
        self.play(FadeIn(l1), FadeIn(l2), run_time=0.3)
        self.reg(c1, c2, l1, l2)
        self.sub_in("一个人明确表达五成好感", 0.2)
        self.wait(0.5)
        self.sub_in("另一个人心意模糊但可能更深", 0.2)
        self.wait(0.5)
        self.wipe(0.25)
        self.chapter_in(3, 7)
        t3 = Text("很多人会选前者", font=SONG, weight="BOLD", font_size=50,
                  color=GREEN).move_to([0, 2.7, 0])
        self.play(FadeIn(t3, lag_ratio=0.08), run_time=0.4)
        self.reg(t3)
        m3 = stickman(1.0).move_to([-3.3, -0.9, 0])
        _c1c = RoundedRectangle(corner_radius=0.1, width=1.7, height=0.8)
        _c1c.set_stroke(BLUE, 2.5).set_fill("#EAF3FC", 1).move_to([-3.3, 0.5, 0])
        c1 = VGroup(_c1c, Text("五成 50%", font=SONG, weight="BOLD", font_size=28,
                               color=BLUE).move_to(_c1c.get_center()))
        box = SurroundingRectangle(VGroup(m3, c1), buff=0.12).set_stroke(GREEN, 4)
        crowd = VGroup(*[stickman(0.62, pose="raised")
                         .move_to([-5.4 + i * 0.85, -1.6, 0]) for i in range(7)])
        self.play(FadeIn(m3), FadeIn(c1), Create(box), run_time=0.45)
        self.play(LaggedStart(*[FadeIn(c, scale=0.5) for c in crowd], lag_ratio=0.06),
                  run_time=0.6)
        self.reg(t3, m3, c1, box, crowd)
        self.sub_in("很多人会选前者", 0.2)
        self.wait(0.8)
        self.sub_in("因为已知的拒绝，像第一个罐子", 0.2)
        self.wait(1.0)

    # ---------- S21 已知的拒绝 110.5-113.5 ----------
    def s21_refuse(self):
        self.wipe(0.25)
        self.chapter_in(4, 7)
        t = VGroup(Text("已知的", font=SONG, weight="BOLD", font_size=46, color=INK),
                   Text("拒绝", font=SONG, weight="BOLD", font_size=46, color=RED),
                   Text("，像第一个罐子", font=SONG, weight="BOLD", font_size=46,
                        color=INK),
                   ).arrange(RIGHT, buff=0.08).move_to([0, 3.0, 0])
        self.play(FadeIn(t, lag_ratio=0.08), run_time=0.4)
        self.reg(t)
        j = jar(0.92).move_to([-3.5, -0.4, 0])
        g = dot_grid(10, 10, lambda i, jj: RED if (i * 10 + jj) % 2 == 0 else DARK)
        g.move_to(j[0].get_center() + DOWN * 0.12).scale(0.96)
        bar = seg_bar([(BLUE, 0.5), ("#F1EAE0", 0.5)], w=2.3, h=0.32, y=-2.35, x=-3.5)
        lb = Text("比例清楚", font=SONG, font_size=26, color=BLUE).move_to([-3.5, -2.85, 0])
        self.play(FadeIn(j), FadeIn(g), FadeIn(bar), FadeIn(lb), run_time=0.5)
        self.reg(t, j, g, bar, lb)
        man = stickman(1.1).move_to([3.6, -0.8, 0])
        self.play(FadeIn(man), run_time=0.3)
        self.reg(man)
        arrow = Arrow([-2.3, -0.5, 0], [2.7, -0.75, 0], buff=0, stroke_width=5,
                      color=RED)
        rej = Text("拒绝", font=SONG, weight="BOLD", font_size=34,
                   color=RED).move_to([0.1, -0.1, 0])
        self.play(GrowArrow(arrow), FadeIn(rej), run_time=0.4)
        star = VGroup(*[Line(ORIGIN, np.array([np.cos(a), np.sin(a), 0]) * 0.32)
                        .set_stroke(RED, 4) for a in np.arange(0, TAU, TAU / 6)])
        star.move_to([3.6, -0.55, 0])
        self.play(FadeIn(star, scale=1.8), run_time=0.3)
        self.reg(arrow, rej, star)
        pt = Text("痛得明白", font=SONG, weight="BOLD", font_size=34,
                  color=RED).move_to([3.6, -2.6, 0])
        self.play(FadeIn(pt), run_time=0.3)
        self.reg(pt)
        self.sub_in("因为已知的拒绝像第一个罐子", 0.2)
        self.sub_in("痛也痛得明白", 0.2)
        self.wait(0.6)

    # ---------- S22 未知的回应 113.5-120.5 ----------
    def s22_unknown(self):
        self.wipe(0.25)
        self.chapter_in(5, 7)
        t = VGroup(Text("未知", font=SONG, weight="BOLD", font_size=46, color=RED),
                   Text("的回应，像第二个罐子", font=SONG, weight="BOLD",
                        font_size=46, color=INK),
                   ).arrange(RIGHT, buff=0.08).move_to([0, 3.0, 0])
        self.play(FadeIn(t, lag_ratio=0.08), run_time=0.4)
        self.reg(t)
        j = jar(0.92).move_to([-3.5, -0.4, 0])
        rng = np.random.default_rng(23)
        g = dot_grid(10, 10, lambda i, jj: RED if rng.uniform() < 0.55 else DARK)
        g.move_to(j[0].get_center() + DOWN * 0.12).scale(0.96)
        q = MathTex("?", font_size=70, color=RED).move_to([-3.5, 1.4, 0])
        l1 = Text("可能全红，也可能全黑", font=SONG, font_size=28,
                  color=RED).move_to([-3.5, -2.55, 0])
        self.play(FadeIn(j), FadeIn(g), FadeIn(q), FadeIn(l1), run_time=0.5)
        self.reg(t, j, g, q, l1)
        man = stickman(1.1).move_to([3.6, -0.9, 0])
        circ = Circle(radius=0.62).set_stroke(RED, 3).move_to(man[0].get_center())
        self.play(FadeIn(man), run_time=0.3)
        self.play(Create(circ), run_time=0.35)
        shake = man.animate.shift(RIGHT * 0.06)
        self.play(shake, run_time=0.08)
        self.play(man.animate.shift(LEFT * 0.12), run_time=0.08)
        self.play(man.animate.shift(RIGHT * 0.06), run_time=0.08)
        self.reg(man, circ)
        unc = Text("等待让人不安", font=SONG, weight="BOLD", font_size=34,
                   color=BLUE).move_to([3.6, -2.6, 0])
        self.play(FadeIn(unc), run_time=0.3)
        self.reg(unc)
        self.sub_in("未知的回应像第二个罐子，可能全红", 0.2)
        self.wait(0.6)
        self.sub_in("也可能全黑。等待让人不安", 0.2)
        self.wait(1.8)

    # ---------- S23 抱紧罐子 120.5-126.5 ----------
    def s23_hug(self):
        self.wipe(0.25)
        self.chapter_in(6, 7)
        t = VGroup(Text("抱紧那个「", font=SONG, weight="BOLD", font_size=46, color=INK),
                   Text("概率确定", font=SONG, weight="BOLD", font_size=46, color=BLUE),
                   Text("」的罐子", font=SONG, weight="BOLD", font_size=46, color=INK),
                   ).arrange(RIGHT, buff=0.06).move_to([0, 3.0, 0])
        self.play(FadeIn(t, lag_ratio=0.08), run_time=0.45)
        self.reg(t)
        j = jar(0.85).move_to([0, -1.0, 0])
        g = dot_grid(10, 10, lambda i, jj: RED if (i * 10 + jj) % 2 == 0 else DARK)
        g.move_to(j[0].get_center() + DOWN * 0.1).scale(0.9)
        self.play(FadeIn(j), FadeIn(g), run_time=0.5)
        self.reg(t, j, g)
        man = stickman(0.95, pose="hug").move_to([0, -0.75, 0])
        man[0].move_to([0, -0.1, 0])   # 头贴罐顶
        self.play(FadeIn(man), run_time=0.4)
        self.reg(man)
        self.sub_in("于是，为了逃避这种悬而未决的折磨", 0.2)
        gray = Text("为了逃避悬而未决的折磨", font=SONG, font_size=28,
                    color=GRAY).move_to([0, -3.05, 0])
        self.play(FadeIn(gray), run_time=0.25)
        self.reg(gray)
        self.wait(0.6)
        self.sub_in("我们主动抱紧了那个「概率确定」的罐子", 0.2)
        self.wait(1.1)

    # ---------- S24 遗憾与圆满 126.5-131.5 ----------
    def s24_ending(self):
        self.wipe(0.3)
        self.chapter_in(7, 7)
        t1 = Text("确定的遗憾", font=SONG, weight="BOLD", font_size=40,
                  color=RED).move_to([-3.9, 2.3, 0])
        t2 = Text("未知的圆满", font=SONG, weight="BOLD", font_size=40,
                  color=BLUE).move_to([3.9, 2.3, 0])
        j1 = jar(0.95).move_to([-3.9, -0.3, 0])
        g1 = dot_grid(10, 10, lambda i, jj: RED if (i * 10 + jj) % 2 == 0 else DARK)
        g1.move_to(j1[0].get_center() + DOWN * 0.12).scale(0.96)
        j2 = jar(0.95).move_to([3.9, -0.3, 0])
        g2 = gray_grid(j2, seed=41).scale(0.96).move_to(j2[0].get_center() + DOWN * 0.12)
        man = stickman(1.15, pose="open").move_to([0, -1.1, 0])
        floor = Line([-7.2, -2.75, 0], [7.2, -2.75, 0]).set_stroke(GRAY, 2)
        self.play(FadeIn(t1, lag_ratio=0.08), FadeIn(t2, lag_ratio=0.08), run_time=0.4)
        self.play(FadeIn(j1), FadeIn(g1), FadeIn(j2), FadeIn(g2), FadeIn(man),
                  FadeIn(floor), run_time=0.5)
        self.reg(t1, t2, j1, g1, j2, g2, man, floor)
        self.sub_in("在感情里", 0.2)
        self.wait(0.5)
        self.sub_in("我们宁愿要一个确定的遗憾", 0.2)
        e = VGroup(Text("宁愿要一个", font=SONG, weight="BOLD", font_size=52, color=INK),
                   Text("确定的遗憾", font=SONG, weight="BOLD", font_size=52, color=RED),
                   Text("，也不敢去赌一个", font=SONG, weight="BOLD", font_size=52,
                        color=INK),
                   Text("未知的圆满", font=SONG, weight="BOLD", font_size=52, color=BLUE),
                   ).arrange(RIGHT, buff=0.1).move_to([0, -3.35, 0])
        e.scale_to_fit_width(15.2)
        self.play(FadeIn(e, lag_ratio=0.05), run_time=0.6)
        self.reg(e)
        self.sub_in("也不敢去赌一个未知的圆满", 0.2)
        self.wait(2.0)
        self.play(*[FadeOut(m) for m in self.cur], run_time=0.6)
        self.cur = []
