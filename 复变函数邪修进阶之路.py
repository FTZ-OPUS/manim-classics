from manim import *
import numpy as np

# ============ 公式混剪·复变函数邪修进阶之路（mixcut SKILL + 新图层：动态彩色函数图像） ============
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16.0
config.frame_height = 9.0

ZH_FONT  = "Kaiti SC"
BG       = "#050505"
INK      = "#F6F2EA"
WALL     = "#3A3F4B"
MUTED    = "#A9B4C2"
PREFIX_C = "#CDDC39"
NAME_GR  = ("#FFD166", "#F59E62")
FORM_GR  = ("#FF8A50", "#FFD166")
SUB1_C   = "#66D19E"
SUB2_C   = "#4DB6AC"
VIOLET   = "#B79CFF"
PREFIX   = "复变函数："
PC       = DOWN * 1.75          # 函数图像面板中心

T_RUN  = 0.45
T_HOLD = 0.55

# ---------- 卡片数据：(标题, 公式, 副标题1(境界·标签), 副标题2, 绘图键) ----------
CARDS = [
    ("复数与共轭", r"z=x+iy,\quad \bar{z}=x-iy,\quad z\bar{z}=|z|^2",
     "炼气·复数的骨架", "模长 |z| 与辐角 θ", None),
    ("指数形式", r"z=re^{i\theta},\quad r=|z|,\ \theta=\arg z",
     "炼气·极坐标登场", "模与辐角", None),
    ("欧拉公式", r"e^{i\theta}=\cos\theta+i\sin\theta",
     "炼气·天人合一", "复指数就是旋转", "euler"),
    ("棣莫弗定理", r"(\cos\theta+i\sin\theta)^n=\cos n\theta+i\sin n\theta",
     "炼气·旋转连击", "n 次幂 = n 倍角", None),
    ("单位根", r"z^n=1\ \Longrightarrow\ z_k=e^{\frac{2k\pi i}{n}}",
     "炼气·根的均匀分布", "正 n 边形的顶点", "roots"),
    ("三角不等式", r"|z_1+z_2|\le|z_1|+|z_2|",
     "炼气·三角不等式", "模的次可加性", None),
    ("乘除几何", r"z_1z_2=r_1r_2\,e^{i(\theta_1+\theta_2)}",
     "炼气·乘法即旋转拉伸", "模相乘，辐角相加", None),
    ("复导数", r"f'(z_0)=\lim_{z\to z_0}\frac{f(z)-f(z_0)}{z-z_0}",
     "筑基·更强的可导", "任意方向极限都相同", None),
    ("柯西-黎曼方程", r"\frac{\partial u}{\partial x}=\frac{\partial v}{\partial y},\quad \frac{\partial u}{\partial y}=-\frac{\partial v}{\partial x}",
     "筑基·解析的心法总纲", "u_x=v_y, u_y=-v_x", "cr"),
    ("解析求导", r"f'(z_0)=u_x+iv_x",
     "筑基·导数速算", "CR 方程的直接推论", None),
    ("调和函数", r"u_{xx}+u_{yy}=0\quad(\text{Laplace})",
     "筑基·解析必然调和", "实虚部都是调和函数", "harm"),
    ("指数函数", r"e^z=e^x(\cos y+i\sin y)",
     "筑基·周期降临", "沿虚轴以 2πi 为周期", None),
    ("三角函数", r"\sin z=\frac{e^{iz}-e^{-iz}}{2i}",
     "筑基·突破实数边界", "|sin z| 可以大于 1", None),
    ("对数函数", r"\log z=\ln|z|+i\arg z",
     "筑基·多值的心魔", "支割线：负实轴", "log"),
    ("幂函数", r"z^a=e^{a\log z}",
     "筑基圆满·万法归一", "指数与对数的合体", None),
    ("复积分", r"\int_C f(z)\,dz=\lim_{n\to\infty}\sum_{k=1}^{n}f(\zeta_k)\,\Delta z_k",
     "金丹·沿曲线积分", "定向分割求和", None),
    ("积分估计", r"\left|\int_C f(z)\,dz\right|\le ML",
     "金丹·积分的上界", "M=|f| 上界，L=弧长", None),
    ("柯西积分定理", r"\oint_C f(z)\,dz=0",
     "金丹·解析即归零", "单连通域内闭曲线积分", None),
    ("柯西积分公式", r"f(z_0)=\frac{1}{2\pi i}\oint_C\frac{f(z)}{z-z_0}\,dz",
     "金丹·一点决定全域", "内部值由边界决定", "cauchy"),
    ("高阶导数公式", r"f^{(n)}(z_0)=\frac{n!}{2\pi i}\oint_C\frac{f(z)}{(z-z_0)^{n+1}}\,dz",
     "金丹·导数也能积分算", "n 阶导数 = n! 版公式", None),
    ("复合闭路定理", r"\oint_{C_0}f\,dz=\sum_{k=1}^{n}\oint_{C_k}f\,dz",
     "金丹·外路等于内路和", "多连通域通行证", None),
    ("路径无关", r"\int_{C_1}f\,dz=\int_{C_2}f\,dz",
     "金丹·殊途同归", "解析域内路径无关", None),
    ("收敛圆", r"\sum_{n=0}^{\infty}a_n(z-z_0)^n,\quad R=\frac{1}{\limsup\limits_{n\to\infty}\sqrt[n]{|a_n|}}",
     "元婴·收敛半径", "柯西-阿达马公式", None),
    ("阿贝尔定理", r"|z|<|z_0|\ \Longrightarrow\ \sum a_nz^n\ \text{absolutely conv.}",
     "元婴·阿贝尔定理", "圆内绝对收敛", None),
    ("泰勒展开", r"f(z)=\sum_{n=0}^{\infty}\frac{f^{(n)}(z_0)}{n!}(z-z_0)^n",
     "元婴·泰勒展开", "收敛半径=最近奇点", "taylor"),
    ("几何级数", r"\frac{1}{1-z}=\sum_{n=0}^{\infty}z^n\quad(|z|<1)",
     "元婴·最基础的级数", "洛朗级数的特例", None),
    ("洛朗级数", r"f(z)=\sum_{n=-\infty}^{+\infty}c_n(z-z_0)^n,\ \ c_n=\frac{1}{2\pi i}\oint_C\frac{f(\zeta)}{(\zeta-z_0)^{n+1}}d\zeta",
     "元婴·负幂次觉醒", "圆环域内展开", "laurent"),
    ("奇点分类", r"\lim_{z\to z_0}f(z):\ \text{finite}/\ \infty/\ \text{no limit}",
     "化神·奇点三品", "可去/极点/本性", None),
    ("留数定义", r"\mathrm{Res}[f,z_0]=c_{-1}=\frac{1}{2\pi i}\oint_C f\,dz",
     "化神·留数=负一次幂系数", "洛朗系数 c-1", "residue"),
    ("一阶极点留数", r"\mathrm{Res}[f,z_0]=\lim_{z\to z_0}(z-z_0)f(z)",
     "化神·一阶秒算", "g(z)/(z-z0) 型 = g(z0)", None),
    ("m 阶极点留数", r"\mathrm{Res}[f,z_0]=\frac{1}{(m-1)!}\lim_{z\to z_0}\frac{d^{m-1}}{dz^{m-1}}\big[(z-z_0)^mf(z)\big]",
     "化神·高阶极点", "求导降阶", None),
    ("留数定理", r"\oint_C f\,dz=2\pi i\sum_{k=1}^{n}\mathrm{Res}[f,z_k]",
     "化神大圆满·留数定理", "积分 = 2πi × 留数和", "residue_thm"),
    ("三角积分", r"\int_0^{2\pi}R(\cos\theta,\sin\theta)\,d\theta=2\pi i\sum\mathrm{Res}",
     "化神·实战：三角积分", "单位圆代换 z=e^{iθ}", None),
    ("无穷积分", r"\int_{-\infty}^{+\infty}f(x)\,dx=2\pi i\sum_{\mathrm{Im}\,z_k>0}\mathrm{Res}[f,z_k]",
     "化神·实战：无穷积分", "只收上半平面的留数", None),
    ("若尔当引理", r"\max_{C_R}|f(z)|\to 0\ \Longrightarrow\ \int_{C_R}f(z)e^{iaz}\,dz\to 0",
     "化神·护法：若尔当引理", "大圆弧积分蒸发 (a>0)", None),
    ("刘维尔定理", r"f\ \text{entire},\ |f|\le M\ \Longrightarrow\ f\equiv\text{const}",
     "渡劫·有界整函数必常数", "非常数整函数必然无界", None),
    ("代数基本定理", r"p_n(z)=0\ \text{has exactly}\ n\ \text{roots in}\ \mathbb{C}",
     "渡劫·n 次方程 n 个根", "刘维尔的推论", "fta"),
    ("儒歇定理", r"|f|>|g|\ \text{on}\ C\ \Longrightarrow\ N(f)=N(f+g)",
     "渡劫·儒歇定理", "零点个数：强者说了算", None),
    ("保角映射", r"f'(z_0)\ne 0\ \Longrightarrow\ \text{conformal}",
     "飞升·保角映射", "伸缩 |f'|，旋转 arg f'", "conformal"),
    ("分式线性映射", r"w=\frac{az+b}{cz+d},\quad ad-bc\ne 0",
     "飞升·分式线性映射", "保角保圆保对称保交比", None),
    ("傅里叶级数", r"f(x)=\frac{a_0}{2}+\sum_{n=1}^{\infty}(a_n\cos nx+b_n\sin nx)",
     "飞升·傅里叶级数", "周期函数的大分解", "fourier"),
    ("傅里叶变换对", r"F(\omega)=\int_{-\infty}^{\infty}f(t)e^{-i\omega t}dt,\ \ f(t)=\frac{1}{2\pi}\int_{-\infty}^{\infty}F(\omega)e^{i\omega t}d\omega",
     "飞升·时频互换", "正逆变换一对", "ftpair"),
    ("卷积定理", r"\mathcal{F}[f*g]=\mathcal{F}[f]\cdot\mathcal{F}[g]",
     "飞升·卷积定理", "时域卷积 = 频域乘积", None),
    ("拉普拉斯变换", r"F(s)=\int_0^{+\infty}f(t)e^{-st}dt",
     "飞升·拉普拉斯降临", "复频域 s = σ + iω", None),
    ("拉氏反演", r"f(t)=\frac{1}{2\pi i}\int_{c-i\infty}^{c+i\infty}F(s)e^{st}\,ds",
     "飞升·留数回归", "反演积分又是留数", None),
    ("色散关系", r"\mathrm{Re}F(\omega)=\frac{1}{\pi}\,\mathrm{P}\!\int_{-\infty}^{+\infty}\frac{\mathrm{Im}F(\omega')}{\omega'-\omega}\,d\omega'",
     "飞升·色散关系", "实部虚部互为希尔伯特变换", "kk"),
]

# ---------- 壁纸公式 ----------
WALL_TEX = [
    r"e^{i\theta}=\cos\theta+i\sin\theta", r"\oint_C f(z)\,dz=0",
    r"\frac{\partial u}{\partial x}=\frac{\partial v}{\partial y}",
    r"f(z)=\sum c_n(z-z_0)^n", r"\mathrm{Res}=c_{-1}",
    r"\oint_C\frac{f(z)}{z-z_0}dz=2\pi i f(z_0)",
    r"|f|\le M\Rightarrow f=\text{const}", r"w=\frac{az+b}{cz+d}",
    r"F(\omega)=\int f(t)e^{-i\omega t}dt", r"z=re^{i\theta}",
    r"\log z=\ln|z|+i\arg z", r"z^a=e^{a\log z}",
    r"\lim_{z\to z_0}(z-z_0)f(z)", r"\sin z=\frac{e^{iz}-e^{-iz}}{2i}",
    r"2\pi i\sum\mathrm{Res}", r"\sqrt[n]{|a_n|}",
    r"N(f)=N(f+g)", r"\int_{C_R}f(z)e^{iz}dz\to 0",
    r"u_{xx}+u_{yy}=0", r"\mathcal{F}[f*g]=\mathcal{F}[f]\cdot\mathcal{F}[g]",
    r"e^z=e^x\cos y+i\,e^x\sin y", r"\mathrm{P}\int\frac{\mathrm{Im}F}{\omega'-\omega}",
    r"\left|\int_C f\,dz\right|\le ML", r"\mathrm{diag}(1,\cdots,1)",
    r"z\bar{z}=|z|^2", r"\arg z=\theta+2k\pi",
]


def axes_plot(fn, x0, x1, color, dash=False, sw=3.5):
    """面板坐标绘图：x=0 对准面板中心，1 单位 = 1 manim 单位"""
    pl = ParametricFunction(
        lambda t: PC + np.array([t, fn(t), 0.0]),
        t_range=[x0, x1], color=color, stroke_width=sw)
    if dash:
        pl = DashedVMobject(pl, num_dashes=60)
    return pl


class ComplexMix(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.pending_fade = []
        self.cur_plot = None
        self.add_wallpaper()
        self.opening()
        self.run_cards()
        self.ending()

    # ---------- 壁纸 ----------
    def add_wallpaper(self):
        rng = np.random.default_rng(11)
        wall = VGroup()
        for tex in WALL_TEX:
            m = MathTex(tex, font_size=int(rng.integers(34, 48)), color=WALL)
            m.set_opacity(0.10)
            m.move_to([rng.uniform(-7.1, 7.1), rng.uniform(-4.0, 4.0), 0])
            m.rotate(rng.uniform(-0.12, 0.12))
            wall.add(m)
        self.wallpaper = wall
        self.add(wall)

    # ---------- 组装 ----------
    def make_title(self, name, font_size=58):
        t1 = Text(PREFIX, font=ZH_FONT, font_size=font_size, color=PREFIX_C, weight=BOLD)
        t2 = Text(name, font=ZH_FONT, font_size=font_size, weight=BOLD)
        t2.set_color_by_gradient(*NAME_GR)
        bar = VGroup(t1, t2).arrange(RIGHT, buff=0.15)
        bar.to_edge(UP, buff=0.45)
        return bar

    def make_formula(self, latex, font_size=54, pos=UP * 0.55):
        f = MathTex(latex, font_size=font_size, stroke_width=1.2)
        f.set_color_by_gradient(*FORM_GR)
        if f.width > 14.4:
            f.scale_to_fit_width(14.4)
        f.move_to(pos)
        return f

    def make_subs(self, s1, s2):
        l1 = Text(s1, font=ZH_FONT, font_size=32, color=SUB1_C, weight=BOLD)
        l2 = Text(s2, font=ZH_FONT, font_size=25, color=SUB2_C)
        return VGroup(l1, l2).arrange(DOWN, buff=0.32).move_to(DOWN * 2.35)

    def make_sub1(self, s1):
        return Text(s1, font=ZH_FONT, font_size=30, color=SUB1_C,
                    weight=BOLD).move_to(DOWN * 0.02)

    def morph_to(self, new_t, new_f, new_s, new_plot=None, run_time=T_RUN):
        anims = [
            ReplacementTransform(self.cur_t, new_t),
            TransformMatchingTex(self.cur_f, new_f, transform_mismatches=True),
            ReplacementTransform(self.cur_s, new_s),
        ]
        if self.cur_plot is not None:
            anims.append(FadeOut(self.cur_plot))
        if new_plot is not None:
            anims.append(FadeIn(new_plot, lag_ratio=0.06))
        if self.pending_fade:
            anims += [FadeOut(m) for m in self.pending_fade]
            self.pending_fade = []
        self.play(*anims, run_time=run_time)
        self.cur_t, self.cur_f, self.cur_s, self.cur_plot = new_t, new_f, new_s, new_plot

    def go_card(self, idx):
        name, latex, s1, s2, key = CARDS[idx]
        has_plot = key is not None
        new_t = self.make_title(name)
        new_f = self.make_formula(latex, pos=UP * 1.05 if has_plot else UP * 0.55)
        if has_plot:
            new_s = self.make_sub1(s1)
            new_plot = PLOT_BUILDERS[key](self)
        else:
            new_s = self.make_subs(s1, s2)
            new_plot = None
        self.morph_to(new_t, new_f, new_s, new_plot)
        self.wait(T_HOLD)

    # ---------- 开场 ----------
    def opening(self):
        big = VGroup(
            Text("复变函数", font=ZH_FONT, font_size=72, weight=BOLD),
            Text("邪修进阶之路", font=ZH_FONT, font_size=72, weight=BOLD),
        ).arrange(DOWN, buff=0.28)
        big[0].set_color_by_gradient("#FFD166", "#F59E62")
        big[1].set_color_by_gradient("#B79CFF", "#FF6B6B")
        big.move_to(UP * 0.7)
        sub1 = Text("一分钟 46 连发 · 从炼气到飞升", font=ZH_FONT,
                    font_size=38, color=SUB1_C, weight=BOLD).next_to(big, DOWN, buff=0.5)
        sub2 = Text("复变函数与积分变换 · 全程可视化", font=ZH_FONT,
                    font_size=26, color=SUB2_C).next_to(sub1, DOWN, buff=0.4)
        self.play(FadeIn(big[0], shift=UP * 0.3), run_time=0.4)
        self.play(FadeIn(big[1], shift=UP * 0.3), run_time=0.4)
        self.play(Write(sub1), FadeIn(sub2), run_time=0.5)
        self.wait(0.8)

        name, latex, s1, s2, key = CARDS[0]
        new_t = self.make_title(name)
        new_f = self.make_formula(latex, pos=UP * 0.55)
        new_s = self.make_subs(s1, s2)
        self.play(
            ReplacementTransform(big, new_t),
            ReplacementTransform(VGroup(sub1, sub2), new_s),
            FadeIn(new_f, shift=DOWN * 0.3),
            run_time=0.5,
        )
        self.cur_t, self.cur_f, self.cur_s, self.cur_plot = new_t, new_f, new_s, None
        self.wait(T_HOLD)

    # ---------- 主循环 ----------
    def run_cards(self):
        for i, card in enumerate(CARDS):
            if i == 0:
                continue
            self.go_card(i)

    # ---------- 结尾 ----------
    def ending(self):
        end_t = Text("点赞 · 收藏 · 关注", font=ZH_FONT, font_size=64, weight=BOLD)
        end_t.set_color_by_gradient("#FFD166", "#F59E62")
        end_t.to_edge(UP, buff=0.45)
        end_f = self.make_formula(r"P(\text{ascend})\to 1", font_size=64)
        end_s = self.make_subs("邪修之路未完待续", "下期更炫")
        self.morph_to(end_t, end_f, end_s)
        self.wait(1.6)
        self.play(FadeOut(self.cur_t), FadeOut(self.cur_f), FadeOut(self.cur_s),
                  FadeOut(self.wallpaper), run_time=0.4)

    # ================= 函数图像面板 =================
    def make_plane(self):
        pl = NumberPlane(
            x_range=[-5.4, 5.4, 1], y_range=[-1.45, 1.45, 1],
            background_line_style={"stroke_color": "#1F3A57", "stroke_width": 1.2},
            axis_config={"stroke_color": "#4A7DB5", "stroke_width": 2.5},
            faded_line_ratio=0)
        pl.move_to(PC)
        return pl

    # ----- 炼气 -----
    def p_conj(self):
        g = VGroup(self.make_plane())
        z = PC + np.array([1.4, 0.85, 0.0])
        zb = PC + np.array([1.4, -0.85, 0.0])
        g.add(Dot(z, radius=0.07, color=BLUE),
              MathTex("z", font_size=26, color=BLUE).next_to(z, UR, buff=0.08))
        g.add(Dot(zb, radius=0.07, color=RED),
              MathTex(r"\bar{z}", font_size=26, color=RED).next_to(zb, DR, buff=0.08))
        g.add(DashedLine(z, zb, color=YELLOW, stroke_width=2.5))
        g.add(Line(PC, z, color=YELLOW, stroke_width=3))
        g.add(MathTex(r"|z|", font_size=24, color=YELLOW)
              .move_to(PC + np.array([0.75, 0.55, 0.0])))
        return g

    def p_euler(self):
        g = VGroup(self.make_plane())
        R = 1.15
        g.add(Circle(radius=R, color=YELLOW, stroke_width=4).move_to(PC))
        ang = 0.95
        pnt = PC + R * np.array([np.cos(ang), np.sin(ang), 0.0])
        g.add(Line(PC, pnt, color=GREEN, stroke_width=3.5))
        g.add(Dot(pnt, radius=0.07, color=ORANGE))
        g.add(DashedLine(pnt, [pnt[0], PC[1], 0], color=BLUE, stroke_width=2.5))
        g.add(DashedLine(pnt, [PC[0], pnt[1], 0], color=RED, stroke_width=2.5))
        g.add(Arc(radius=0.42, start_angle=0, angle=ang, color=ORANGE, stroke_width=3)
              .shift(PC))
        g.add(MathTex(r"\cos\theta", font_size=22, color=BLUE)
              .move_to(PC + np.array([0.62, -0.2, 0.0])))
        g.add(MathTex(r"\sin\theta", font_size=22, color=RED)
              .move_to(PC + np.array([0.62, 0.52, 0.0])))
        return g

    def p_roots(self):
        g = VGroup(self.make_plane())
        R = 1.15
        cols = [RED, ORANGE, YELLOW, GREEN, BLUE, VIOLET]
        pts = [PC + R * np.array([np.cos(k * np.pi / 3), np.sin(k * np.pi / 3), 0.0])
               for k in range(6)]
        g.add(Circle(radius=R, color=MUTED, stroke_width=1.5).move_to(PC))
        g.add(Polygon(*pts, color=INK, stroke_width=2.5, fill_opacity=0))
        for p, col in zip(pts, cols):
            g.add(Dot(p, radius=0.08, color=col))
        return g

    # ----- 筑基 -----
    def p_cr(self):
        g = VGroup(self.make_plane())
        for r in (0.38, 0.78, 1.18):
            g.add(Circle(radius=r, color=BLUE, stroke_width=2.8).move_to(PC))
        for a in np.arange(0, 2 * np.pi, np.pi / 4):
            g.add(Line(PC, PC + 1.45 * np.array([np.cos(a), np.sin(a), 0.0]),
                       color=RED, stroke_width=2.5))
        g.add(MathTex(r"w=e^z", font_size=28, color=YELLOW)
              .move_to(PC + np.array([4.35, 1.02, 0.0])))
        return g

    def p_harm(self):
        g = VGroup()
        cols, rows = 12, 5
        cw, chh = 0.9, 0.58
        for i in range(cols):
            for j in range(rows):
                x = (i - (cols - 1) / 2) * cw
                y = (j - (rows - 1) / 2) * chh
                u = x * x - y * y
                v = max(-1.0, min(1.0, u / 4.0))
                col = interpolate_color(RED, YELLOW, (v + 1) / 2) if v < 0 else \
                    interpolate_color(YELLOW, BLUE, v)
                sq = Square(side_length=1.0, stroke_color=BG, stroke_width=1.5)
                sq.set_fill(col, opacity=0.72)
                sq.scale(np.array([cw, chh, 1.0]), about_point=ORIGIN)
                sq.move_to(PC + np.array([x, y, 0.0]))
                g.add(sq)
        g.add(MathTex(r"u=\mathrm{Re}(z^2)=x^2-y^2", font_size=26, color=INK)
              .move_to(PC + np.array([0.0, -1.68, 0.0])))
        return g

    def p_log(self):
        g = VGroup(self.make_plane())
        g.add(Line(PC + LEFT * 5.4, PC, color=RED, stroke_width=6))
        g.add(MathTex(r"\text{branch cut}", font_size=22, color=RED)
              .move_to(PC + np.array([-3.5, 0.34, 0.0])))
        prev = None
        cols = [BLUE, GREEN, RED, YELLOW]
        for th in np.linspace(0, 6.4 * np.pi, 700):
            r = 0.28 * np.exp(0.115 * th)
            x, y = r * np.cos(th), r * np.sin(th)
            if abs(y) > 1.4 or abs(x) > 5.3:
                prev = None
                continue
            q = PC + np.array([x, y, 0.0])
            c = cols[min(int(th / (2 * np.pi)), 3)]
            if prev is not None:
                g.add(Line(prev, q, color=c, stroke_width=3))
            prev = q
        return g

    # ----- 金丹 -----
    def p_cauchy(self):
        g = VGroup(self.make_plane())
        g.add(Circle(radius=1.3, color=YELLOW, stroke_width=4).move_to(PC))
        z0 = PC + np.array([0.42, 0.2, 0.0])
        g.add(Dot(z0, radius=0.07, color=RED))
        g.add(MathTex(r"z_0", font_size=26, color=RED).next_to(z0, UP, buff=0.08))
        g.add(MathTex(r"\oint_C\frac{f(z)}{z-z_0}dz=2\pi i\,f(z_0)",
                      font_size=26, color=GREEN).move_to(PC + np.array([3.3, -0.8, 0.0])))
        return g

    # ----- 元婴 -----
    def p_taylor(self):
        g = VGroup(self.make_plane())
        g.add(Line(PC + LEFT * 5.3, PC + RIGHT * 5.3, color=MUTED, stroke_width=2))
        g.add(axes_plot(lambda x: 1.1 * np.sin(0.5 * x), -5.3, 5.3, INK, dash=True, sw=3))
        g.add(axes_plot(lambda x: 0.55 * x, -2.6, 2.6, BLUE))
        g.add(axes_plot(lambda x: 0.55 * x - 0.0229 * x ** 3, -3.4, 3.4, GREEN))
        g.add(axes_plot(lambda x: 0.55 * x - 0.0229 * x ** 3 + 0.000143 * x ** 5,
                        -4.4, 4.4, ORANGE))
        g.add(MathTex(r"\sin", font_size=24, color=INK)
              .move_to(PC + np.array([4.85, 0.72, 0.0])))
        g.add(MathTex(r"n=1,3,5", font_size=24, color=GREEN)
              .move_to(PC + np.array([-4.5, -1.02, 0.0])))
        return g

    def p_laurent(self):
        g = VGroup(self.make_plane())
        outer = Circle(radius=1.38, color=YELLOW, stroke_width=4).move_to(PC)
        outer.set_fill(GREEN, opacity=0.15)
        inner = Circle(radius=0.7, color=ORANGE, stroke_width=4).move_to(PC)
        inner.set_fill(BG, opacity=1.0)
        g.add(outer, inner)
        g.add(Line(PC + np.array([-0.12, -0.12, 0]), PC + np.array([0.12, 0.12, 0]),
                   color=RED, stroke_width=3.5))
        g.add(Line(PC + np.array([-0.12, 0.12, 0]), PC + np.array([0.12, -0.12, 0]),
                   color=RED, stroke_width=3.5))
        g.add(MathTex(r"r<|z-z_0|<R", font_size=26, color=INK)
              .move_to(PC + np.array([3.35, 0.88, 0.0])))
        return g

    # ----- 化神 -----
    def p_residue(self):
        g = VGroup(self.make_plane())
        C = DashedVMobject(Circle(radius=1.15, color=ORANGE, stroke_width=4)
                           .move_to(PC), num_dashes=32)
        g.add(C)
        g.add(Line(PC + np.array([-0.12, -0.12, 0]), PC + np.array([0.12, 0.12, 0]),
                   color=RED, stroke_width=3.5))
        g.add(Line(PC + np.array([-0.12, 0.12, 0]), PC + np.array([0.12, -0.12, 0]),
                   color=RED, stroke_width=3.5))
        g.add(MathTex(r"\mathrm{Res}[f,z_0]=c_{-1}", font_size=28, color=GREEN)
              .move_to(PC + np.array([3.2, 0.62, 0.0])))
        return g

    def p_residue_thm(self):
        g = VGroup(self.make_plane())
        contour = ParametricFunction(
            lambda t: PC + np.array([
                (2.35 + 0.35 * np.sin(3 * t)) * np.cos(t),
                (1.12 + 0.22 * np.sin(2 * t)) * np.sin(t), 0.0]),
            t_range=[0, 2 * np.pi], color=YELLOW, stroke_width=5)
        g.add(contour)
        for cx, cy in [(-1.25, 0.32), (0.35, 0.58), (1.35, -0.38)]:
            g.add(Line(PC + np.array([cx - 0.09, cy - 0.09, 0]),
                       PC + np.array([cx + 0.09, cy + 0.09, 0]), color=RED, stroke_width=3.5))
            g.add(Line(PC + np.array([cx - 0.09, cy + 0.09, 0]),
                       PC + np.array([cx + 0.09, cy - 0.09, 0]), color=RED, stroke_width=3.5))
        g.add(MathTex(r"2\pi i\sum\mathrm{Res}", font_size=28, color=GREEN)
              .move_to(PC + np.array([3.95, -0.85, 0.0])))
        g.add(Arc(radius=0.55, start_angle=0.4, angle=1.5, color=ORANGE, stroke_width=3)
              .move_to(PC + np.array([1.95, 0.78, 0.0])))
        return g

    # ----- 渡劫 / 飞升 -----
    def p_fta(self):
        g = VGroup(self.make_plane())
        R = 1.15
        ang = [0.3, 1.1, 2.0, 3.4, 4.6]
        cols = [RED, ORANGE, YELLOW, GREEN, BLUE]
        for a, col in zip(ang, cols):
            g.add(Dot(PC + R * np.array([np.cos(a), np.sin(a), 0.0]),
                      radius=0.08, color=col))
        g.add(MathTex(r"n=5", font_size=28, color=GREEN)
              .move_to(PC + np.array([4.4, 1.0, 0.0])))
        return g

    def p_conformal(self):
        g = VGroup(self.make_plane())
        pal = [RED, ORANGE, YELLOW, GREEN, BLUE, VIOLET]
        k = 0
        for i in range(3):
            for j in range(3):
                x = -3.7 + i * 0.54
                y = 0.95 - j * 0.54
                sq = Square(side_length=1.0, stroke_color=INK, stroke_width=1.5)
                sq.set_fill(pal[k % 6], opacity=0.42)
                sq.scale(np.array([0.54, 0.54, 1.0]), about_point=ORIGIN)
                sq.move_to(PC + np.array([x, y, 0.0]))
                g.add(sq)
                k += 1
        g.add(MathTex(r"z", font_size=28, color=INK).move_to(PC + np.array([-5.0, 1.22, 0.0])))
        g.add(Arrow(PC + np.array([-1.15, 0.0, 0.0]), PC + np.array([0.55, 0.0, 0.0]),
                    color=YELLOW, stroke_width=4))
        g.add(MathTex(r"w=z^2", font_size=28, color=YELLOW)
              .move_to(PC + np.array([-0.3, 0.4, 0.0])))
        pal2 = [RED, ORANGE, GREEN, BLUE]
        for i, u0 in enumerate([0.35, 0.7, 1.05]):
            g.add(ParametricFunction(
                lambda t, u0=u0: PC + np.array([
                    (u0 * u0 - t * t) * 0.62, 2 * u0 * t * 0.62, 0.0]),
                t_range=[-1.05, 1.05], color=pal2[i], stroke_width=3))
        for i, v0 in enumerate([0.35, 0.7, 1.05]):
            g.add(ParametricFunction(
                lambda t, v0=v0: PC + np.array([
                    (t * t - v0 * v0) * 0.62, 2 * t * v0 * 0.62, 0.0]),
                t_range=[-1.1, 1.1], color=pal2[(i + 2) % 4], stroke_width=3))
        g.add(MathTex(r"w", font_size=28, color=INK).move_to(PC + np.array([4.95, 1.22, 0.0])))
        return g

    # ----- 飞升 -----
    def p_fourier(self):
        g = VGroup(self.make_plane())
        g.add(Line(PC + LEFT * 5.3, PC + RIGHT * 5.3, color=MUTED, stroke_width=2))
        x = -5.2
        level = 1.0
        while x < 5.2:
            nx = min(x + 1.5, 5.2)
            g.add(Line(PC + np.array([x, level * 1.2, 0]),
                       PC + np.array([nx, level * 1.2, 0]), color=INK, stroke_width=2.5))
            if nx < 5.2:
                g.add(Line(PC + np.array([nx, level * 1.2, 0]),
                           PC + np.array([nx, -level * 1.2, 0]), color=INK, stroke_width=2.5))
            level = -level
            x = nx

        def S(n):
            return lambda xx: sum(
                (4 * 0.8) / (np.pi * (2 * j + 1)) * np.sin((2 * j + 1) * (2 * np.pi / 3) * xx)
                for j in range(n))
        g.add(axes_plot(S(1), -5.3, 5.3, BLUE))
        g.add(axes_plot(lambda xx: S(2)(xx), -5.3, 5.3, ORANGE))
        g.add(axes_plot(lambda xx: S(3)(xx), -5.3, 5.3, GREEN))
        g.add(axes_plot(lambda xx: S(5)(xx), -5.3, 5.3, RED))
        return g

    def p_ftpair(self):
        g = VGroup(self.make_plane())
        g.add(Line(PC + LEFT * 5.2, PC + LEFT * 0.5, color=MUTED, stroke_width=2))
        g.add(Line(PC + RIGHT * 0.5, PC + RIGHT * 5.2, color=MUTED, stroke_width=2))
        gl = axes_plot(lambda t: 1.32 * np.exp(-t * t / 0.45), -2.6, 2.6, RED)
        gl.shift(LEFT * 2.85)
        gr = axes_plot(lambda w: 0.95 * np.exp(-w * w / 3.6), -4.6, 4.6, BLUE)
        gr.shift(RIGHT * 2.85)
        g.add(gl, gr)
        g.add(MathTex(r"f(t)", font_size=26, color=RED).move_to(PC + np.array([-4.9, 1.0, 0.0])))
        g.add(MathTex(r"F(\omega)", font_size=26, color=BLUE).move_to(PC + np.array([4.7, 1.0, 0.0])))
        g.add(MathTex(r"\mathcal{F}", font_size=30, color=YELLOW).move_to(PC + np.array([0.0, 0.85, 0.0])))
        g.add(Arrow(PC + np.array([-0.75, 0.4, 0.0]), PC + np.array([0.75, 0.4, 0.0]),
                    color=YELLOW, stroke_width=3.5))
        return g

    def p_kk(self):
        g = VGroup(self.make_plane())
        g.add(Line(PC + LEFT * 5.3, PC + RIGHT * 5.3, color=MUTED, stroke_width=2))
        g.add(axes_plot(lambda w: 1.25 / (1 + w * w), -5.3, 5.3, BLUE))
        g.add(axes_plot(lambda w: -2.6 * w / ((1 + w * w) ** 2), -5.3, 5.3, RED))
        g.add(MathTex(r"\mathrm{Re}F", font_size=26, color=BLUE)
              .move_to(PC + np.array([-4.55, 0.92, 0.0])))
        g.add(MathTex(r"\mathrm{Im}F", font_size=26, color=RED)
              .move_to(PC + np.array([4.55, -0.98, 0.0])))
        return g


PLOT_BUILDERS = {
    "euler": ComplexMix.p_euler,
    "roots": ComplexMix.p_roots,
    "cr": ComplexMix.p_cr,
    "harm": ComplexMix.p_harm,
    "log": ComplexMix.p_log,
    "cauchy": ComplexMix.p_cauchy,
    "taylor": ComplexMix.p_taylor,
    "laurent": ComplexMix.p_laurent,
    "residue": ComplexMix.p_residue,
    "residue_thm": ComplexMix.p_residue_thm,
    "fta": ComplexMix.p_fta,
    "conformal": ComplexMix.p_conformal,
    "fourier": ComplexMix.p_fourier,
    "ftpair": ComplexMix.p_ftpair,
    "kk": ComplexMix.p_kk,
}
