# -*- coding: utf-8 -*-
"""
《我一个 3000 粉的小博主，竟遭遇了网暴》
Manim CE 0.21.0 / 1920x1080 / 16:9
风格：米白纸面 + 宋体标题 + 彩色圆角框（宋体定理片）
      × 火柴人 + 印章 + 章节标记（简笔科普片）
"""

from manim import *
import numpy as np

config.pixel_width, config.pixel_height = 1920, 1080
config.frame_width, config.frame_height = 16.0, 9.0
config.background_color = "#FBF6EF"
config.media_dir = "/Users/fengtianzhu/WorkBuddy/2026-09-15-21-50-18/songti_manim/media"

RED = "#E8535A"
BLUE = "#4A9DE8"
GREEN = "#2BB89A"
PURPLE = "#8B7BE8"
GOLD = "#E8A84B"
INK = "#3A3A3C"
GRAY = "#B8AFA5"
GRIDC = "#E8E0D6"
CFB = "#EAF3FC"
CFR = "#FCEAEB"
CFG = "#E8F7F2"
CFP = "#F0EEFE"
CFGOLD = "#FBF0DA"
SONG = "Songti SC"
HEI = "PingFang SC"

SAFE_W = 14.0
SUB_FS = 32


# ---------------------------------------------------------------- 组件库
def ST(txt, fs=40, color=INK, font=SONG, weight=BOLD, ls=None):
    kw = dict(font=font, font_size=fs, color=color, weight=weight)
    if ls is not None:
        kw["line_spacing"] = ls
    return Text(txt, **kw)


def fit(mob, w=SAFE_W):
    if mob.width > w:
        mob.scale_to_fit_width(w)
    return mob


def cbox(tex, edge, fill, w=None, h=0.95, fs=36, pad=0.36):
    t = MathTex(tex, font_size=fs, color=edge)
    if w is None:
        w = t.width + 2 * pad
    r = RoundedRectangle(corner_radius=0.14, width=w, height=h)
    r.set_stroke(edge, 2.6).set_fill(fill, 1)
    if t.width > w - 0.3:
        t.scale_to_fit_width(w - 0.3)
    return VGroup(r, t.move_to(r))


def pill(txt, edge=GRAY, tcol=INK, fs=28, fill=WHITE, op=0.94):
    t = ST(txt, fs=fs, color=tcol, font=HEI)
    r = RoundedRectangle(corner_radius=0.12, width=t.width + 0.5, height=t.height + 0.42)
    r.set_stroke(edge, 2.4).set_fill(fill, op)
    return VGroup(r, t.move_to(r))


def man(scale=1.0, pose="stand", color=INK):
    """简笔火柴人：所有 Line 端点一律 3D [x,y,0]。"""
    s = scale
    parts = []
    head = Circle(radius=0.22 * s, color=color, stroke_width=2.6).set_fill(WHITE, 1)
    head.move_to([0, 0.80 * s, 0])
    parts.append(head)
    parts.append(Line([0, 0.58 * s, 0], [0, 0.02 * s, 0]))
    if pose == "open":
        parts.append(Line([0, 0.48 * s, 0], [-0.46 * s, 0.54 * s, 0]))
        parts.append(Line([0, 0.48 * s, 0], [0.46 * s, 0.54 * s, 0]))
    elif pose == "raised":
        parts.append(Line([0, 0.48 * s, 0], [-0.42 * s, 0.92 * s, 0]))
        parts.append(Line([0, 0.48 * s, 0], [0.42 * s, 0.92 * s, 0]))
    elif pose == "point":
        parts.append(Line([0, 0.48 * s, 0], [-0.30 * s, 0.20 * s, 0]))
        parts.append(Line([0, 0.48 * s, 0], [0.62 * s, 0.62 * s, 0]))
    else:
        parts.append(Line([0, 0.48 * s, 0], [-0.30 * s, 0.18 * s, 0]))
        parts.append(Line([0, 0.48 * s, 0], [0.30 * s, 0.18 * s, 0]))
    parts.append(Line([0, 0.02 * s, 0], [-0.28 * s, -0.46 * s, 0]))
    parts.append(Line([0, 0.02 * s, 0], [0.28 * s, -0.46 * s, 0]))
    for p in parts[1:]:
        p.set_stroke(color, 2.6)
    g = VGroup(*parts)
    g.move_to([0, 0, 0])
    return g


def stamp(txt, color=RED, fs=54, rot=-0.06, fill=WHITE, op=0.9):
    t = ST(txt, fs=fs, color=color)
    r = RoundedRectangle(corner_radius=0.12, width=t.width + 0.8, height=t.height + 0.45)
    r.set_stroke(color, 3.6).set_fill(fill, op)
    return VGroup(r, t.move_to(r)).rotate(rot)


def arrow(a, b, color=INK, sw=2.6):
    return Arrow(a, b, buff=0, color=color, stroke_width=sw,
                 max_tip_length_to_length_ratio=0.28, tip_length=0.22)


def bigval(tex, color=GOLD, fs=100):
    """金色高亮数字块：框按公式实际尺寸自适应，避免溢出。"""
    t = MathTex(tex, font_size=fs, color=color)
    r = RoundedRectangle(corner_radius=0.16, width=t.width + 1.2, height=t.height + 0.5)
    r.set_stroke(color, 3.0).set_fill(CFGOLD, 1)
    return VGroup(r, t.move_to(r))


def star(pos, color=GOLD, r=0.15):
    d = Square(side_length=r * 1.5).rotate(PI / 4)
    return d.set_stroke(width=0).set_fill(color, 1).move_to(pos)


def phone(s=1.0):
    """手机（简笔）。"""
    body = RoundedRectangle(corner_radius=0.12, width=0.62 * s, height=1.15 * s)
    body.set_stroke(INK, 2.6).set_fill(WHITE, 1)
    scr = RoundedRectangle(corner_radius=0.06, width=0.5 * s, height=0.86 * s)
    scr.set_stroke("#B9B0A6", 1.6).set_fill("#F2EEE8", 1).move_to(body.get_center())
    dot = Dot(radius=0.035 * s, color="#B9B0A6").move_to(body.get_center() + DOWN * 0.44 * s)
    return VGroup(body, scr, dot)


def bubble(tex, fs=26, h=0.95):
    """聊天气泡（群里的消息）。"""
    m = MathTex(tex, font_size=fs, color=INK)
    w = m.width + 0.7
    r = RoundedRectangle(corner_radius=0.2, width=w, height=h)
    r.set_stroke(GRAY, 2.2).set_fill(WHITE, 0.98)
    if m.width > w - 0.3:
        m.scale_to_fit_width(w - 0.3)
    return VGroup(r, m.move_to(r))


# ---------------------------------------------------------------- 场景
class WangBaoReply(Scene):

    # ---------------- 基础设施 ----------------
    def background(self):
        g = VGroup()
        for x in np.arange(-8.0, 8.01, 0.8):
            g.add(Line([x, -4.5, 0], [x, 4.5, 0]))
        for y in np.arange(-4.5, 4.51, 0.8):
            g.add(Line([-8.0, y, 0], [8.0, y, 0]))
        g.set_stroke(GRIDC, 1.2, 0.8)
        self.add(g)

    def reg(self, *mobs):
        self.cur.extend(mobs)

    def unreg(self, *mobs):
        ids = {id(m) for m in mobs}
        self.cur = [m for m in self.cur if id(m) not in ids]

    def wipe(self, t=0.28):
        out = list(self.cur)
        if self.sub_mob is not None:
            out.append(self.sub_mob)
            self.sub_mob = None
        if out:
            self.play(*[FadeOut(m) for m in out], run_time=t)
        self.cur = []

    def sub_in(self, text, fs=SUB_FS):
        if self.sub_mob is not None:
            self.play(FadeOut(self.sub_mob), run_time=0.14)
            self.remove(self.sub_mob)          # 硬移除，杜绝任何叠印
            self.sub_mob = None
        t = ST(text, fs=fs, color=WHITE, font=HEI)
        t.set_stroke(BLACK, 5, background=True)
        fit(t, 14.6)
        t.to_edge(DOWN, buff=0.34)
        self.play(FadeIn(t, lag_ratio=0.04), run_time=0.45)
        self.sub_mob = t

    def chapter(self, n, total=16):
        c = ST("%02d / %d" % (n, total), fs=26, color="#B0A89E", font=HEI, weight=NORMAL)
        c.to_corner(UL, buff=0.45)
        self.reg(c)
        self.play(FadeIn(c), run_time=0.22)

    def sec(self, txt, y=3.55, color=INK, fs=42):
        t = ST(txt, fs=fs, color=color)
        fit(t, 13.6)
        t.move_to([0, y, 0])
        self.reg(t)
        self.play(FadeIn(t, lag_ratio=0.06), run_time=0.45)
        return t

    # ---------------- 0 标题 ----------------
    def s0_title(self):
        self.wipe()
        t1 = ST("我一个 3000 粉的小博主", fs=66)
        t2 = ST("竟遭遇了网暴", fs=66, color=RED)
        g = VGroup(t1, t2).arrange(DOWN, buff=0.34).move_to([0, 0.3, 0])
        self.reg(g)
        self.play(FadeIn(t1, lag_ratio=0.08), run_time=0.85)
        self.play(FadeIn(t2, lag_ratio=0.08), run_time=0.7)
        self.wait(1.9)
        self.wipe()

    # ---------------- 1 起因（火柴人 MG） ----------------
    def s1_cause(self):
        self.wipe()
        self.chapter(1)

        # 拍1 我：3000 粉的小博主
        me = man(0.95, "stand").move_to([-6.1, -0.35, 0])
        tag_me = pill("3000 粉", GRAY, INK, fs=25).next_to(me, UP, buff=0.18)
        self.reg(me, tag_me)
        self.play(FadeIn(me, shift=UP * 0.15), FadeIn(tag_me), run_time=0.5)
        self.sub_in("我做了个数学视频号，3000 粉。")
        self.wait(1.5)

        # 拍2 某个万粉博主，拿手机在 QQ 群里发题
        big = man(1.05, "stand").move_to([-2.5, -0.35, 0])
        ph = phone(0.95).move_to([-1.78, -0.70, 0])
        arm = Line([-2.5, 0.15, 0], [-1.82, -0.18, 0]).set_stroke(INK, 2.6)
        tag_big = pill("某个万粉数学博主", RED, RED, fs=25)
        tag_big.next_to(big, UP, buff=0.32)
        grp = VGroup(*[man(0.58, "stand").move_to([x, -0.75, 0])
                       for x in [1.45, 2.30, 3.15, 4.00]])
        gtag = pill("QQ 群", GRAY, "#7A726A", fs=23).move_to([2.72, -1.8, 0])
        self.reg(big, ph, arm, tag_big, grp, gtag)
        self.play(FadeIn(big), FadeIn(arm), FadeIn(ph), FadeIn(tag_big), run_time=0.55)
        self.play(LaggedStart(*[FadeIn(c) for c in grp], lag_ratio=0.12),
                  FadeIn(gtag), run_time=0.7)
        self.sub_in("前不久，某个万粉数学博主，在 QQ 群里发了一道题。")
        self.wait(1.5)

        # 题目气泡从手机飞进群里
        bub0 = bubble(r"x^{2}+y^{2}+\tfrac{1}{x^{2}}+\tfrac{1}{y^{2}}\ \ge\ \tfrac{17}{2}",
                      fs=26, h=0.95)
        bub0.move_to([-1.78, 0.80, 0])
        self.reg(bub0)
        self.play(FadeIn(bub0, scale=1.1), run_time=0.35)
        self.play(bub0.animate.move_to([1.90, 1.15, 0]), run_time=0.75)
        self.wait(1.0)

        # 拍3 我举手，把解法发出去
        me2 = man(0.95, "raised").move_to(me.get_center())
        bub = cbox(r"\frac{1}{16x^{2}}", BLUE, CFB, w=1.7, h=0.8, fs=32)
        bub.move_to(me.get_center() + RIGHT * 1.2 + UP * 0.85)
        self.reg(bub)
        self.play(Transform(me, me2), run_time=0.28)
        self.play(FadeIn(bub, scale=1.2), run_time=0.3)
        self.play(bub.animate.move_to([5.5, 0.6, 0]), run_time=0.7)
        self.sub_in("我在群里把解法发了出去。")
        self.wait(1.3)

        # 拍4 围观
        self.play(me.animate.move_to([-5.0, -0.4, 0]),
                  tag_me.animate.shift(RIGHT * 1.1), run_time=0.5)
        ctr = np.array([-5.0, -0.4, 0])
        ring = VGroup()
        for i in range(12):
            a = TAU * i / 12 + 0.26
            ring.add(man(0.6, "stand").move_to(
                ctr + np.array([2.15 * np.cos(a), 1.30 * np.sin(a), 0])))
        bangs = VGroup()
        for i in range(8):
            a = TAU * i / 8 + 0.5
            b = ST("!", fs=38, color=RED)
            b.move_to(ctr + np.array([2.75 * np.cos(a), 1.75 * np.sin(a), 0]))
            bangs.add(b)
        self.reg(ring, bangs)
        self.play(LaggedStart(*[FadeIn(r) for r in ring], lag_ratio=0.06), run_time=0.9)
        self.play(LaggedStart(*[FadeIn(b, shift=b.get_center() * -0.22) for b in bangs],
                              lag_ratio=0.06), run_time=0.7)
        self.play(me.animate.scale(0.85), run_time=0.3)
        self.sub_in("然后，我遭遇了一场网暴。")
        self.wait(1.4)

        # 拍5 印章
        self.play(*[FadeOut(m) for m in [big, ph, arm, tag_big, grp, gtag, bub0, bub]],
                  run_time=0.25)
        self.unreg(big, ph, arm, tag_big, grp, gtag, bub0, bub)
        st = stamp("网暴", RED, fs=64).move_to([0.8, 0.2, 0])
        note = ST("疑似被举报 · 限流 · 下架", fs=30, color=RED, font=HEI)
        note.next_to(st, DOWN, buff=0.45)
        fit(note, 12.0)
        self.reg(st, note)
        self.play(FadeIn(st, scale=1.6), run_time=0.32)
        self.play(FadeIn(note), run_time=0.35)
        self.sub_in("疑似被举报、限流、下架。")
        self.wait(1.9)
        self.wipe()

    # ---------------- 2 那到底是一道什么题 ----------------
    def s2_problem(self):
        self.wipe()
        self.chapter(2)
        self.sec("就是这道题", y=3.5)
        card = cbox(r"x^{2}+y^{2}+\frac{1}{x^{2}}+\frac{1}{y^{2}}\ \ge\ \frac{17}{2}",
                    INK, WHITE, w=10.6, h=1.5, fs=54, pad=0.6)
        card.move_to([0, 1.30, 0])
        prem = MathTex(r"x,y>0,\qquad x+y=1", font_size=42, color=BLUE)
        prem.next_to(card, UP, buff=0.4)
        self.reg(card, prem)
        self.play(FadeIn(prem, lag_ratio=0.06), run_time=0.4)
        self.play(FadeIn(card, scale=0.93), run_time=0.55)
        self.sub_in("这是「基本不等式」这一章，章节测试里会出现的题。")
        self.wait(1.5)

        tag = pill("基本不等式 · 章节测试题", GOLD, "#8A6A20", fs=27)
        tag.next_to(card, DOWN, buff=0.5)
        self.reg(tag)
        self.play(FadeIn(tag), run_time=0.35)
        self.play(Indicate(tag, color=GOLD, scale_factor=1.06), run_time=0.6)
        self.sub_in("这样的题，我本人就做过类似的。它不是什么大学题。")
        self.wait(1.8)
        self.wipe()

    # ---------------- 3 他的解法：求导 ----------------
    def s3_deriv(self):
        self.wipe()
        self.chapter(3)
        self.sec("他的做法：求导", y=3.55, color=RED)
        ax = Axes(x_range=[0.25, 0.75, 0.1], y_range=[8, 20, 2],
                  x_length=9.6, y_length=4.2,
                  axis_config={"color": "#C9BFB2", "stroke_width": 2.2}, tips=False)
        ax.move_to([-0.6, -0.5, 0])
        curve = ax.plot(lambda x: x ** 2 + (1 - x) ** 2 + 1 / x ** 2 + 1 / (1 - x) ** 2,
                        x_range=[0.25, 0.75, 0.004], color=BLUE, stroke_width=4)
        dot = Dot(ax.c2p(0.5, 8.5), color=RED, radius=0.1)
        tan = Line(ax.c2p(0.34, 8.5), ax.c2p(0.66, 8.5)).set_stroke(GOLD, 3.2)
        vlab = MathTex(r"x=\tfrac{1}{2}", font_size=40, color=RED)
        vlab.next_to(dot, UR, buff=0.26)
        self.reg(ax, curve, dot, tan, vlab)          # curve 必须登记，否则永久残影
        self.play(Create(ax), run_time=0.6)
        self.play(Create(curve), run_time=1.2)
        self.sub_in("设出 f(x)，令 f'(x)=0，解出 x=1/2。")
        self.play(FadeIn(dot, scale=1.4), run_time=0.3)
        self.play(Create(tan), FadeIn(vlab), run_time=0.5)

        fml = MathTex(r"f(x)=x^{2}+(1-x)^{2}+\frac{1}{x^{2}}+\frac{1}{(1-x)^{2}}",
                      font_size=38, color=INK)
        fml.move_to([0.0, -2.95, 0])
        fit(fml, 11.5)
        self.reg(fml)
        self.play(FadeIn(fml), run_time=0.45)
        warn = pill("需要高二以上", GRAY, "#7A726A", fs=25).to_corner(UR, buff=0.7)
        self.reg(warn)
        self.play(FadeIn(warn), run_time=0.3)
        self.wait(1.3)

        val = DecimalNumber(0, num_decimal_places=1, font_size=48, color=RED)
        val.move_to([5.4, -1.5, 0])
        tr = ValueTracker(0)
        val.add_updater(lambda m: m.set_value(tr.get_value() * 8.5))
        self.reg(val)
        self.play(FadeIn(val), run_time=0.2)
        self.play(tr.animate.set_value(1), run_time=1.0)
        val.clear_updaters()
        self.play(Transform(val, MathTex(r"\frac{17}{2}", font_size=56, color=RED)
                            .move_to(val.get_center())), run_time=0.45)
        self.sub_in("最小值就是 17/2。")
        self.wait(1.4)
        self.wipe()

    # ---------------- 4 我的解法：拆项 + 基本不等式 ----------------
    def s4_amgm(self):
        self.wipe()
        self.chapter(4)
        self.sec("我的做法：拆项 + 基本不等式", y=3.6, color=BLUE)

        st0 = MathTex(r"\frac{1}{x^{2}}=\frac{1}{16x^{2}}+\frac{15}{16}\cdot\frac{1}{x^{2}}",
                      font_size=50, color=INK)
        st0.move_to([0, 2.35, 0])
        fit(st0, 10.5)
        lab0 = ST("把 1/x² 拆成两项", fs=30, color=BLUE, font=HEI)
        lab0.next_to(st0, LEFT, buff=0.55)
        self.reg(st0, lab0)
        self.play(FadeIn(lab0, lag_ratio=0.05), FadeIn(st0, scale=1.06), run_time=0.6)
        self.sub_in("把 1/x² 拆成 1/(16x²) 和 15/(16x²)。")
        self.wait(1.5)

        self.play(FadeOut(lab0), FadeOut(st0), run_time=0.25)
        self.unreg(lab0, st0)

        b_a = cbox(r"x^{2}+\frac{1}{16x^{2}}", BLUE, CFB, w=4.1, h=1.1, fs=38)
        b_b = cbox(r"y^{2}+\frac{1}{16y^{2}}", GREEN, CFG, w=4.1, h=1.1, fs=38)
        b_c = cbox(r"\frac{15}{16}\Big(\frac{1}{x^{2}}+\frac{1}{y^{2}}\Big)",
                   PURPLE, CFP, w=5.0, h=1.1, fs=38)
        row = VGroup(b_a, b_b, b_c).arrange(RIGHT, buff=0.35)
        row.move_to([0, 1.5, 0])
        fit(row, 13.8)
        self.reg(row)
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.18) for x in [b_a, b_b, b_c]],
                              lag_ratio=0.18), run_time=0.9)
        self.sub_in("两项配基本不等式，剩下一项用权方和收掉。")
        self.wait(1.3)

        r1 = cbox(r"\ge\ 2\sqrt{\frac{1}{16}}=\frac{1}{2}", BLUE, CFB, w=4.1, h=0.95, fs=38)
        r2 = cbox(r"\ge\ \frac{1}{2}", GREEN, CFG, w=4.1, h=0.95, fs=38)
        r3 = cbox(r"\ge\ \frac{15}{16}\cdot 8=\frac{15}{2}", PURPLE, CFP, w=5.0, h=0.95, fs=38)
        row2 = VGroup(r1, r2, r3)
        for i, host in enumerate([b_a, b_b, b_c]):
            row2[i].move_to([host.get_center()[0], -0.15, 0])
        self.reg(row2)
        self.play(LaggedStart(*[FadeIn(x, shift=DOWN * 0.15) for x in row2],
                              lag_ratio=0.18), run_time=0.9)
        kf = MathTex(r"\frac{1^{3}}{x^{2}}+\frac{1^{3}}{y^{2}}\ \ge\ "
                     r"\frac{(1+1)^{3}}{(x+y)^{2}}=\frac{8}{(x+y)^{2}}=8",
                     font_size=36, color="#8A8078")
        kf.move_to([0, -1.8, 0])
        fit(kf, 11.0)
        self.reg(kf)
        self.play(FadeIn(kf), run_time=0.45)
        self.sub_in("第三项用权方和：1/x² + 1/y² ≥ 8。")
        self.wait(1.7)

        self.play(FadeOut(kf), run_time=0.2)
        self.unreg(kf)
        self.play(*[FadeOut(m) for m in [row, row2]], run_time=0.25)
        self.unreg(row, row2)

        tot = MathTex(r"\frac{1}{2}+\frac{1}{2}+\frac{15}{2}=", font_size=58, color=INK)
        res = bigval(r"\frac{17}{2}", GOLD, fs=94)
        line = VGroup(tot, res).arrange(RIGHT, buff=0.5).move_to([0, 0.4, 0])
        fit(line, 13.0)
        self.reg(line)
        self.play(FadeIn(tot), run_time=0.5)
        self.play(FadeIn(res, scale=1.25),
                  Flash(res[1], color=GOLD, line_length=0.55, num_lines=16,
                        flash_radius=1.5),
                  run_time=0.7)
        self.sub_in("加起来刚好是 17/2。等号在 x=y=1/2 取到。")
        self.wait(2.0)
        self.wipe()

    # ---------------- 5 1/16 哪来的 + Jensen ----------------
    def s5_source(self):
        self.wipe()
        self.chapter(5)
        self.sec("那个 1/16，是哪来的？", y=3.6, color=GOLD)

        chain = [
            MathTex(r"x=\frac{1}{2}", font_size=46, color=INK),
            MathTex(r"x^{2}=\frac{1}{4}", font_size=46, color=INK),
            MathTex(r"\sqrt{t}=x^{2}=\frac{1}{4}", font_size=46, color=INK),
            MathTex(r"t=\frac{1}{16}", font_size=54, color=GOLD),
        ]
        g = VGroup()
        for i, m in enumerate(chain):
            g.add(m)
            if i < len(chain) - 1:
                g.add(arrow([0, 0, 0], [0, -0.5, 0], color=GOLD, sw=2.4))
        g.arrange(DOWN, buff=0.14)
        g.move_to([-3.9, 0.05, 0])
        self.reg(g)
        self.play(LaggedStart(*[FadeIn(x) for x in g], lag_ratio=0.2), run_time=2.0)

        note = ST("要让等号落在 x = 1/2，\n只能解出 t = 1/16。\n\n这是设计出来的。",
                  fs=36, color=INK, ls=1.35)
        fit(note, 6.2)
        note.move_to([3.3, 0.15, 0])
        self.reg(note)
        self.play(FadeIn(note, lag_ratio=0.06), run_time=0.8)
        self.sub_in("那个 1/16 不是猜的，是从等号条件倒推出来的。")
        self.wait(2.2)

        self.wipe()
        self.chapter(5)
        self.sec("还有一个更短的写法", y=3.6, color=PURPLE)
        j1 = MathTex(r"f(t)=t^{2}+\frac{1}{t^{2}},\qquad f''(t)=2+\frac{6}{t^{4}}>0",
                     font_size=44, color=INK)
        j1.move_to([0, 1.9, 0])
        fit(j1, 11.5)
        cvx = ST("f 是凸函数", fs=32, color=PURPLE, font=HEI)
        cvx.move_to([0, 1.0, 0])
        j2 = MathTex(r"f(x)+f(y)\ \ge\ 2f\Big(\frac{x+y}{2}\Big)=2f\Big(\frac{1}{2}\Big)"
                     r"=2\Big(\frac{1}{4}+4\Big)=\frac{17}{2}",
                     font_size=44, color=PURPLE)
        j2.move_to([0, -0.25, 0])
        fit(j2, 13.0)
        self.reg(j1, j2, cvx)
        self.play(FadeIn(j1), run_time=0.5)
        self.play(FadeIn(cvx), run_time=0.3)
        self.sub_in("f(t)=t²+1/t² 是凸函数，它的一行写法就是这样的。")
        self.play(FadeIn(j2, lag_ratio=0.05), run_time=0.8)
        self.wait(2.2)
        self.wipe()

    # ---------------- 6 三条路，同一个答案 ----------------
    def s6_paths(self):
        self.wipe()
        self.chapter(6)
        t = MathTex(r"x^{2}+y^{2}+\frac{1}{x^{2}}+\frac{1}{y^{2}}\ge\frac{17}{2}",
                    font_size=44, color=INK)
        t.move_to([0, 3.4, 0])
        fit(t, 11.5)
        self.reg(t)
        self.play(FadeIn(t), run_time=0.4)

        labels = [("求导", RED, 2.3), ("拆项 + 基本不等式", BLUE, 0.4), ("Jensen 凸性", PURPLE, -1.5)]
        paths = VGroup()
        for name, col, y0 in labels:
            lb = pill(name, col, col, fs=30).move_to([-4.6, y0, 0])
            self.reg(lb)
            p = VMobject().set_points_as_corners([[-2.3, y0, 0], [-0.9, y0, 0], [1.2, 0.4, 0]])
            p.set_stroke(col, 4.5)
            paths.add(p)
            self.play(FadeIn(lb), run_time=0.28)
            self.play(Create(p), run_time=0.5)
        self.reg(paths)
        goal = bigval(r"\frac{17}{2}", GOLD, fs=86).move_to([3.4, 0.4, 0])
        self.reg(goal)
        self.play(FadeIn(goal, scale=1.2),
                  Flash(goal[1], color=GOLD, line_length=0.5, num_lines=14,
                        flash_radius=1.4),
                  run_time=0.6)
        self.sub_in("三种完全不同的思路，都落到同一个 17/2。")
        self.wait(2.0)
        self.wipe()

    # ---------------- 7 转折：手写解法 → 私发动画 → 举报下架 ----------------
    def s7_takedown(self):
        self.wipe()
        self.chapter(7)

        # 拍1 手写解法发在群里，他们说挺好（视频没在群里宣传过）
        paper = RoundedRectangle(corner_radius=0.1, width=4.3, height=2.8)
        paper.set_stroke(INK, 2.4).set_fill(WHITE, 0.97).move_to([-0.5, 0.6, 0])
        sol = MathTex(r"x^{2}+y^{2}+\tfrac{1}{x^{2}}+\tfrac{1}{y^{2}}\ \ge\ \tfrac{17}{2}",
                      font_size=34, color=INK)
        fit(sol, 3.7)
        sol.move_to(paper.get_center() + UP * 0.55)
        hlines = VGroup(*[Line([0, 0, 0], [w, 0, 0]).set_stroke("#9A9088", 2.0)
                          for w in [2.9, 3.3, 2.1]])
        hlines.arrange(DOWN, aligned_edge=LEFT, buff=0.30)
        hlines.move_to(paper.get_center() + DOWN * 0.62)
        ptag = pill("手写解法 · 发在群里", GRAY, INK, fs=24)
        ptag.move_to(paper.get_center() + DOWN * 1.80)
        parchment = VGroup(paper, sol, hlines, ptag)
        self.reg(parchment)
        self.play(FadeIn(parchment, scale=0.95), run_time=0.5)
        self.sub_in("我把手写的解法发在群里。他们说，挺好。")
        self.wait(1.1)

        ok = pill("挺好", GREEN, GREEN, fs=26).move_to([3.4, 1.9, 0])
        self.reg(ok)
        self.play(FadeIn(ok, scale=1.2), run_time=0.3)
        self.wait(0.9)
        self.play(FadeOut(parchment), FadeOut(ok), run_time=0.3)
        self.unreg(parchment, ok)

        # 拍2 第二天，把题做成动画私发给他
        card = RoundedRectangle(corner_radius=0.16, width=6.2, height=3.5)
        card.set_stroke(INK, 2.6).set_fill(WHITE, 0.95)
        play = Triangle(color=BLUE, stroke_width=0).set_fill(BLUE, 1).scale(0.42)
        play.rotate(-PI / 2).move_to(card.get_center())
        vcard = VGroup(card, play).move_to([0, 0.35, 0])
        self.reg(vcard)
        self.play(FadeIn(vcard, scale=0.94), run_time=0.5)
        self.sub_in("第二天，我把昨天一起讨论的题做成了动画，私发给他。")
        self.wait(1.4)

        # 拍3 等来的却是抄袭指控 + 侮辱嘲讽
        acc = stamp("抄袭指控", RED, fs=50).move_to([0, 0.35, 0])
        self.reg(acc)
        self.play(FadeIn(acc, scale=1.7), run_time=0.35)
        self.sub_in("等来的却是抄袭的指控，还有侮辱、谩骂，和满带优越感的嘲讽。")
        self.wait(1.7)
        self.play(FadeOut(acc), run_time=0.25)
        self.unreg(acc)

        # 拍4 视频被举报、限流、下架
        st = stamp("限流 / 下架", RED, fs=54).move_to([0, 0.35, 0])
        self.reg(st)
        self.play(FadeIn(st, scale=1.7), run_time=0.35)
        self.sub_in("疑似被他们举报、限流、下架。")        # 与印章同拍切换，避免字幕错位
        self.wait(0.6)

        frags = VGroup()
        for i in range(9):
            f = Rectangle(width=0.9, height=0.7).set_stroke(GRAY, 1.5).set_fill("#EDE7DF", 1)
            f.move_to(card.get_center() + np.array([np.random.uniform(-2.6, 2.6),
                                                    np.random.uniform(-1.5, 1.5), 0]))
            frags.add(f)
        self.play(FadeOut(vcard), FadeOut(st), run_time=0.3)
        self.unreg(vcard, st)
        self.reg(frags)
        self.play(LaggedStart(*[FadeIn(f) for f in frags], lag_ratio=0.05), run_time=0.5)
        self.play(LaggedStart(*[f.animate.shift(DOWN * 1.6 +
                                                RIGHT * np.random.uniform(-1, 1)).set_opacity(0)
                                for f in frags], lag_ratio=0.05), run_time=0.8)
        self.wait(1.2)
        caveat = ST("＊举报人的身份我无法确认；但群里的言语攻击、视频被限流下架，都是真的。",
                    fs=26, color="#8A8078", font=HEI, weight=NORMAL)
        fit(caveat, 13.4)
        caveat.move_to([0, -1.7, 0])
        self.reg(caveat)
        self.play(FadeIn(caveat, lag_ratio=0.04), run_time=0.55)
        self.wait(2.3)
        self.wipe()

    # ---------------- 8 指控一：抄袭 ----------------
    def s8_plagiarism(self):
        self.wipe()
        self.chapter(8)
        st = stamp("抄袭？", RED, fs=56).move_to([0, 1.5, 0])
        self.reg(st)
        self.play(FadeIn(st, scale=1.6), run_time=0.32)
        self.sub_in("第一个指控是抄袭，理由是我在群里看到了别人问的题。")
        self.wait(1.4)

        q = MathTex(r"x+y=1\ \Longrightarrow\ x^{2}+y^{2}+\frac{1}{x^{2}}+\frac{1}{y^{2}}"
                    r"\ge\frac{17}{2}", font_size=42, color=INK)
        q.move_to([0, -0.2, 0])
        fit(q, 11.5)
        self.reg(q)
        self.play(FadeIn(q), run_time=0.4)
        self.play(st.animate.scale(0.7).move_to([-5.0, 2.75, 0]), run_time=0.4)

        names = [("求导", RED, -4.2), ("基本不等式", BLUE, 0.0), ("Jensen", PURPLE, 4.2)]
        links = VGroup()
        for name, col, x0 in names:
            lb = pill(name, col, col, fs=28).move_to([x0, -1.55, 0])
            self.reg(lb)
            p = VMobject().set_points_as_corners([[x0, -0.68, 0], [x0, -1.18, 0]])
            p.set_stroke(col, 3.5)
            links.add(p)
            self.play(Create(p), FadeIn(lb), run_time=0.35)
            bx = cbox(r"\frac{17}{2}", col, WHITE, w=1.7, h=0.85, fs=34)
            bx.move_to([x0, -2.65, 0])
            self.reg(bx)
            self.play(FadeIn(bx), run_time=0.3)
        self.reg(links)                              # 连接线也要登记
        self.sub_in("题目是他自己发在 QQ 群里求解答的；同一个不等式，本来就有无数种证法。")
        self.wait(1.5)

        big = ST("谁抄谁？", fs=62, color=RED).move_to([0, 2.4, 0])
        self.reg(big)
        self.play(FadeIn(big, lag_ratio=0.08), run_time=0.6)
        self.sub_in("求导能到 17/2，基本不等式能到 17/2，凸函数也能到 17/2——谁抄谁？")
        self.wait(2.0)
        self.wipe()

    # ---------------- 9 指控二：AI 写的 ----------------
    def s9_ai(self):
        self.wipe()
        self.chapter(9)
        st = stamp("代码是 AI 写的？", RED, fs=44).move_to([0, 3.3, 0])
        self.reg(st)
        self.play(FadeIn(st, scale=1.5), run_time=0.32)
        self.sub_in("第二个指控是：动画代码是 AI 写的，所以这不算我的东西。")
        self.wait(1.4)

        code = VGroup()
        for i in range(13):
            w = np.random.uniform(2.0, 5.2)
            code.add(Line([0, 0, 0], [w, 0, 0]).set_stroke("#B9B0A6", 2.2))
        code.arrange(DOWN, aligned_edge=LEFT, buff=0.17).move_to([-1.2, 0.85, 0])
        self.reg(code)
        self.play(LaggedStart(*[FadeIn(c) for c in code], lag_ratio=0.05), run_time=0.7)
        self.wait(0.3)

        pen = Line([0, 0.34, 0], [0, -0.34, 0]).set_stroke(INK, 3.2)
        tip = Triangle(color=INK, stroke_width=0).set_fill(INK, 1).scale(0.16)
        tip.rotate(PI).move_to([0, -0.34, 0])
        pen.add(tip)
        pen.move_to([-3.6, -1.95, 0])
        calc = RoundedRectangle(corner_radius=0.1, width=0.9, height=1.15)
        calc.set_stroke(INK, 2.6).set_fill(WHITE, 1).move_to([-0.2, -1.95, 0])
        ruler = Rectangle(width=1.5, height=0.28).set_stroke(INK, 2.6).set_fill(WHITE, 1)
        ruler.move_to([3.2, -1.95, 0])
        tools = VGroup(pen, calc, ruler)
        self.reg(tools)
        self.play(FadeOut(code), run_time=0.3)
        self.unreg(code)
        self.play(LaggedStart(*[FadeIn(t, scale=1.2) for t in tools], lag_ratio=0.15),
                  run_time=0.7)
        lab = pill("笔 · 计算器 · 排版尺", GRAY, INK, fs=28).move_to([0, -2.95, 0])
        self.reg(lab)
        self.play(FadeIn(lab), run_time=0.3)
        self.wait(1.5)

        self.play(FadeOut(tools), FadeOut(lab), run_time=0.25)
        self.unreg(tools, lab)
        mini = VGroup(
            MathTex(r"x=\tfrac{1}{2}", font_size=40, color=INK),
            MathTex(r"\Rightarrow\ t=\tfrac{1}{16}", font_size=44, color=GOLD),
        ).arrange(RIGHT, buff=0.35).move_to([0, 0.75, 0])
        self.reg(mini)
        self.play(FadeIn(mini), run_time=0.45)
        big = ST("AI 猜不出 1/16。\n它是从等号条件倒推出来的。", fs=46, color=INK, ls=1.3)
        fit(big, 12.5)
        big.move_to([0, -1.35, 0])
        self.reg(big)
        self.play(FadeIn(big, lag_ratio=0.06), run_time=0.7)
        self.sub_in("AI 帮我把几百行动画代码写出来了。但拆哪一项、拆成多少，是我自己想的。")
        self.wait(2.0)

        self.wipe()
        self.chapter(9)
        self.sec("用 AI 做数学动画，带来了什么", y=3.6, color=BLUE)
        board = RoundedRectangle(corner_radius=0.14, width=4.2, height=2.0)
        board.set_stroke("#6E6A64", 2.6).set_fill(INK, 1).move_to([-4.0, 1.55, 0])
        bf = MathTex(r"\frac{1}{x^{2}}+\frac{1}{y^{2}}\ge 8", font_size=40, color=WHITE)
        bf.move_to(board)
        self.reg(board, bf)
        self.play(FadeIn(board), FadeIn(bf), run_time=0.5)
        self.wait(0.3)

        ax2 = Axes(x_range=[0, 1, 0.25], y_range=[0, 1, 0.25], x_length=4.4, y_length=2.2,
                   axis_config={"color": "#C9BFB2", "stroke_width": 2}, tips=False)
        ax2.move_to([3.0, 1.55, 0])
        fancy = VGroup(ax2)
        for i in range(3):
            fancy.add(ax2.plot(lambda x, i=i: 0.25 + 0.55 * x ** (1 + i) + 0.06 * i,
                               x_range=[0, 1, 0.02],
                               color=[BLUE, GREEN, PURPLE][i], stroke_width=3))
        for i in range(24):
            fancy.add(Dot(radius=0.045, color=GOLD).move_to(
                ax2.c2p(np.random.uniform(0, 1), np.random.uniform(0, 1))))
        self.reg(fancy)
        self.play(FadeOut(board), FadeOut(bf), run_time=0.3)
        self.unreg(board, bf)
        self.play(LaggedStart(*[Create(x) if isinstance(x, (Axes, ParametricFunction))
                                else FadeIn(x) for x in fancy], lag_ratio=0.04),
                  run_time=1.1)
        self.sub_in("同一行公式，变成了看得见的动态过程。")
        self.wait(1.4)

        rows = [("可视化", "把抽象推导变成看得见的画面", BLUE),
                ("效率", "几百行动画代码的时间省下来", GREEN),
                ("观感", "观众看得更明白，看得更舒服", PURPLE)]
        g = VGroup()
        for lab, txt, col in rows:
            g.add(VGroup(pill(lab, col, col, fs=24), ST(txt, fs=32, color=INK))
                  .arrange(RIGHT, buff=0.38))
        g.arrange(DOWN, buff=0.42, aligned_edge=LEFT).move_to([0, -1.35, 0])
        for item in g:
            self.reg(item)
            self.play(FadeIn(item, shift=RIGHT * 0.2), run_time=0.45)
            self.wait(0.12)
        self.sub_in("用 AI 做数学动画，可视化更好、效率更高，观众的观感也更好。")
        self.wait(2.2)
        self.wipe()

    # ---------------- 10 这种题，我顺手就推了 ----------------
    def s10_cheap(self):
        self.wipe()
        self.chapter(10)
        self.sec("什么才真的需要 AI", y=3.6, color=GOLD)

        bar1 = RoundedRectangle(corner_radius=0.1, width=4.0, height=0.8)
        bar1.set_stroke(BLUE, 2.6).set_fill(CFB, 1)
        g1 = VGroup(bar1, ST("这道题", fs=30, color=BLUE).move_to(bar1)).move_to([-4.0, 2.45, 0])

        bar2 = RoundedRectangle(corner_radius=0.1, width=12.0, height=0.8)
        bar2.set_stroke(RED, 2.6).set_fill(CFR, 1)
        l2 = ST("陈计教授《代数不等式》的经典配方 / IMO 级 SOS 配方", fs=28, color=RED)
        fit(l2, 11.4)
        g2 = VGroup(bar2, l2.move_to(bar2)).move_to([0.0, 1.35, 0])

        self.reg(g1, g2)
        self.play(GrowFromEdge(g1, LEFT), run_time=0.45)
        self.play(GrowFromEdge(g2, LEFT), run_time=0.65)
        src = ST("陈计 · 宁波大学数学系教授 · 四届 IMO 国家集训队教练",
                 fs=24, color="#8A8078", font=HEI, weight=NORMAL)
        src.next_to(g2, DOWN, buff=0.26)
        fit(src, 12.0)
        self.reg(src)
        self.play(FadeIn(src), run_time=0.3)

        t1 = pill("取等条件一凑，1/16 到手", BLUE, BLUE, fs=26).move_to([2.4, 2.45, 0])
        self.reg(t1)
        self.play(FadeIn(t1), run_time=0.3)
        self.sub_in("真正值得动用 AI 辅助的，是那种系数长得像乱码的顶级配方。")
        self.wait(1.7)

        mine = ST("这种题，我顺手就推了。犯不着为它花钱。", fs=44, color=INK)
        fit(mine, 12.5)
        mine.move_to([0, -0.7, 0])
        self.reg(mine)
        self.play(FadeIn(mine, lag_ratio=0.06), run_time=0.7)
        self.sub_in("这种题我顺手就推了。真要花 AI 的钱，也不会花在这种地方。")
        self.wait(1.8)

        self.play(FadeOut(g1), FadeOut(g2), FadeOut(src), FadeOut(t1), FadeOut(mine),
                  run_time=0.25)
        self.unreg(g1, g2, src, t1, mine)

        chain = [pill("解法太巧妙", GRAY, INK, fs=28),
                 pill("所以是 AI 写的", GRAY, INK, fs=28),
                 pill("所以该举报", GRAY, INK, fs=28)]
        cg = VGroup()
        for i, c in enumerate(chain):
            cg.add(c)
            if i < 2:
                cg.add(arrow([0, 0, 0], [0.85, 0, 0], color=GRAY, sw=2.4))
        cg.arrange(RIGHT, buff=0.2)
        fit(cg, 12.6)
        cg.move_to([0, -0.85, 0])
        self.reg(cg)
        self.play(LaggedStart(*[FadeIn(x) for x in cg], lag_ratio=0.22), run_time=1.0)
        x1 = Line(cg.get_corner(UL) + LEFT * 0.25, cg.get_corner(DR) + RIGHT * 0.25)
        x2 = Line(cg.get_corner(DL) + LEFT * 0.25, cg.get_corner(UR) + RIGHT * 0.25)
        redx = VGroup(x1, x2).set_stroke(RED, 6)
        self.reg(redx)
        self.play(Create(redx), run_time=0.5)
        alt = ST("照这逻辑：越巧妙的解法，就越不像人。", fs=42, color=RED)
        fit(alt, 12.5)
        alt.move_to([0, -2.5, 0])
        self.reg(alt)
        self.play(FadeIn(alt, lag_ratio=0.06), run_time=0.7)
        self.sub_in("照这个道理，数学史上所有漂亮的证明，是不是都该被举报？")
        self.wait(2.0)
        self.wipe()

    # ---------------- 11 “哗众取宠”？恰恰相反 ----------------
    def s11_highschool(self):
        self.wipe()
        self.chapter(11)
        self.sec("高一，根本还不会求导", y=3.6, color=BLUE)

        def page(title, sub, tag, col, x):
            r = RoundedRectangle(corner_radius=0.12, width=5.2, height=2.6)
            r.set_stroke(col, 2.6).set_fill(WHITE, 0.95)
            t1 = ST(title, fs=30, color=col).move_to(r.get_center() + UP * 0.62)
            t2 = ST(sub, fs=34, color=INK).move_to(r.get_center() + DOWN * 0.12)
            p = pill(tag, col, col, fs=28).move_to(r.get_center() + DOWN * 0.95)
            fit(t1, 4.7)
            fit(t2, 4.7)
            return VGroup(r, t1, t2, p).move_to([x, 0.8, 0])

        pg1 = page("必修第一册 · 2.2", "基本不等式", "高一", BLUE, -3.5)
        pg2 = page("选择性必修第二册", "导数及其应用", "高二", RED, 3.5)
        self.reg(pg1, pg2)
        self.play(FadeIn(pg1, shift=UP * 0.2), run_time=0.5)
        self.play(FadeIn(pg2, shift=UP * 0.2), run_time=0.5)
        conc = ST("高一没有导数。", fs=52, color=RED).move_to([0, -2.5, 0])
        self.reg(conc)
        self.play(FadeIn(conc, lag_ratio=0.08), run_time=0.7)
        self.sub_in("基本不等式是必修一的内容，导数要到选择性必修第二册。")
        self.wait(1.9)

        # 唯一的路
        self.wipe()
        self.chapter(11)
        self.sec("对高一学生，基本不等式不是一种选择", y=3.6, color=BLUE)
        left = pill("基本不等式 —— 唯一的路", GREEN, GREEN, fs=32).move_to([-3.6, 0.9, 0])
        right = pill("求导", GRAY, GRAY, fs=32).move_to([3.6, 0.9, 0])
        seals = ST("未学", fs=30, color="#7A726A").move_to(right).rotate(-0.1)
        pp = VMobject().set_points_as_corners([[-3.6, -0.05, 0], [-3.6, 0.5, 0]])
        pp.set_stroke(GREEN, 4)
        pp2 = VMobject().set_points_as_corners([[3.6, -0.05, 0], [3.6, 0.5, 0]])
        pp2.set_stroke(GRAY, 4)
        self.reg(left, right, seals, pp, pp2)
        self.play(Create(pp), FadeIn(left), run_time=0.5)
        self.play(Create(pp2), FadeIn(right), run_time=0.5)
        self.play(FadeIn(seals, scale=1.5), run_time=0.3)
        msg = ST("让高一学生看得懂，这叫适配，不叫炫技。", fs=42, color=INK)
        fit(msg, 12.5)
        msg.move_to([0, -1.6, 0])
        self.reg(msg)
        self.play(FadeIn(msg, lag_ratio=0.05), run_time=0.7)
        self.sub_in("他们说配凑是哗众取宠。可那是对高一唯一可用的工具。")
        self.wait(2.0)

        # 严格性对比
        self.wipe()
        self.chapter(11)
        self.sec("真论严格，配凑这一路反而更干净", y=3.6, color=GOLD)
        row1 = cbox(r"(a-b)^{2}\ge 0\ \Longrightarrow\ \frac{a+b}{2}\ge\sqrt{ab}",
                    GOLD, CFGOLD, w=8.6, h=1.25, fs=42)
        row1.move_to([-1.6, 1.4, 0])
        tag1 = pill("展开即得 · 彻底闭环", GOLD, "#8A6A20", fs=26).move_to([5.05, 1.4, 0])
        self.reg(row1, tag1)
        self.play(FadeIn(row1, shift=RIGHT * 0.2), FadeIn(tag1), run_time=0.6)

        row2 = RoundedRectangle(corner_radius=0.14, width=8.6, height=1.25)
        row2.set_stroke(GRAY, 2.4).set_fill("#F4F1EC", 1).move_to([-1.6, -0.55, 0])
        t2t = ST("高中里的导数：直观引入", fs=34, color="#7A726A").move_to(row2)
        g2 = VGroup(row2, t2t)
        tag2 = pill("严格化要到数学分析", GRAY, "#7A726A", fs=26).move_to([5.05, -0.55, 0])
        self.reg(g2, tag2)
        self.play(FadeIn(g2, shift=RIGHT * 0.2), FadeIn(tag2), run_time=0.6)
        bl = ST("基本不等式只需 (a−b)² ≥ 0，展开就完了。", fs=38, color=INK)
        fit(bl, 12.8)
        bl.move_to([0, -2.3, 0])
        self.reg(bl)
        self.play(FadeIn(bl, lag_ratio=0.05), run_time=0.6)
        self.sub_in("导数依赖的极限，在高中只是直观描述。配凑那一路，是彻底闭环的。")
        self.wait(2.1)

        # 回到题目
        self.wipe()
        self.chapter(11)
        self.sec("这哪里是什么大学题", y=3.6, color=RED)
        q = cbox(r"x+y=1\ \Longrightarrow\ x^{2}+y^{2}+\frac{1}{x^{2}}+\frac{1}{y^{2}}"
                 r"\ge\frac{17}{2}", INK, WHITE, w=11.6, h=1.5, fs=42, pad=0.6)
        q.move_to([0, 1.85, 0])
        self.reg(q)
        self.play(FadeIn(q, scale=0.94), run_time=0.5)

        pts = [("用到的工具", "只有基本不等式，没有一步超出高一", GREEN),
               ("等号条件", "x = y = 1/2，1/16 一凑就出来", BLUE),
               ("题目定位", "「基本不等式」章节测试题的难度", GOLD)]
        g = VGroup()
        for lab, txt, col in pts:
            g.add(VGroup(pill(lab, col, col, fs=24), ST(txt, fs=32, color=INK))
                  .arrange(RIGHT, buff=0.38))
        g.arrange(DOWN, buff=0.42, aligned_edge=LEFT).move_to([0, -0.35, 0])
        for item in g:
            self.reg(item)
            self.play(FadeIn(item, shift=RIGHT * 0.2), run_time=0.45)
            self.wait(0.12)
        self.sub_in("这本来就是给高中生做的题。把它说成大学题，只能说没见过几道。")
        self.wait(2.2)
        self.wipe()

    # ---------------- 12 豆包 ----------------
    def s12_doubao(self):
        self.wipe()
        self.chapter(12)
        board = RoundedRectangle(corner_radius=0.14, width=6.6, height=1.5)
        board.set_stroke(GOLD, 3.4).set_fill(CFGOLD, 1).move_to([0, 1.75, 0])
        bt = ST("在校大学生 · 免费领 3 个月会员", fs=38, color="#8A6A20").move_to(board)
        fit(bt, 6.2)
        g = VGroup(board, bt)
        self.reg(g)
        self.play(FadeIn(g, scale=1.12), run_time=0.5)
        self.sub_in("我替豆包说了句话：它给在校大学生免费送三个月会员，原价 68 一个月。")
        self.wait(1.7)

        stu = man(1.0, "raised").move_to([-2.4, -1.1, 0])
        sparks = VGroup(star([-3.0, 0.35, 0]), star([-2.4, 0.58, 0]), star([-1.8, 0.35, 0]))
        self.reg(stu, sparks)
        self.play(FadeIn(stu), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(s, scale=1.6) for s in sparks], lag_ratio=0.15),
                  run_time=0.5)
        self.sub_in("我觉得，这是件好事。")
        self.wait(1.3)

        grp = VGroup(*[man(0.72, "stand").move_to([x, -1.25, 0])
                       for x in [1.1, 2.0, 2.9, 3.8]])
        self.reg(grp)
        self.play(LaggedStart(*[FadeIn(c) for c in grp], lag_ratio=0.12), run_time=0.6)
        self.play(*[c.animate.shift(LEFT * 0.8) for c in grp],
                  stu.animate.scale(0.85), run_time=0.5)
        self.sub_in("然后，我也被骂了。")
        self.wait(1.7)
        self.wipe()

    # ---------------- 13 自证陷阱 ----------------
    def s13_trap(self):
        self.wipe()
        self.chapter(13)
        self.sec("自证陷阱", y=3.6, color=PURPLE)
        me = man(1.05, "stand").move_to([0, -0.3, 0])
        self.reg(me)
        self.play(FadeIn(me), run_time=0.35)
        self.sub_in("被冤枉的时候，人的第一反应是解释。")
        self.wait(1.2)

        rings = []
        for lvl, (r, n, col) in enumerate([(1.7, 2, PURPLE), (2.4, 4, "#A99BEE"),
                                           (3.1, 8, "#C6BCF4")]):
            rg = VGroup()
            for i in range(n):
                a0 = TAU * i / n + 0.14
                a1 = TAU * (i + 1) / n - 0.14
                rg.add(Arc(radius=r, start_angle=a0, angle=(a1 - a0),
                           arc_center=me.get_center()).set_stroke(col, 3.4))
            rings.append(rg)
            self.reg(rg)
            self.play(LaggedStart(*[Create(a) for a in rg], lag_ratio=0.12),
                      run_time=0.55 + 0.15 * lvl)
            self.wait(0.2)

        lab2 = pill("他们说：你看他急了", PURPLE, PURPLE, fs=30).move_to([0, 2.95, 0])
        self.reg(lab2)
        self.play(FadeIn(lab2), run_time=0.35)
        self.sub_in("你解释第一遍，他们问第二遍。你解释第二遍，他们说'你看他急了'。")
        self.wait(1.9)

        self.play(*[FadeOut(r) for r in rings], FadeOut(lab2), run_time=0.5)
        self.unreg(lab2, *rings)
        self.play(me.animate.scale(0.62).move_to([-5.9, -1.5, 0]), run_time=0.45)

        msg = ST("这不是辩论，这叫自证陷阱。", fs=50, color=PURPLE).move_to([0, 1.3, 0])
        msg2 = ST("你越想证明自己，那个洞就越深。", fs=42, color=INK).move_to([0, 0.35, 0])
        self.reg(msg, msg2)
        self.play(FadeIn(msg, lag_ratio=0.06), run_time=0.6)
        self.play(FadeIn(msg2, lag_ratio=0.06), run_time=0.6)
        only = ST("我只澄清这一次。", fs=54, color=RED).move_to([0, -2.2, 0])
        self.reg(only)
        self.play(FadeIn(only, lag_ratio=0.08), run_time=0.7)
        self.wait(2.1)
        self.wipe()

    # ---------------- 14 我的立场 ----------------
    def s14_stance(self):
        self.wipe()
        self.chapter(14)
        self.sec("我的立场", y=3.6, color=INK)

        items = [
            ("我的视频，经得起核查。", "解法原创 · 过程可复现 · 每一步都能验算", GREEN),
            ("但我不需要靠它自证。", "我不会为一句我没错的话反复道歉", BLUE),
            ("所以，我只把话说清楚。", "不复述、不逐条回应、不陪你玩", GOLD),
        ]
        g = VGroup()
        for a, b, col in items:
            t1 = ST(a, fs=42, color=col)
            t2 = ST(b, fs=27, color="#8A8078", font=HEI, weight=NORMAL)
            fit(t1, 11.0)
            fit(t2, 11.0)
            box = VGroup(t1, t2).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
            dot = Circle(radius=0.12, color=col, stroke_width=3).set_fill(col, 1)
            dot.next_to(box, LEFT, buff=0.45)
            g.add(VGroup(dot, box))
        g.arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to([0, 0.3, 0])
        for item in g:
            self.reg(item)
            self.play(FadeIn(item, shift=RIGHT * 0.2), run_time=0.55)
            self.wait(0.3)
        self.sub_in("我的视频经得起核查；但我不需要靠它来证明我自己。我只把话说清楚，这一次。")
        self.wait(2.4)
        self.wipe()

    # ---------------- 15 给同行的一句话 ----------------
    def s15_advice(self):
        self.wipe()
        self.chapter(15)
        self.sec("想对同行的数学博主说一句", y=3.6, color=INK)

        ped = RoundedRectangle(corner_radius=0.1, width=3.6, height=0.55)
        ped.set_stroke(GRAY, 2.4).set_fill("#EFEBE5", 1).move_to([-3.9, -0.6, 0])
        pl = ST("道德高地", fs=27, color="#8A8078", font=HEI, weight=NORMAL).move_to(ped)
        b1 = man(1.0, "point").move_to([-3.9, 0.4, 0])
        follower = man(0.7, "stand").move_to([-2.5, -1.3, 0])
        left = VGroup(ped, pl, b1, follower)
        self.reg(left)
        self.play(FadeIn(left, lag_ratio=0.12), run_time=0.7)

        desk = Rectangle(width=3.2, height=0.22).set_stroke(INK, 2.4).set_fill(WHITE, 1)
        desk.move_to([3.9, -0.9, 0])
        b2 = man(1.0, "stand").move_to([3.5, 0.15, 0])
        mon = RoundedRectangle(corner_radius=0.08, width=1.6, height=1.05)
        mon.set_stroke(INK, 2.4).set_fill(WHITE, 1).move_to([5.35, 0.3, 0])
        gra = VGroup()
        for i in range(3):
            c = ParametricFunction(
                lambda t, i=i: np.array([0.6 * t, 0.3 * t ** (1 + i), 0]),
                t_range=[0, 1, 0.05], color=[BLUE, GREEN, PURPLE][i]).set_stroke(width=2.6)
            c.move_to(mon.get_center() + LEFT * 0.36 + DOWN * 0.08)
            gra.add(c)
        rgt = VGroup(desk, b2, mon, gra)
        self.reg(rgt)
        self.play(FadeIn(rgt, lag_ratio=0.1), run_time=0.7)
        self.sub_in("少站在道德高地上指点别人，多花点时间钻研自己的内容。")
        self.wait(1.7)

        ped_pos = ped.get_center()
        frags = VGroup()
        for i in range(6):
            f = Rectangle(width=0.55, height=0.5).set_stroke(GRAY, 1.4).set_fill("#EFEBE5", 1)
            f.move_to(ped_pos + np.array([-1.25 + 0.5 * i, np.random.uniform(-0.15, 0.15), 0]))
            frags.add(f)
        self.play(FadeOut(left), run_time=0.25)
        self.unreg(left)
        self.reg(frags)
        self.play(FadeIn(frags), run_time=0.25)
        self.play(LaggedStart(*[f.animate.shift(DOWN * 1.5).set_opacity(0) for f in frags],
                              lag_ratio=0.05), run_time=0.7)
        self.play(gra.animate.set_color(GOLD), run_time=0.5)

        msg = ST("把精力放在内容上。", fs=52, color=INK).move_to([0, 2.4, 0])
        self.reg(msg)
        self.play(FadeIn(msg, lag_ratio=0.08), run_time=0.6)
        self.sub_in("粉丝多粉丝少，不代表谁有资格戴着有色眼镜，去打压别人。")
        self.wait(1.8)

        last = ST("何况我读过研，比那些骂我的人年长。这些都不重要——\n粉丝少，也不该被这样对待。",
                  fs=34, color="#8A8078", font=HEI, weight=NORMAL, ls=1.35)
        fit(last, 12.6)
        last.move_to([0, -2.4, 0])
        self.reg(last)
        self.play(FadeIn(last, lag_ratio=0.05), run_time=0.8)
        self.wait(2.2)
        self.wipe()

    # ---------------- 16 落点 ----------------
    def s16_end(self):
        self.wipe()
        self.chapter(16)

        ring = VGroup()
        for i in range(14):
            a = TAU * i / 14 + 0.2
            ring.add(man(0.72, "stand").move_to(
                np.array([5.6 * np.cos(a), 3.0 * np.sin(a), 0])))
        self.reg(ring)
        self.play(LaggedStart(*[FadeIn(r) for r in ring], lag_ratio=0.06), run_time=1.1)

        card = bigval(r"\frac{17}{2}", GOLD, fs=104).move_to([0, 0.15, 0])
        self.reg(card)
        self.play(FadeIn(card, scale=1.15), run_time=0.6)

        movers = VGroup(*[r for i, r in enumerate(ring) if i % 3 == 0])
        self.play(movers.animate.shift(UP * 0.12), run_time=0.4)
        self.play(movers.animate.shift(DOWN * 0.12), run_time=0.4)
        self.sub_in("他们可以继续围着，但 17/2 不会动。")
        self.wait(1.5)

        st = stamp("证明", RED, fs=62).move_to([0, 0.15, 0])
        self.reg(st)
        self.play(FadeIn(st, scale=1.7), run_time=0.35)
        self.sub_in("因为数学这个东西，只认证明。")
        self.wait(1.4)

        self.play(FadeOut(ring), FadeOut(st), FadeOut(card), run_time=0.5)
        self.unreg(ring, st, card)
        gold = ST("数学不认粉丝数，它只认证明。", fs=68, color=INK)
        fit(gold, 15.2)
        gold.move_to([0, 0.3, 0])
        self.reg(gold)
        self.play(FadeIn(gold, lag_ratio=0.1), run_time=1.1)
        self.sub_in("我该说的，说完了。")
        self.wait(2.4)

        fin = ST("嘉豪解法", fs=32, color="#B0A89E", font=HEI, weight=NORMAL)
        fin.to_corner(DR, buff=0.55)
        self.reg(fin)
        self.play(FadeIn(fin), run_time=0.4)
        self.wait(1.2)

    # ---------------- 主流程 ----------------
    def construct(self):
        self.background()
        self.cur = []
        self.sub_mob = None
        np.random.seed(7)

        self.s0_title()
        self.s1_cause()
        self.s2_problem()
        self.s3_deriv()
        self.s4_amgm()
        self.s5_source()
        self.s6_paths()
        self.s7_takedown()
        self.s8_plagiarism()
        self.s9_ai()
        self.s10_cheap()
        self.s11_highschool()
        self.s12_doubao()
        self.s13_trap()
        self.s14_stance()
        self.s15_advice()
        self.s16_end()
