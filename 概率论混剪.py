from manim import *
import numpy as np

# ============ 模板B：壁纸混剪风（逆向自爆款样本） ============
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16.0
config.frame_height = 9.0

ZH_FONT  = "Kaiti SC"
BG       = "#050505"
WALL     = "#3A3F4B"
PREFIX_C = "#CDDC39"   # 固定前缀：黄绿
NAME_GR  = ("#FFD166", "#F59E62")   # 主题名：金橙渐变
FORM_GR  = ("#FF8A50", "#FFD166")   # 公式：橙→金 渐变
SUB1_C   = "#66D19E"
SUB2_C   = "#4DB6AC"
MUTED    = "#A9B4C2"
PREFIX   = "概率统计："

T_RUN  = 0.45   # 形变时长（样本B实测：14卡/14.4s ≈ 1.03s/卡）
T_HOLD = 0.55   # 停留时长

# ---------- 卡片数据：(标题, 公式LaTeX, 副标题1, 副标题2) ----------
CARDS = [
    ("容斥公式", r"P(A\cup B)=P(A)+P(B)-P(AB)",
     "三事件：加减交替进行", "集合思想"),
    ("条件概率", r"P(B\,|\,A)=\frac{P(AB)}{P(A)}",
     "乘法公式：链式相乘", "缩小样本空间"),
    ("全概率公式", r"P(B)=\sum_{i}P(A_i)P(B\,|\,A_i)",
     "完备事件组加权平均", "由因推果"),
    ("贝叶斯公式", r"P(A_j\,|\,B)=\frac{P(A_j)P(B\,|\,A_j)}{P(B)}",
     "先验变后验", "由果溯因"),
    ("抽签公平原理", r"P(A_k)=\frac{m}{n}\quad(k=1,2,\cdots,n)",
     "中签概率与顺序无关", "不必抢第一个！"),
    ("二项分布", r"P(X=k)=C_n^k p^k q^{n-k},\ \ E(X)=np",
     "D(X)=npq，n 重伯努利", "q = 1-p"),
    ("泊松分布", r"P(X=k)=\frac{\lambda^k e^{-\lambda}}{k!}",
     "n 大 p 小时二项的极限", "期望与方差都是 λ"),
    ("几何分布", r"P(X=k)=q^{k-1}p,\ \ E(X)=\frac{1}{p}",
     "首次成功所需次数", "离散型无记忆"),
    ("指数分布·无记忆", r"P(X>s+t\,|\,X>s)=P(X>t)",
     "已用 s 小时，剩余重新算", "连续型唯一无记忆"),
    ("切比雪夫不等式", r"P\big(|X-E(X)|\geq\varepsilon\big)\leq\frac{D(X)}{\varepsilon^2}",
     "只知道期望方差也能估计", "万能放缩"),
    ("方差计算神器", r"E(X^2)=D(X)+E^2(X)",
     "先求 E(X²) 再减 E 的平方", "出现率 100%"),
    ("方差的线性性", r"D(aX+b)=a^2 D(X)",
     "常数被吃掉，倍数要平方", "不需要独立"),
    ("协方差", r"\mathrm{Cov}(X,Y)=E(XY)-E(X)E(Y)",
     "D(X±Y) 拆分的钥匙", "独立则 Cov = 0"),
    ("相关系数", r"|\rho|\leq 1,\ \ |\rho|=1\Longleftrightarrow P(Y=aX+b)=1",
     "线性相关强弱", "标准化协方差"),
    ("最大最小值分布", r"F_{\max}(y)=\big[F(y)\big]^n,\ \ F_{\min}(y)=1-\big[1-F(y)\big]^n",
     "n 个独立同分布", "期末大题常客"),
    ("标准化", r"Z=\frac{X-\mu}{\sigma}\sim N(0,1)",
     "任何正态查同一张表", "横轴平移+缩放"),
    ("正态线性组合", r"aX+b\sim N\big(a\mu+b,\ a^2\sigma^2\big)",
     "独立正态相加仍是正态", "正态家族封闭性"),
    ("卡方分布", r"\chi^2(m)+\chi^2(n)=\chi^2(m+n)",
     "期望 n，方差 2n", "标准正态平方和"),
    ("t 分布与 F 分布", r"t^2(n)=F(1,n)",
     "n→∞ 时 t 变标准正态", "三大分布一家人"),
    ("样本均值分布", r"\bar{X}\sim N\Big(\mu,\ \frac{\sigma^2}{n}\Big)",
     "正态总体镇店之宝", "平均之后更集中"),
    ("样本方差分布", r"\frac{(n-1)S^2}{\sigma^2}\sim\chi^2(n-1)",
     "E(S²)=σ²，无偏估计", "为什么除 n-1"),
    ("统计的基石", r"\bar{X}\ \perp\ S^2",
     "正态总体下相互独立", "t 分布全靠它"),
]

# ---------- 壁纸公式（静止幽灵层） ----------
WALL_TEX = [
    r"P(A|B)=\frac{P(AB)}{P(A)}", r"\int_{-\infty}^{+\infty}f(x)dx=1",
    r"\sum_{k=0}^{\infty}p_k=1", r"F(x)=P(X\leq x)",
    r"\lim_{n\to\infty}F_n(x)=F(x)", r"\rho=\frac{Cov(X,Y)}{\sqrt{DX}\sqrt{DY}}",
    r"E(X)=\int x f(x)dx", r"\chi^2=\sum_{i=1}^n X_i^2",
    r"C_n^k=\frac{n!}{k!(n-k)!}", r"\lambda^{k}e^{-\lambda}",
    r"N(\mu,\sigma^2)", r"\bar{X}=\frac{1}{n}\sum X_i",
    r"\Gamma\Big(\frac{n}{2}\Big)", r"\phi(x)=\frac{1}{\sqrt{2\pi}}e^{-x^2/2}",
    r"\sqrt{n}\ \sigma", r"\ i.i.d.", r"\alpha=0.05",
    r"S^2=\frac{1}{n-1}\sum(X_i-\bar{X})^2", r"D(X)\geq 0",
    r"P\big(|Z|>z\big)", r"t_{\alpha/2}(n)", r"\prod_{i=1}^{n}p_i",
    r"e^{-\lambda}\sum \frac{\lambda^k}{k!}",
    r"\int_a^b\frac{1}{b-a}dx", r"\frac{1}{\sigma\sqrt{2\pi}}",
]


class ProbMixCut(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.pending_fade = []
        self.add_wallpaper()
        self.opening()
        self.run_cards()
        self.ending()

    # ---------- 壁纸 ----------
    def add_wallpaper(self):
        rng = np.random.default_rng(42)
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

    def make_subs(self, s1, s2):
        l1 = Text(s1, font=ZH_FONT, font_size=34, color=SUB1_C, weight=BOLD)
        l2 = Text(s2, font=ZH_FONT, font_size=26, color=SUB2_C)
        return VGroup(l1, l2).arrange(DOWN, buff=0.42).move_to(DOWN * 2.35)

    def morph_to(self, new_t, new_f, new_s, run_time=T_RUN):
        anims = [
            # 标题/副标题：整族字形拉伸形变（字形不足的会被复制拉伸，产生样本里的“拉丝”感）
            ReplacementTransform(self.cur_t, new_t),
            # 公式：共享符号精确飞行，对不上的碎片不淡出、而是互相形变过去（爆款转场的灵魂）
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
            Text("概率统计", font=ZH_FONT, font_size=76, weight=BOLD),
            Text("·", font=ZH_FONT, font_size=76, color=MUTED),
            Text("考试神公式", font=ZH_FONT, font_size=76, weight=BOLD),
        ).arrange(RIGHT, buff=0.3)
        big.set_color_by_gradient("#FFD166", "#F59E62")
        big.move_to(UP * 0.8)
        sub1 = Text("22 条二级结论 · 一分钟刷完", font=ZH_FONT, font_size=40,
                    color=SUB1_C, weight=BOLD).next_to(big, DOWN, buff=0.8)
        sub2 = Text("快速形变 · 护眼暗色", font=ZH_FONT, font_size=28,
                    color=SUB2_C).next_to(sub1, DOWN, buff=0.5)
        self.play(FadeIn(big, shift=UP * 0.4), run_time=0.4)
        self.play(Write(sub1), FadeIn(sub2), run_time=0.35)
        self.wait(0.5)

        # 变身成第 1 张卡（三路同拍，跟上混剪节奏）
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
            if name == "标准化":
                self.graph_bell()      # 3σ 绘图页，随后自然接“标准化”
                self.go_card(i)
            elif name == "卡方分布":
                self.graph_clt()       # CLT 绘图页，随后自然接“卡方分布”
                self.go_card(i)
            else:
                self.go_card(i)

    # ---------- 绘图页1：3σ 钟形曲线（样本A式绘图） ----------
    def graph_bell(self):
        self.morph_to(
            self.make_title("3σ 原则"),
            self.make_formula(r"P(|X-\mu|\le 3\sigma)\approx 0.9973",
                              font_size=50, pos=DOWN * 1.55),
            self.make_subs("68.3% → 95.4% → 99.7%", "考试估算神器"),
        )
        axes = Axes(x_range=[-4, 4, 1], y_range=[0, 0.45, 0.1],
                    x_length=9.6, y_length=2.9,
                    axis_config={"color": WALL, "stroke_width": 2, "include_ticks": False})
        axes.move_to(UP * 1.15)
        pdf = lambda x: np.exp(-x * x / 2) / np.sqrt(2 * np.pi)
        curve = axes.plot(pdf, x_range=[-3.9, 3.9], color="#FFD166", stroke_width=5)
        area1 = axes.get_area(curve, x_range=[-1, 1], color="#66D19E", opacity=0.45)
        area2 = VGroup(axes.get_area(curve, x_range=[-2, -1], color="#F59E62", opacity=0.4),
                       axes.get_area(curve, x_range=[1, 2], color="#F59E62", opacity=0.4))
        area3 = VGroup(axes.get_area(curve, x_range=[-3, -2], color="#FF6B6B", opacity=0.35),
                       axes.get_area(curve, x_range=[2, 3], color="#FF6B6B", opacity=0.35))
        p1 = Text("68.3%", font=ZH_FONT, font_size=26, color="#0F1720", weight=BOLD)
        p1.move_to(axes.c2p(0, 0.12))
        p2 = Text("95.4%", font=ZH_FONT, font_size=24, color="#FFD166", weight=BOLD)
        p2.move_to(axes.c2p(1.5, 0.05))
        p3 = Text("99.7%", font=ZH_FONT, font_size=24, color="#FF6B6B", weight=BOLD)
        p3.move_to(axes.c2p(2.75, 0.03))
        ticks = VGroup(*[
            MathTex(s, font_size=26, color=MUTED).move_to(axes.c2p(x, -0.06)).shift(DOWN * 0.3)
            for s, x in [(r"\mu", 0), (r"\pm\sigma", 1), (r"\pm 2\sigma", 2), (r"\pm 3\sigma", 3)]
        ])
        self.play(Create(axes), Create(curve), run_time=0.45)
        self.play(FadeIn(area1), FadeIn(area2), FadeIn(area3), run_time=0.3)
        self.play(FadeIn(p1), FadeIn(p2), FadeIn(p3), FadeIn(ticks), run_time=0.25)
        self.wait(0.7)
        self.pending_fade = [axes, curve, area1, area2, area3, p1, p2, p3, ticks]

    # ---------- 绘图页2：CLT 柱状图逼近正态 ----------
    def graph_clt(self):
        self.morph_to(
            self.make_title("中心极限定理"),
            self.make_formula(
                r"\frac{\bar{X}-\mu}{\sigma/\sqrt{n}}\;\xrightarrow{\;n\to\infty\;}\;N(0,1)",
                font_size=50, pos=UP * 1.75),
            self.make_subs("不管总体是什么分布", "样本够大就近似正态"),
        )
        heights = [0.12, 0.26, 0.5, 0.82, 1.18, 1.45, 1.55, 1.45, 1.18, 0.82, 0.5, 0.26, 0.12]
        base_y = -1.5
        bars = VGroup()
        for k, h in enumerate(heights):
            x = -3.6 + k * 0.6
            bars.add(Rectangle(width=0.5, height=h, fill_color="#F59E62",
                               fill_opacity=0.75, stroke_width=0)
                     .move_to([x + 0.3, base_y + h / 2, 0]))
        baseline = Line([-3.9, base_y, 0], [3.9, base_y, 0], color=WALL, stroke_width=2)
        curve = ParametricFunction(
            lambda t: np.array([t, base_y + 1.45 * np.exp(-t * t / (2 * 0.95 ** 2)), 0]),
            t_range=[-3.4, 3.4], color="#FFD166", stroke_width=5)
        lab = Text("样本均值的分布 → 越来越像钟形", font=ZH_FONT, font_size=28, color=MUTED)
        lab.move_to([0, base_y + 1.95, 0])
        self.play(FadeIn(bars, lag_ratio=0.06), Create(baseline), run_time=0.45)
        self.play(Create(curve), FadeIn(lab), run_time=0.3)
        self.wait(0.7)
        self.pending_fade = [bars, baseline, curve, lab]

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
