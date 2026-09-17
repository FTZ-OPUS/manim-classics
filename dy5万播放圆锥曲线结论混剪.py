from manim import *
import numpy as np

# ============ 公式混剪·圆锥曲线篇（按 formula-mixcut-animation.md 定稿版） ============
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16.0
config.frame_height = 9.0

ZH_FONT  = "Kaiti SC"
BG       = "#050505"
WALL     = "#3A3F4B"
MUTED    = "#A9B4C2"
PREFIX_C = "#CDDC39"
NAME_GR  = ("#FFD166", "#F59E62")
FORM_GR  = ("#FF8A50", "#FFD166")
SUB1_C   = "#66D19E"
SUB2_C   = "#4DB6AC"
PREFIX   = "圆锥曲线："

T_RUN  = 0.45   # 形变时长（SKILL 定稿：1.03s/卡）
T_HOLD = 0.55   # 停留时长

# ---------- 卡片数据：(标题, 公式LaTeX, 副标题1, 副标题2) ----------
CARDS = [
    ("统一定义", r"\frac{|MF|}{d}=e",
     "e=1 抛物线，e<1 椭圆，e>1 双曲线", "一切从这个比值开始"),
    ("椭圆第一定义", r"|MF_1|+|MF_2|=2a\ \ (2a>2c)",
     "一根绳圈画出的轨迹", "到两定点距离之和"),
    ("椭圆焦半径", r"r_1=a+ex_0,\quad r_2=a-ex_0",
     "左加右减，一加一减", "e = c/a 是离心率"),
    ("焦准距", r"\frac{a^2}{c}-c=\frac{b^2}{c}",
     "焦点到准线的距离", "椭圆双曲线都是它"),
    ("焦点三角形面积", r"S_{\triangle PF_1F_2}=b^2\tan\frac{\theta}{2}",
     "θ 是两条焦半径的夹角", "椭圆专属公式"),
    ("内心横坐标", r"x_I=a",
     "焦点三角形内心的横坐标", "双曲线则切于顶点"),
    ("椭圆中点弦", r"k_{AB}\cdot k_{OM}=-\frac{b^2}{a^2}",
     "点差法一步到位", "O 原点，M 中点"),
    ("最短焦点弦", r"|AB|_{\min}=\frac{2b^2}{a}",
     "通径：垂直于长轴的弦", "最长就是长轴 2a"),
    ("椭圆第三定义", r"k_1k_2=-\frac{b^2}{a^2}",
     "与两顶点连线斜率之积", "第三定义的定值"),
    ("椭圆离心率", r"e=\frac{c}{a}=\sqrt{1-\frac{b^2}{a^2}}",
     "e 越大椭圆越扁", "0 < e < 1"),
    ("焦半径乘积", r"|PF_1|\cdot|PF_2|\le a^2",
     "短轴端点处取最大", "面积公式的伏笔"),
    ("最远最近", r"|PF|_{\max}=a+c,\ \ |PF|_{\min}=a-c",
     "长轴两端点处取到", "到焦点距离的极值"),
    ("双曲线定义", r"\big||MF_1|-|MF_2|\big|=2a\ \ (2a<2c)",
     "距离之差的绝对值", "双曲线第一定义"),
    ("双曲线焦半径", r"r=ex_0-a",
     "右支上的点到右焦点", "距离要先减 a"),
    ("abc 关系对照", r"a^2=b^2+c^2\ \ vs\ \ c^2=a^2+b^2",
     "椭圆 vs 双曲线，别背反", "焦点在哪谁加谁"),
    ("渐近线", r"d(F,\ l)=b",
     "渐近线 y=±(b/a)x", "焦点到渐近线距离 = b"),
    ("焦点三角形·双曲", r"S_{\triangle PF_1F_2}=b^2\cot\frac{\theta}{2}",
     "和椭圆只差一个余切", "tan 变 cot"),
    ("双曲线中点弦", r"k_{AB}\cdot k_{OM}=\frac{b^2}{a^2}",
     "负号变正号", "双曲线点差法"),
    ("双曲线第三定义", r"k_1k_2=\frac{b^2}{a^2}",
     "渐近线是它的极限", "定值为正"),
    ("共轭双曲线", r"\frac{1}{e_1^2}+\frac{1}{e_2^2}=1",
     "实虚轴互换的一对", "离心率的倒数平方和"),
    ("等轴双曲线", r"a=b\ \Longrightarrow\ e=\sqrt{2}",
     "渐近线互相垂直", "离心率是常数"),
    ("抛物线焦半径", r"r=x_0+\frac{p}{2}",
     "准线替你记着距离", "y² = 2px 的福利"),
    ("焦点弦", r"|AB|=\frac{2p}{\sin^2\theta}",
     "θ 为弦的倾斜角", "抛物线焦点弦"),
    ("焦点弦倒数和", r"\frac{1}{|FA|}+\frac{1}{|FB|}=\frac{2a}{b^2}",
     "椭圆为定值，双曲线同款", "抛物线对应 2/p"),
    ("焦点弦乘积", r"x_1x_2=\frac{p^2}{4},\ \ y_1y_2=-p^2",
     "韦达定理直接写", "联立都不用算"),
    ("抛物线通径", r"|AB|_{\min}=2p",
     "垂直于对称轴的焦点弦", "抛物线最短焦点弦"),
    ("圆切准线", r"R=\frac{|AB|}{2}=d(M,\,l)",
     "以 AB 为直径的圆", "与准线一定相切"),
    ("光学·抛物线", r"y^2=2px",
     "平行于轴的光线反射过焦点", "太阳灶的原理"),
    ("光学·椭圆双曲线", r"F_1\longrightarrow P\longrightarrow F_2",
     "椭圆：一个焦点发出的光", "反射后必过另一个焦点"),
    ("弦长公式", r"|AB|=\sqrt{1+k^2}\cdot\frac{\sqrt{\Delta}}{|A|}",
     "联立消元后的万能钥匙", "A 是二次项系数"),
    ("通径大统一", r"\frac{2b^2}{a}\quad\text{and}\quad 2p",
     "椭圆双曲线 vs 抛物线", "通径大统一"),
    ("定点·椭圆", r"k_1k_2=e^2-1\Longrightarrow O\in AB",
     "即 k1·k2 = −b²/a²", "P 在椭圆上，AB 恒过原点"),
    ("定点·椭圆斜率", r"k_1+k_2=0\Longrightarrow k_{AB}=\frac{b^2x_0}{a^2y_0}",
     "斜率之和为零", "AB 斜率恒为定值"),
    ("定点·双曲线", r"k_1k_2=e^2-1\Longrightarrow O\in AB",
     "即 k1·k2 = b²/a²", "双曲线同款过原点"),
    ("定点·双曲斜率", r"k_1+k_2=0\Longrightarrow k_{AB}=-\frac{b^2x_0}{a^2y_0}",
     "和零定斜率", "只差一个负号"),
    ("定点·双曲进阶", r"k_1k_2=e^2\Longrightarrow T=\frac{a^2}{a^2+2b^2}(x_0,-y_0)",
     "斜率之积等于 e²", "AB 过定点 T"),
    ("定点·抛物线", r"k_1k_2=\lambda\Longrightarrow T=\Big(x_0-\frac{2p}{\lambda},\ -y_0\Big)",
     "λ=-1 时 T=(x0+2p, -y0)", "斜率之积定值 → 过定点"),
    ("定点·抛物斜率", r"k_1+k_2=0\Longrightarrow k_{AB}=-\frac{p}{y_0}",
     "和零定斜率", "抛物线版本"),
    ("口诀总结", r"k_1+k_2=0\Rightarrow\text{slope const},\ \ \ k_1k_2=\lambda\Rightarrow\text{fixed point}",
     "和零定斜率，积定过定点", "特殊值探路，一般证明收尾"),
]

# ---------- 壁纸公式 ----------
WALL_TEX = [
    r"\frac{x^2}{a^2}+\frac{y^2}{b^2}=1", r"\frac{x^2}{a^2}-\frac{y^2}{b^2}=1",
    r"y^2=2px", r"e=\frac{c}{a}", r"k_1k_2=-\frac{b^2}{a^2}",
    r"|AB|=\frac{2p}{\sin^2\theta}", r"F_1(-c,0)", r"l:\ x=-\frac{a^2}{c}",
    r"r=a+ex_0", r"b^2\tan\frac{\theta}{2}", r"b^2\cot\frac{\theta}{2}",
    r"y=\pm\frac{b}{a}x", r"\sqrt{1+k^2}", r"\Delta=b^2-4ac",
    r"\frac{1}{|FA|}+\frac{1}{|FB|}=\frac{2a}{b^2}", r"x_1x_2=\frac{p^2}{4}",
    r"y_1y_2=-p^2", r"\frac{2b^2}{a}", r"\Gamma(x)=\int t^{x-1}e^{-t}dt",
    r"\rho=\frac{ep}{1-e\cos\theta}", r"\frac{a^2}{c}-c", r"e=\sqrt{2}",
    r"\cosh t=\frac{e^t+e^{-t}}{2}", r"\big||MF_1|-|MF_2|\big|=2a",
    r"x_I=a", r"\sin^2\theta+\cos^2\theta=1",
]


class ConicMixCut(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.pending_fade = []
        self.add_wallpaper()
        self.opening()
        self.run_cards()
        self.ending()

    # ---------- 壁纸 ----------
    def add_wallpaper(self):
        rng = np.random.default_rng(7)
        wall = VGroup()
        for tex in WALL_TEX:
            m = MathTex(tex, font_size=int(rng.integers(34, 48)), color=WALL)
            m.set_opacity(0.10)
            m.move_to([rng.uniform(-7.1, 7.1), rng.uniform(-4.0, 4.0), 0])
            m.rotate(rng.uniform(-0.12, 0.12))
            wall.add(m)
        self.wallpaper = wall
        self.add(wall)

    # ---------- 组装卡片 ----------
    def make_title(self, name, font_size=60):
        t1 = Text(PREFIX, font=ZH_FONT, font_size=font_size, color=PREFIX_C, weight=BOLD)
        t2 = Text(name, font=ZH_FONT, font_size=font_size, weight=BOLD)
        t2.set_color_by_gradient(*NAME_GR)
        bar = VGroup(t1, t2).arrange(RIGHT, buff=0.15)
        bar.to_edge(UP, buff=0.45)
        return bar

    def make_formula(self, latex, font_size=64, pos=UP * 0.55):
        f = MathTex(latex, font_size=font_size, stroke_width=1.2)
        f.set_color_by_gradient(*FORM_GR)
        if f.width > 14.4:
            f.scale_to_fit_width(14.4)
        f.move_to(pos)
        return f

    def make_subs(self, s1, s2, pos=DOWN * 2.35):
        l1 = Text(s1, font=ZH_FONT, font_size=34, color=SUB1_C, weight=BOLD)
        l2 = Text(s2, font=ZH_FONT, font_size=26, color=SUB2_C)
        return VGroup(l1, l2).arrange(DOWN, buff=0.42).move_to(pos)

    def morph_to(self, new_t, new_f, new_s, run_time=T_RUN):
        anims = [
            ReplacementTransform(self.cur_t, new_t),
            TransformMatchingTex(self.cur_f, new_f, transform_mismatches=True),
            ReplacementTransform(self.cur_s, new_s),
        ]
        if self.pending_fade:
            anims += [FadeOut(m) for m in self.pending_fade]
            self.pending_fade = []
        self.play(*anims, run_time=run_time)
        self.cur_t, self.cur_f, self.cur_s = new_t, new_f, new_s

    def go_card(self, idx):
        name, latex, s1, s2 = CARDS[idx]
        self.morph_to(self.make_title(name), self.make_formula(latex),
                      self.make_subs(s1, s2))
        self.wait(T_HOLD)

    # ---------- 开场 ----------
    def opening(self):
        big = VGroup(
            Text("圆锥曲线", font=ZH_FONT, font_size=76, weight=BOLD),
            Text("·", font=ZH_FONT, font_size=76, color=MUTED),
            Text("二级结论", font=ZH_FONT, font_size=76, weight=BOLD),
        ).arrange(RIGHT, buff=0.3)
        big.set_color_by_gradient("#FFD166", "#F59E62")
        big.move_to(UP * 0.8)
        sub1 = Text("34 条神结论 · 一分钟刷完", font=ZH_FONT, font_size=40,
                    color=SUB1_C, weight=BOLD).next_to(big, DOWN, buff=0.8)
        sub2 = Text("快速形变 · 护眼暗色", font=ZH_FONT, font_size=28,
                    color=SUB2_C).next_to(sub1, DOWN, buff=0.5)
        self.play(FadeIn(big, shift=UP * 0.4), run_time=0.4)
        self.play(Write(sub1), FadeIn(sub2), run_time=0.35)
        self.wait(0.5)

        name, latex, s1, s2 = CARDS[0]
        new_t = self.make_title(name)
        new_s = self.make_subs(s1, s2)
        new_f = self.make_formula(latex)
        self.play(
            TransformMatchingShapes(big, new_t),
            TransformMatchingShapes(VGroup(sub1, sub2), new_s),
            FadeIn(new_f, shift=DOWN * 0.3),
            run_time=0.5,
        )
        self.cur_t, self.cur_f, self.cur_s = new_t, new_f, new_s
        self.wait(T_HOLD)

    # ---------- 主循环 ----------
    def run_cards(self):
        for i, card in enumerate(CARDS):
            if i == 0:
                continue
            name = card[0]
            if name == "椭圆第一定义":
                self.graph_ellipse(card)
            elif name == "渐近线":
                self.graph_hyper(card)
            elif name == "焦点弦":
                self.graph_para(card)
            elif name == "定点·椭圆":
                self.graph_fixed(card)
            else:
                self.go_card(i)

    # ---------- 绘图页1：椭圆第一定义 ----------
    def graph_ellipse(self, card):
        name, latex, s1, s2 = card
        self.morph_to(self.make_title(name),
                      self.make_formula(latex, font_size=50, pos=UP * 1.85),
                      self.make_subs(s1, s2, pos=DOWN * 2.8))
        a, b = 2.05, 1.4
        c = float(np.sqrt(a * a - b * b))
        ctr = DOWN * 1.05
        ell = Ellipse(width=2 * a, height=2 * b, color="#FFD166", stroke_width=5)
        ell.move_to(ctr)
        F1 = Dot(ctr + LEFT * c, radius=0.07, color="#F59E62")
        F2 = Dot(ctr + RIGHT * c, radius=0.07, color="#F59E62")
        th = 0.7
        P = Dot(ctr + np.array([a * np.cos(th), b * np.sin(th), 0]),
                radius=0.07, color="#5DADEC")
        seg1 = Line(F1.get_center(), P.get_center(), color="#5DADEC", stroke_width=4)
        seg2 = Line(F2.get_center(), P.get_center(), color="#5DADEC", stroke_width=4)
        l1 = MathTex(r"r_1", font_size=28, color="#5DADEC").move_to(
            F1.get_center() * 0.45 + P.get_center() * 0.55 + UP * 0.32 + LEFT * 0.25)
        l2 = MathTex(r"r_2", font_size=28, color="#5DADEC").move_to(
            F2.get_center() * 0.45 + P.get_center() * 0.55 + UP * 0.32 + RIGHT * 0.3)
        f1l = MathTex(r"F_1", font_size=28, color=MUTED).next_to(F1, DOWN, buff=0.15)
        f2l = MathTex(r"F_2", font_size=28, color=MUTED).next_to(F2, DOWN, buff=0.15)
        self.play(Create(ell), run_time=0.45)
        self.play(Create(seg1), Create(seg2), FadeIn(F1), FadeIn(F2), FadeIn(P), run_time=0.3)
        self.play(FadeIn(l1), FadeIn(l2), FadeIn(f1l), FadeIn(f2l), run_time=0.25)
        self.wait(0.7)
        self.pending_fade = [ell, F1, F2, P, seg1, seg2, l1, l2, f1l, f2l]

    # ---------- 绘图页2：双曲线渐近线 ----------
    def graph_hyper(self, card):
        name, latex, s1, s2 = card
        self.morph_to(self.make_title(name),
                      self.make_formula(latex, font_size=50, pos=UP * 1.85),
                      self.make_subs(s1, s2, pos=DOWN * 2.8))
        a, b = 1.7, 1.3
        c = float(np.sqrt(a * a + b * b))
        m = b / a
        ctr = DOWN * 0.95
        br1 = ParametricFunction(
            lambda t: ctr + np.array([a * np.cosh(t), b * np.sinh(t), 0]),
            t_range=[-1.35, 1.35], color="#FFD166", stroke_width=5)
        br2 = ParametricFunction(
            lambda t: ctr + np.array([-a * np.cosh(t), b * np.sinh(t), 0]),
            t_range=[-1.35, 1.35], color="#FFD166", stroke_width=5)
        asy1 = DashedLine(ctr + np.array([-5.6, -5.6 * m, 0]) * 0.85,
                          ctr + np.array([5.6, 5.6 * m, 0]) * 0.85,
                          color="#5DADEC", stroke_width=3)
        asy2 = DashedLine(ctr + np.array([-5.6, 5.6 * m, 0]) * 0.85,
                          ctr + np.array([5.6, -5.6 * m, 0]) * 0.85,
                          color="#5DADEC", stroke_width=3)
        F2 = Dot(ctr + RIGHT * c, radius=0.07, color="#F59E62")
        t_f = c / (1 + m * m)
        foot = ctr + np.array([t_f, m * t_f, 0])
        perp = DashedLine(F2.get_center(), foot, color="#FF6B6B", stroke_width=3)
        dlab = MathTex(r"d=b", font_size=30, color="#FF6B6B").move_to(
            F2.get_center() * 0.4 + foot * 0.6 + DOWN * 0.35)
        flab = MathTex(r"F_2", font_size=28, color=MUTED).next_to(F2, DOWN, buff=0.15)
        alab = MathTex(r"y=\frac{b}{a}x", font_size=26, color="#5DADEC").move_to(
            ctr + np.array([4.1, 4.1 * m, 0]) + RIGHT * 0.1 + UP * 0.25)
        self.play(Create(asy1), Create(asy2), run_time=0.3)
        self.play(Create(br1), Create(br2), FadeIn(F2), FadeIn(flab), run_time=0.4)
        self.play(Create(perp), FadeIn(dlab), FadeIn(alab), run_time=0.3)
        self.wait(0.7)
        self.pending_fade = [br1, br2, asy1, asy2, F2, perp, dlab, flab, alab]

    # ---------- 绘图页3：抛物线焦点弦 ----------
    def graph_para(self, card):
        name, latex, s1, s2 = card
        self.morph_to(self.make_title(name),
                      self.make_formula(latex, font_size=50, pos=UP * 1.85),
                      self.make_subs(s1, s2, pos=DOWN * 2.8))
        s = 1.35
        ox = -0.6                       # 顶点 x
        par = ParametricFunction(
            lambda t: np.array([ox + s * t * t / 2, s * t, 0]),
            t_range=[-2.05, 2.05], color="#FFD166", stroke_width=5)
        p2 = 0.675                      # p/2（像素单位）
        F = Dot([ox + p2, 0, 0], radius=0.07, color="#F59E62")
        flab = MathTex(r"F", font_size=28, color=MUTED).next_to(F, DOWN, buff=0.15)
        direct = DashedLine([ox - p2, -2.95, 0], [ox - p2, 2.95, 0],
                            color="#5DADEC", stroke_width=3)
        dlab = MathTex(r"l", font_size=28, color="#5DADEC").move_to([ox - p2, 3.1, 0])
        tA, tB = 0.414, -2.414          # 斜率 -1 的焦点弦参数
        A = np.array([ox + s * tA * tA / 2, s * tA, 0])
        B = np.array([ox + s * tB * tB / 2, s * tB, 0])
        chord = Line(A - np.array([1.1, -1.1, 0]) * 0.6, B + np.array([1.1, -1.1, 0]) * 0.25,
                     color="#F59E62", stroke_width=4)
        dA = DashedLine(A, [ox - p2, A[1], 0], color=MUTED, stroke_width=2)
        dB = DashedLine(B, [ox - p2, B[1], 0], color=MUTED, stroke_width=2)
        M = (A + B) / 2
        R = float(np.linalg.norm(A - B) / 2)
        circ = Circle(radius=R, color="#5DADEC", stroke_width=3).set_stroke(opacity=0.85)
        circ.move_to(M)
        alab = MathTex(r"A", font_size=26, color=MUTED).next_to(A, UP, buff=0.12)
        blab = MathTex(r"B", font_size=26, color=MUTED).next_to(B, UP, buff=0.12)
        self.play(Create(par), FadeIn(F), FadeIn(flab), Create(direct), FadeIn(dlab), run_time=0.45)
        self.play(Create(chord), Create(dA), Create(dB), FadeIn(alab), FadeIn(blab), run_time=0.3)
        self.play(Create(circ), run_time=0.25)
        self.wait(0.7)
        self.pending_fade = [par, F, flab, direct, dlab, chord, dA, dB, alab, blab, circ]

    # ---------- 绘图页4：定点定值（k1k2=e²-1 → AB 恒过原点） ----------
    def graph_fixed(self, card):
        name, latex, s1, s2 = card
        self.morph_to(self.make_title(name),
                      self.make_formula(latex, font_size=50, pos=UP * 1.85),
                      self.make_subs(s1, s2, pos=DOWN * 2.8))
        a, b = 2.0, 1.4
        ctr = DOWN * 0.95
        sc = 1.3
        ell = Ellipse(width=2 * a * sc, height=2 * b * sc, color="#FFD166", stroke_width=5)
        ell.move_to(ctr)
        P0 = np.array([1.2, 1.4 * np.sqrt(1 - 1.2 ** 2 / 4), 0.0])
        P = ctr + P0 * sc
        Pdot = Dot(P, radius=0.07, color="#5DADEC")
        Plab = MathTex(r"P", font_size=28, color="#5DADEC").next_to(P, UP, buff=0.12)
        Odot = Dot(ctr, radius=0.09, color="#FF6B6B")
        Olab = MathTex(r"O", font_size=30, color="#FF6B6B").next_to(Odot, DL, buff=0.12)

        def si(k):
            x0, y0, _ = P0
            t = -2 * (x0 / a ** 2 + k * y0 / b ** 2) / (1 / a ** 2 + k ** 2 / b ** 2)
            return ctr + np.array([x0 + t, y0 + k * t, 0]) * sc

        lines = VGroup()
        dots = VGroup()
        for k1, col in [(0.6, "#F59E62"), (1.2, "#B79CFF")]:
            A = si(k1)
            B = si(-k1)
            lines.add(VGroup(Line(A, B, color=col, stroke_width=4),
                             Line(P, A, color=MUTED, stroke_width=2),
                             Line(P, B, color=MUTED, stroke_width=2)))
            dots.add(VGroup(Dot(A, radius=0.05, color=col), Dot(B, radius=0.05, color=col)))
        self.play(Create(ell), FadeIn(Pdot), FadeIn(Plab), FadeIn(Odot), FadeIn(Olab), run_time=0.45)
        self.play(Create(lines[0]), FadeIn(dots[0]), run_time=0.3)
        self.play(Create(lines[1]), FadeIn(dots[1]), run_time=0.3)
        box = SurroundingRectangle(Odot, color="#FF6B6B", buff=0.1, corner_radius=0.05)
        self.play(Create(box), run_time=0.25)
        self.wait(0.6)
        self.pending_fade = [ell, Pdot, Plab, Odot, Olab, lines, dots, box]

    # ---------- 结尾 ----------
    def ending(self):
        end_t = Text("点赞 · 收藏 · 关注", font=ZH_FONT, font_size=64, weight=BOLD)
        end_t.set_color_by_gradient("#FFD166", "#F59E62")
        end_t.to_edge(UP, buff=0.45)
        end_f = self.make_formula(r"P(\text{pass})\to 1", font_size=64)
        end_s = self.make_subs("逢考必过", "下期更炫")
        self.morph_to(end_t, end_f, end_s)
        self.wait(1.1)
        self.play(FadeOut(self.cur_t), FadeOut(self.cur_f), FadeOut(self.cur_s),
                  FadeOut(self.wallpaper), run_time=0.4)
