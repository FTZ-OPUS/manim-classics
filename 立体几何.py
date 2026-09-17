"""立体几何邪修之路 — 36 神式公式混剪（双层卡片：公式+绘图）
节奏：1.0s/卡（T_RUN=0.45 + T_HOLD=0.55），总时长 ≈ 36 + 开场结尾 ≈ 38.8s
"""
from manim import *
import numpy as np
import random

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16.0
config.frame_height = 9.0
config.background_color = "#050505"

T_RUN = 0.45
T_HOLD = 0.55
PC = DOWN * 1.75          # 绘图面板中心
KAI = "Kaiti SC"

# ---------------- 伪 3D 投影（绘图层） ----------------
YAW = 0.52

def unit3(v):
    v = np.asarray(v, float)
    return v / np.linalg.norm(v)

def pr(p):
    x, y, z = float(p[0]), float(p[1]), float(p[2])
    xr = x * np.cos(YAW) - y * np.sin(YAW)
    yr = x * np.sin(YAW) + y * np.cos(YAW)
    return np.array([xr, z - 0.32 * yr, 0.0])

PAL = ["#4FC3F7", "#FFD166", "#66D19E", "#F06292", "#FF8A50", "#BA68C8"]
GREY = "#5A6B7A"

def fitc(g, max_w=5.6, max_h=2.35, center=PC):
    w, h = g.width, g.height
    if w > 0 and h > 0:
        s = min(max_w / w, max_h / h)
        if s < 1:
            g.scale(s)
    g.move_to(center)
    return g

def wire(pts, edges, hidden=(), dots=True, sw=4.0, colors=None):
    g = VGroup()
    for i, j in hidden:
        g.add(DashedVMobject(Line(pr(pts[i]), pr(pts[j]), color=GREY, stroke_width=2.2), num_dashes=16))
    for k, (i, j) in enumerate(edges):
        col = (colors[k % len(colors)] if colors else PAL[k % len(PAL)])
        g.add(Line(pr(pts[i]), pr(pts[j]), color=col, stroke_width=sw))
    if dots:
        for p in pts:
            g.add(Dot(pr(p), radius=0.05, color="#FFE082"))
    return g

def arrow3(p, q, color, sw=5.0):
    return Arrow(pr(p), pr(q), buff=0, color=color, stroke_width=sw,
                 max_tip_length_to_length_ratio=0.24)

def arc3(c, u, v, r, color, sw=3.5):
    u, v = unit3(u), unit3(v)
    om = float(np.arccos(np.clip(np.dot(u, v), -1, 1)))
    if om < 1e-6:
        om = 1e-6
    def fn(t):
        s = (np.sin((1 - t) * om) * u + np.sin(t * om) * v) / np.sin(om)
        return pr(np.asarray(c, float) + r * unit3(s))
    return ParametricFunction(fn, t_range=[0, om], color=color, stroke_width=sw)

CUBE = [(-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
        (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)]
CUBE_E = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4),
          (0, 4), (1, 5), (2, 6), (3, 7)]
TETRA = [(0.85, 0.85, 0.85), (0.85, -0.85, -0.85), (-0.85, 0.85, -0.85), (-0.85, -0.85, 0.85)]
TETRA_E = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

# ---------------- 数据：36 神式 (境界, 名称, 公式, 副标题1, 副标题2, 绘图键) ----------------
CARDS = [
    ("炼气", "球的体积", r"V=\frac{4}{3}\pi R^{3}", "炼气·第一神式", "立体几何的地基", "sph"),
    ("炼气", "球的表面积", r"S=4\pi R^{2}", "炼气·表里生辉", "四个大圆面积总和", "sph_surf"),
    ("炼气", "锥体体积", r"V=\frac{1}{3}Sh", "炼气·削峰填谷", "祖暅原理可证", "cone"),
    ("炼气", "台体体积", r"V=\frac{h}{3}\left(S+\sqrt{SS'}+S'\right)", "炼气·截台之术", "上下底面积的调和", "frust"),
    ("炼气", "球冠面积", r"S=2\pi Rh", "炼气·冠冕之术", "只算球面一角", "sph_cap"),
    ("炼气", "球缺体积", r"V=\pi h^{2}\left(R-\frac{h}{3}\right)", "炼气·藏锋于鞘", "球缺即球冠之体", "sph_seg"),
    ("炼气", "椭球体积", r"V=\frac{4}{3}\pi abc", "炼气·椭圆升维", "三轴相乘即成积", "ell"),
    ("筑基", "欧拉公式", r"V-E+F=2", "筑基·万形之律", "凸多面体皆服从", "cube"),
    ("筑基", "线面角公式", r"\sin\theta=\frac{\left|\vec{v}\cdot\vec{n}\right|}{\left|\vec{v}\right|\left|\vec{n}\right|}", "筑基·法向一击", "线面角一步到位", "line_plane"),
    ("筑基", "点面距公式", r"d=\frac{\left|\overrightarrow{AP}\cdot\vec{n}\right|}{\left|\vec{n}\right|}", "筑基·垂线测深", "平面方程直读距离", "pt_plane"),
    ("筑基", "等体积法", r"d=\frac{3V}{S}", "筑基·剁锥求距", "换底求高神技", "d_vol"),
    ("筑基", "面积射影定理", r"S'=S\cos\theta", "筑基·投影缩面", "斜面面积打余弦折", "proj_area"),
    ("筑基", "最小角定理", r"\cos\varphi=\cos\theta_{1}\cos\theta_{2}", "筑基·三余弦锁角", "斜线夹角的最小值", "min_angle"),
    ("筑基", "方向余弦", r"\cos^{2}\alpha+\cos^{2}\beta+\cos^{2}\gamma=1", "筑基·三方归一", "对角线与三棱的夹角", "dir_cos"),
    ("金丹", "异面直线夹角", r"\cos\theta=\frac{\left|\vec{a}\cdot\vec{b}\right|}{\left|\vec{a}\right|\left|\vec{b}\right|}", "金丹·平移共面", "异面化相交再算", "skew"),
    ("金丹", "二面角法向量", r"\cos\theta=\frac{\left|\vec{n}_{1}\cdot\vec{n}_{2}\right|}{\left|\vec{n}_{1}\right|\left|\vec{n}_{2}\right|}", "金丹·双法向对撞", "锐二面角取绝对值", "dih"),
    ("金丹", "向量叉乘", r"\left|\vec{a}\times\vec{b}\right|=\left|\vec{a}\right|\left|\vec{b}\right|\sin\theta", "金丹·右手法则", "法向量的生产机器", "cross"),
    ("金丹", "向量混合积", r"\left[\vec{a},\vec{b},\vec{c}\right]=\vec{a}\cdot\left(\vec{b}\times\vec{c}\right)", "金丹·三向定积", "平行六面体之源", "mixed"),
    ("金丹", "四面体体积", r"V=\frac{1}{6}\left|\vec{a}\cdot\left(\vec{b}\times\vec{c}\right)\right|", "金丹·六分混积", "三条棱定死体积", "tetra_vol"),
    ("金丹", "异面直线距离", r"d=\frac{\left|\left(\vec{a}\times\vec{b}\right)\cdot\overrightarrow{AB}\right|}{\left|\vec{a}\times\vec{b}\right|}", "金丹·公垂收割", "叉乘除完即距离", "skew_dist"),
    ("元婴", "球的截面", r"d^{2}+r^{2}=R^{2}", "元婴·截圆定理", "球心距锁死小圆", "cut"),
    ("元婴", "补形模型", r"R=\frac{\sqrt{a^{2}+b^{2}+c^{2}}}{2}", "元婴·墙角补形", "装进长方体就赢", "box_model"),
    ("元婴", "棱锥外接球", r"R=\frac{h^{2}+r^{2}}{2h}", "元婴·轴上寻心", "球心必在高线上", "pysph"),
    ("元婴", "直棱柱外接球", r"R^{2}=r^{2}+\frac{h^{2}}{4}", "元婴·柱中藏球", "上下底心对中点", "prism_sph"),
    ("元婴", "内切球公式", r"r=\frac{3V}{S}", "元婴·等积掏球", "S 为全面积", "in_sph"),
    ("元婴", "正四面体双球", r"R=\frac{\sqrt{6}}{4}a\qquad r=\frac{\sqrt{6}}{12}a", "元婴·正四双球", "外接恒为内切三倍", "tet2"),
    ("元婴", "正四面体高与体", r"h=\frac{\sqrt{6}}{3}a\qquad V=\frac{\sqrt{2}}{12}a^{3}", "元婴·棱上四分", "球心分高三比一", "tetra_hv"),
    ("化神", "三面角余弦定理", r"\cos\gamma=\cos\alpha\cos\beta+\sin\alpha\sin\beta\cos C", "化神·球面余弦", "不建系秒二面角", "tri"),
    ("化神", "二面角万能公式", r"\cos C=\frac{\cos\gamma-\cos\alpha\cos\beta}{\sin\alpha\sin\beta}", "化神·万能公式", "三面角反求二面角", "dih_all"),
    ("化神", "三面角正弦定理", r"\frac{\sin\alpha}{\sin A}=\frac{\sin\beta}{\sin B}=\frac{\sin\gamma}{\sin C}", "化神·球面正弦", "面角对二面角", "sin_tri"),
    ("化神", "斯坦纳定理", r"\cos\theta=\cos\theta_{1}\cos\theta_{2}\cos\theta_{3}+\sin\theta_{1}\sin\theta_{2}", "化神·射影锁角", "同侧取正异侧取负", "stn"),
    ("渡劫", "四面体余弦定理", r"\cos\theta=\frac{\left|AC^{2}+BD^{2}-AD^{2}-BC^{2}\right|}{2\,AB\cdot CD}", "渡劫·对棱一式", "对棱夹角一步封喉", "opp"),
    ("渡劫", "张角定理空间版", r"\frac{PE}{AE}=\frac{V_{PBCD}}{V_{ABCD}}", "渡劫·体积张角", "张角定理登空间", "zj"),
    ("渡劫", "四面体中线定理", r"9m_{A}^{2}=3\left(AB^{2}+AC^{2}+AD^{2}\right)-\left(BC^{2}+BD^{2}+CD^{2}\right)", "渡劫·中线九式", "阿波罗尼奥斯升维", "med"),
    ("登神", "欧拉四面体公式", r"36V^{2}=\det G\qquad G=\left(\vec{a}_{i}\cdot\vec{a}_{j}\right)_{3\times 3}", "登神·格拉姆行列式", "三棱定死四面体", "gram_det"),
    ("登神", "凯莱-门格公式", r"288V^{2}=\det\begin{vmatrix}0&1&1&1&1\\1&0&a^{2}&b^{2}&c^{2}\\1&a^{2}&0&f^{2}&e^{2}\\1&b^{2}&f^{2}&0&d^{2}\\1&c^{2}&e^{2}&d^{2}&0\end{vmatrix}", "登神·六棱入阵封神", "六棱定死四面体", "cm"),
]

WALLPAPER = [
    r"V=\frac{4}{3}\pi R^{3}", r"S=4\pi R^{2}", r"\vec{n}_{1}\cdot\vec{n}_{2}", r"V-E+F=2",
    r"\frac{h^{2}+r^{2}}{2h}", r"d^{2}+r^{2}=R^{2}", r"\vec{a}\times\vec{b}", r"\det G",
    r"\cos\gamma=\cos\alpha\cos\beta", r"\sin\theta", r"\sqrt{6}\,a", r"R=3r",
    r"\frac{\sqrt{2}}{2}a", r"288V^{2}", r"\sin\alpha\sin\beta\cos C", r"\frac{3V}{S}",
    r"\theta\in\left[0,\frac{\pi}{2}\right]", r"\vec{a}\cdot\left(\vec{b}\times\vec{c}\right)",
    r"\cos^{2}\alpha+\cos^{2}\beta", r"OA\perp\alpha", r"l_{1}\parallel l_{2}", r"\angle AOB",
    r"\frac{1}{3}Sh", r"\pi R^{2}", r"\perp", r"\cong", r"PE\cdot AE", r"\sin\frac{\alpha}{2}",
]


class LitiGod(Scene):
    # ---------- 基础构件 ----------
    def make_plane(self):
        return NumberPlane(
            x_range=[-5.4, 5.4, 1], y_range=[-1.45, 1.45, 1],
            background_line_style={"stroke_color": "#1F3A57", "stroke_width": 1.2},
            axis_config={"stroke_color": "#4A7DB5", "stroke_width": 2.5},
            faded_line_ratio=0).move_to(PC)

    def panel(self, d):
        return VGroup(self.make_plane(), fitc(d))

    def make_title(self, realm, name):
        pre = Text(realm, font=KAI, weight=BOLD, font_size=60, color="#CDDC39")
        sep = Text("·", font=KAI, weight=BOLD, font_size=60, color="#CDDC39")
        main = Text(name, font=KAI, weight=BOLD, font_size=60)
        main.set_color_by_gradient("#FFD166", "#F59E62")
        return VGroup(pre, sep, main).arrange(RIGHT, buff=0.10).to_edge(UP, buff=0.45)

    def make_formula(self, latex, pos, max_h=None):
        f = MathTex(latex, font_size=64, stroke_width=1.2)
        if f.width > 14.4:
            f.scale_to_fit_width(14.4)
        if max_h is not None and f.height > max_h:
            f.scale_to_fit_height(max_h)
        f.set_color_by_gradient("#FF8A50", "#FFD166")
        f.move_to(pos)
        return f

    def make_subs(self, s1, s2):
        l1 = Text(s1, font=KAI, weight=BOLD, font_size=34, color="#66D19E")
        l2 = Text(s2, font=KAI, font_size=26, color="#4DB6AC")
        return VGroup(l1, l2).arrange(DOWN, buff=0.20).move_to(DOWN * 2.35)

    def make_sub1(self, s1):
        return Text(s1, font=KAI, weight=BOLD, font_size=34, color="#66D19E").move_to(DOWN * 3.72)

    def add_wallpaper(self):
        rng = random.Random(20260911)
        for s in WALLPAPER:
            m = MathTex(s, font_size=rng.uniform(34, 48), color="#7A8794").set_opacity(0.10)
            m.move_to([rng.uniform(-7.1, 7.1), rng.uniform(-4, 4), 0])
            m.rotate(rng.uniform(-0.12, 0.12))
            self.add(m)

    # ---------- 转场 ----------
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
        self.play(*anims, run_time=run_time)

    def go_card(self, idx):
        realm, name, latex, s1, s2, key = CARDS[idx]
        has_plot = key is not None
        new_t = self.make_title(realm, name)
        new_f = self.make_formula(latex, UP * 1.05 if has_plot else UP * 0.55,
                                  max_h=2.0 if has_plot else None)
        new_s = self.make_sub1(s1) if has_plot else self.make_subs(s1, s2)
        new_plot = getattr(self, "p_" + key)() if has_plot else None
        if self.cur_f is None:  # 首卡：公式 FadeIn 进场
            anims = [ReplacementTransform(self.cur_t, new_t),
                     FadeIn(new_f, shift=DOWN * 0.3),
                     ReplacementTransform(self.cur_s, new_s)]
            if new_plot is not None:
                anims.append(FadeIn(new_plot, lag_ratio=0.06))
            self.play(*anims, run_time=T_RUN)
        else:
            self.morph_to(new_t, new_f, new_s, new_plot)
        self.cur_t, self.cur_f, self.cur_s, self.cur_plot = new_t, new_f, new_s, new_plot
        self.wait(T_HOLD)

    # ---------- 绘图库（16 图） ----------
    def p_sph(self):
        d = VGroup()
        d.add(Circle(radius=1.35, color="#4FC3F7", stroke_width=4))
        d.add(DashedVMobject(Ellipse(width=2.7, height=0.86, color="#4FC3F7", stroke_width=2.5), num_dashes=30))
        d.add(DashedVMobject(Ellipse(width=1.7, height=2.62, color="#1E5F8A", stroke_width=2), num_dashes=34))
        d.add(Line(ORIGIN, 1.35 * RIGHT, color="#FFD166", stroke_width=4.5))
        d.add(Dot(ORIGIN, radius=0.05, color="#FFE082"), Dot(1.35 * RIGHT, radius=0.05, color="#FFE082"))
        return self.panel(d)

    def p_cone(self):
        d = VGroup()
        apex = np.array([0.0, 0.0, 1.15]); cb = np.array([0.0, 0.0, -0.85]); r = 1.05
        d.add(Ellipse(width=2 * r, height=2 * r * 0.34, color="#4FC3F7", stroke_width=3.5).move_to(pr(cb)))
        d.add(Line(pr(apex), pr(cb) + LEFT * r, color="#FFD166", stroke_width=4.5))
        d.add(Line(pr(apex), pr(cb) + RIGHT * r, color="#FF8A50", stroke_width=4.5))
        d.add(DashedVMobject(Line(pr(apex), pr(cb), color="#66D19E", stroke_width=3), num_dashes=12))
        d.add(Dot(pr(apex), radius=0.055, color="#FFE082"), Dot(pr(cb), radius=0.05, color="#FFE082"))
        return self.panel(d)

    def p_ell(self):
        d = VGroup()
        d.add(Ellipse(width=3.3, height=2.0, color="#4FC3F7", stroke_width=4))
        d.add(DashedVMobject(Ellipse(width=3.3, height=0.92, color="#66D19E", stroke_width=2.5), num_dashes=30))
        d.add(DashedVMobject(Line(UP * 1.0, DOWN * 1.0, color="#F06292", stroke_width=2.5), num_dashes=14))
        for p in [1.65 * RIGHT, 1.65 * LEFT, UP * 1.0, DOWN * 1.0]:
            d.add(Dot(p, radius=0.045, color="#FFE082"))
        return self.panel(d)

    def p_cube(self):
        return self.panel(wire(CUBE, CUBE_E, hidden=[(0, 1), (0, 3), (0, 4)]))

    def p_skew(self):
        d = VGroup()
        d.add(wire(CUBE, CUBE_E, dots=False, sw=2.2, colors=[GREY]))
        d.add(arrow3(CUBE[0], CUBE[1], "#FF5252", sw=6))
        d.add(arrow3(CUBE[3], CUBE[7], "#40C4FF", sw=6))
        d.add(MathTex(r"\vec{a}", font_size=30, color="#FF5252").move_to(pr(CUBE[1]) + DOWN * 0.28))
        d.add(MathTex(r"\vec{b}", font_size=30, color="#40C4FF").move_to(pr(CUBE[7]) + RIGHT * 0.35 + UP * 0.12))
        return self.panel(d)

    def p_dih(self):
        d = VGroup()
        phi = 2.0
        q1 = [(0, 0, 0), (2.4, 0, 0), (2.4, 1.5, 0), (0, 1.5, 0)]
        q2 = [(0, 0, 0), (2.4, 0, 0),
              (2.4, 1.5 * np.cos(phi), 1.5 * np.sin(phi)),
              (0, 1.5 * np.cos(phi), 1.5 * np.sin(phi))]
        d.add(Polygon(*[pr(p) for p in q1], fill_color="#1E88E5", fill_opacity=0.22,
                      stroke_color="#4FC3F7", stroke_width=3))
        d.add(Polygon(*[pr(p) for p in q2], fill_color="#00897B", fill_opacity=0.22,
                      stroke_color="#66D19E", stroke_width=3))
        d.add(Line(pr((0, 0, 0)), pr((2.4, 0, 0)), color="#FFD166", stroke_width=5))
        c1 = np.array([1.2, 0.75, 0.0])
        c2 = np.array([1.2, 0.75 * np.cos(phi), 0.75 * np.sin(phi)])
        n1 = np.array([0, 0, 1.0])
        n2 = np.array([0, -np.sin(phi), np.cos(phi)])
        d.add(arrow3(c1, c1 + 0.85 * n1, "#FFD166", sw=4))
        d.add(arrow3(c2, c2 + 0.85 * n2, "#F06292", sw=4))
        d.add(arc3((0.55, 0, 0), (0, 1, 0), (0, np.cos(phi), np.sin(phi)), 0.5, "#FFD166"))
        return self.panel(d)

    def p_cross(self):
        d = VGroup()
        a = np.array([1.9, 0.25, 0.15]); b = np.array([0.35, 1.75, 0.35])
        c = unit3(np.cross(a, b)) * 1.65
        d.add(Polygon(pr(ORIGIN), pr(a), pr(a + b), pr(b),
                      fill_color="#37474F", fill_opacity=0.35, stroke_width=2, stroke_color="#78909C"))
        d.add(arrow3(ORIGIN, a, "#4FC3F7", sw=5))
        d.add(arrow3(ORIGIN, b, "#66D19E", sw=5))
        d.add(arrow3(ORIGIN, c, "#FF5252", sw=5.5))
        d.add(MathTex(r"\vec{a}", font_size=30, color="#4FC3F7").move_to(pr(a) + RIGHT * 0.32 + DOWN * 0.1))
        d.add(MathTex(r"\vec{b}", font_size=30, color="#66D19E").move_to(pr(b) + UP * 0.28))
        d.add(MathTex(r"\vec{a}\times\vec{b}", font_size=30, color="#FF5252").move_to(pr(c) + RIGHT * 0.95))
        d.add(Dot(pr(ORIGIN), radius=0.05, color="#FFE082"))
        return self.panel(d)

    def p_mixed(self):
        d = VGroup()
        a = np.array([1.75, 0.25, 0.10]); b = np.array([0.30, 1.65, 0.20]); c = np.array([0.15, 0.30, 1.40])
        V = {"O": np.zeros(3), "a": a, "b": b, "c": c, "ab": a + b, "ac": a + c, "bc": b + c, "abc": a + b + c}
        d.add(Polygon(pr(V["O"]), pr(V["a"]), pr(V["ab"]), pr(V["b"]),
                      fill_color="#37474F", fill_opacity=0.18, stroke_width=0))
        for k1, k2, col, sw in [("O", "a", "#4FC3F7", 5), ("O", "b", "#66D19E", 5), ("O", "c", "#FF5252", 5),
                                ("a", "ab", GREY, 2.2), ("b", "ab", GREY, 2.2), ("a", "ac", GREY, 2.2),
                                ("c", "ac", GREY, 2.2), ("b", "bc", GREY, 2.2), ("c", "bc", GREY, 2.2),
                                ("ab", "abc", GREY, 2.2), ("ac", "abc", GREY, 2.2), ("bc", "abc", GREY, 2.2)]:
            d.add(Line(pr(V[k1]), pr(V[k2]), color=col, stroke_width=sw))
        d.add(Dot(pr(V["O"]), radius=0.055, color="#FFE082"))
        return self.panel(d)

    def p_cut(self):
        d = VGroup()
        d.add(Circle(radius=1.35, color="#4FC3F7", stroke_width=4))
        sec = Ellipse(width=2.26, height=0.66, color="#66D19E", stroke_width=3.5).move_to(UP * 0.45)
        d.add(sec)
        d.add(DashedVMobject(Line(ORIGIN, UP * 0.45, color="#FFD166", stroke_width=3.5), num_dashes=10))
        d.add(Line(UP * 0.45, UP * 0.45 + RIGHT * 1.13, color="#F06292", stroke_width=4))
        d.add(Dot(ORIGIN, radius=0.05, color="#FFE082"), Dot(UP * 0.45, radius=0.05, color="#FFE082"))
        d.add(MathTex(r"d", font_size=28, color="#FFD166").move_to(RIGHT * 0.30 + UP * 0.24))
        d.add(MathTex(r"r", font_size=28, color="#F06292").move_to(UP * 0.45 + RIGHT * 0.55 + UP * 0.34))
        return self.panel(d)

    def p_pysph(self):
        d = VGroup()
        d.add(Circle(radius=1.5, color="#FF8A50", stroke_width=4).move_to(UP * 0.12))
        d.add(Ellipse(width=2.1, height=0.62, color="#4FC3F7", stroke_width=3.5).move_to(DOWN * 0.85))
        d.add(Line(np.array([0, 0.72, 0]), np.array([-1.05, -0.85, 0]), color="#FFD166", stroke_width=4))
        d.add(Line(np.array([0, 0.72, 0]), np.array([1.05, -0.85, 0]), color="#FF8A50", stroke_width=4))
        d.add(DashedVMobject(Line(np.array([0, -0.85, 0]), np.array([0, 0.72, 0]),
                                  color="#66D19E", stroke_width=3), num_dashes=12))
        d.add(Dot(np.array([0, 0.72, 0]), radius=0.055, color="#FFE082"))
        d.add(Dot(np.array([0, -0.85, 0]), radius=0.05, color="#FFE082"))
        d.add(Dot(np.array([0, 0.12, 0]), radius=0.05, color="#F06292"))
        return self.panel(d)

    def p_tet2(self):
        d = VGroup()
        d.add(wire(TETRA, TETRA_E, sw=3.8))
        d.add(Circle(radius=1.42, color="#FF8A50", stroke_width=3.5).move_to(UP * 0.05))
        d.add(DashedVMobject(Circle(radius=0.474, color="#66D19E", stroke_width=3).move_to(UP * 0.05), num_dashes=44))
        return self.panel(d)

    def p_tri(self):
        d = VGroup()
        L, el = 3.4, np.radians(32)
        P = []
        for az_deg in (88, 208, 328):
            az = np.radians(az_deg)
            P.append(np.array([L*np.cos(el)*np.cos(az), L*np.cos(el)*np.sin(az), L*np.sin(el)]))
        ray_c = ["#FF5252", "#40C4FF", "#69F0AE"]
        arc_c = ["#FFD166", "#F06292", "#BA68C8"]
        lb = [r"\alpha", r"\beta", r"\gamma"]
        for p, col in zip(P, ray_c):
            d.add(Line(pr(ORIGIN), pr(p), color=col, stroke_width=5.5))
        for k in range(3):
            u, v = P[k], P[(k+1) % 3]
            d.add(arc3(ORIGIN, u, v, 0.98, arc_c[k], sw=3))
            d.add(MathTex(lb[k], font_size=32, color=arc_c[k])
                  .move_to(pr(unit3(u + v) * (0.66 * L))))
        d.add(Dot(pr(ORIGIN), radius=0.06, color="#FFE082"))
        return self.panel(d)

    def p_stn(self):
        d = VGroup()
        quad = [(-2.3, -1.2, 0), (1.9, -1.2, 0), (2.7, 1.2, 0), (-1.5, 1.2, 0)]
        d.add(Polygon(*[pr(p) for p in quad], fill_color="#263238", fill_opacity=0.55,
                      stroke_color=GREY, stroke_width=2.5))
        P1 = np.array([-0.9, 0.15, 0.0]); d1 = np.array([0.75, 0.20, 0.95])
        P2 = np.array([0.95, -0.10, 0.0]); d2 = np.array([-0.25, 0.65, 0.80])
        d.add(arrow3(P1, P1 + d1, "#FF5252", sw=5))
        d.add(arrow3(P2, P2 + d2, "#40C4FF", sw=5))
        d.add(DashedVMobject(Line(pr(P1 + d1), pr(P1 + np.array([d1[0], d1[1], 0])),
                                  color=GREY, stroke_width=2.5), num_dashes=10))
        d.add(DashedVMobject(Line(pr(P2 + d2), pr(P2 + np.array([d2[0], d2[1], 0])),
                                  color=GREY, stroke_width=2.5), num_dashes=10))
        d.add(DashedVMobject(Line(pr(ORIGIN), pr(ORIGIN + np.array([0, 0, 1.8])),
                                  color="#66D19E", stroke_width=2.5), num_dashes=14))
        d.add(arc3(P1, d1, np.array([d1[0], d1[1], 0]), 0.5, "#FFD166"))
        d.add(arc3(P2, d2, np.array([d2[0], d2[1], 0]), 0.5, "#FFD166"))
        d.add(Dot(pr(P1), radius=0.045, color="#FFE082"), Dot(pr(P2), radius=0.045, color="#FFE082"))
        return self.panel(d)

    def p_opp(self):
        d = VGroup()
        d.add(wire(TETRA, TETRA_E, dots=False, sw=2.4, colors=["#78909C"]))
        d.add(Line(pr(TETRA[0]), pr(TETRA[1]), color="#FF5252", stroke_width=6))
        d.add(Line(pr(TETRA[2]), pr(TETRA[3]), color="#40C4FF", stroke_width=6))
        d.add(*[Dot(pr(p), radius=0.05, color="#FFE082") for p in TETRA])
        for k, ch, off in [(0, "A", DOWN * 0.26 + LEFT * 0.1), (1, "B", DOWN * 0.26 + RIGHT * 0.1),
                           (2, "C", UP * 0.26), (3, "D", DOWN * 0.3)]:
            d.add(MathTex(ch, font_size=28, color="#FFE082").move_to(pr(TETRA[k]) + off))
        return self.panel(d)

    def p_zj(self):
        d = VGroup()
        T = [(0.9, 0.9, 0.9), (0.9, -0.9, -0.9), (-0.9, 0.9, -0.9), (-0.9, -0.9, 0.9)]
        A, B, C, D = T
        E = (np.array(B) + np.array(C) + np.array(D)) / 3
        P = np.array(A) + 0.62 * (E - np.array(A))
        d.add(Polygon(pr(B), pr(C), pr(D), fill_color="#00897B", fill_opacity=0.20,
                      stroke_color="#26A69A", stroke_width=2.5))
        d.add(wire(T, TETRA_E, dots=False, sw=2.6, colors=["#90A4AE"]))
        d.add(Line(pr(A), pr(P), color="#FF5252", stroke_width=5))
        d.add(DashedVMobject(Line(pr(P), pr(E), color="#FFD166", stroke_width=3.5), num_dashes=10))
        d.add(*[Dot(pr(p), radius=0.05, color="#FFE082") for p in T])
        d.add(Dot(pr(P), radius=0.055, color="#FF5252"), Dot(pr(E), radius=0.055, color="#FFD166"))
        d.add(MathTex("P", font_size=28, color="#FF5252").move_to(pr(P) + LEFT * 0.3))
        d.add(MathTex("E", font_size=28, color="#FFD166").move_to(pr(E) + DOWN * 0.3))
        return self.panel(d)

    def p_cm(self):
        return self.panel(wire([(0.95, 0.95, 0.95), (0.95, -0.95, -0.95),
                                (-0.95, 0.95, -0.95), (-0.95, -0.95, 0.95)],
                               TETRA_E, sw=5.5))

    def p_sph_surf(self):
        d = VGroup()
        R = 1.35
        d.add(Circle(radius=R, color="#4FC3F7", stroke_width=3.5))
        d.add(DashedVMobject(Ellipse(width=2 * R, height=0.86, color="#4FC3F7", stroke_width=2.2), num_dashes=30))
        d.add(DashedVMobject(Ellipse(width=2 * R * 0.86, height=0.55, color="#66D19E", stroke_width=2).move_to(UP * 0.65), num_dashes=22))
        d.add(DashedVMobject(Ellipse(width=2 * R * 0.86, height=0.55, color="#66D19E", stroke_width=2).move_to(DOWN * 0.65), num_dashes=22))
        d.add(DashedVMobject(Ellipse(width=1.1, height=2 * R, color="#FFD166", stroke_width=2), num_dashes=28))
        d.add(Line(ORIGIN, R * RIGHT, color="#FF8A50", stroke_width=4))
        d.add(Dot(ORIGIN, radius=0.05, color="#FFE082"), Dot(R * RIGHT, radius=0.05, color="#FFE082"))
        d.add(MathTex(r"R", font_size=28, color="#FF8A50").move_to(R * 0.5 * RIGHT + UP * 0.22))
        return self.panel(d)

    def p_frust(self):
        d = VGroup()
        b = [(-1.25, -1.25, -0.9), (1.25, -1.25, -0.9), (1.25, 1.25, -0.9), (-1.25, 1.25, -0.9)]
        t = [(-0.65, -0.65, 0.85), (0.65, -0.65, 0.85), (0.65, 0.65, 0.85), (-0.65, 0.65, 0.85)]
        for k in range(4):
            d.add(Line(pr(b[k]), pr(b[(k + 1) % 4]), color="#4FC3F7", stroke_width=3.5))
            d.add(Line(pr(t[k]), pr(t[(k + 1) % 4]), color="#66D19E", stroke_width=3.5))
            d.add(Line(pr(b[k]), pr(t[k]), color=PAL[k % len(PAL)], stroke_width=4))
        d.add(DashedVMobject(Line(pr((0, 0, -0.9)), pr((0, 0, 0.85)), color="#FFD166", stroke_width=3), num_dashes=12))
        d.add(Dot(pr((0, 0, -0.9)), radius=0.045, color="#FFE082"), Dot(pr((0, 0, 0.85)), radius=0.045, color="#FFE082"))
        d.add(MathTex(r"S", font_size=28, color="#4FC3F7").move_to(pr((0, 0, -0.9)) + DOWN * 0.25))
        d.add(MathTex(r"S'", font_size=28, color="#66D19E").move_to(pr((0, 0, 0.85)) + UP * 0.25))
        d.add(MathTex(r"h", font_size=28, color="#FFD166").move_to(pr((0, 0, -0.02)) + RIGHT * 0.28))
        return self.panel(d)

    def p_sph_cap(self):
        d = VGroup()
        R = 1.35
        d.add(Circle(radius=R, color="#263238", stroke_width=2.5))
        d.add(DashedVMobject(Ellipse(width=2 * R, height=0.86, color="#37474F", stroke_width=2), num_dashes=24))
        r_c = float(np.sqrt(max(R**2 - 0.45**2, 0)))
        d.add(Ellipse(width=2 * r_c, height=0.86 * (r_c / R), color="#66D19E", stroke_width=3.5).move_to(UP * 0.45))
        theta_cut = float(np.arcsin(0.45 / R))
        arc_cap = Arc(radius=R, start_angle=theta_cut, angle=np.pi - 2 * theta_cut, color="#FF8A50", stroke_width=5)
        d.add(arc_cap)
        d.add(DashedVMobject(Line(UP * 0.45, UP * R, color="#FFD166", stroke_width=3), num_dashes=8))
        d.add(Dot(UP * 0.45, radius=0.045, color="#FFE082"), Dot(UP * R, radius=0.045, color="#FFE082"))
        d.add(MathTex(r"h", font_size=28, color="#FFD166").move_to(UP * 0.90 + RIGHT * 0.25))
        d.add(Line(ORIGIN, R * RIGHT, color="#4FC3F7", stroke_width=2.5))
        d.add(Dot(ORIGIN, radius=0.045, color="#FFE082"))
        d.add(MathTex(r"R", font_size=26, color="#4FC3F7").move_to(RIGHT * 0.7 + DOWN * 0.22))
        return self.panel(d)

    def p_sph_seg(self):
        d = VGroup()
        R = 1.35
        d.add(Circle(radius=R, color="#263238", stroke_width=2))
        d.add(DashedVMobject(Ellipse(width=2 * R, height=0.86, color="#37474F", stroke_width=2), num_dashes=24))
        r_c = float(np.sqrt(max(R**2 - 0.45**2, 0)))
        sec = Ellipse(width=2 * r_c, height=0.86 * (r_c / R), color="#00897B", fill_color="#00897B", fill_opacity=0.35, stroke_width=3).move_to(UP * 0.45)
        d.add(sec)
        theta_cut = float(np.arcsin(0.45 / R))
        arc_cap = Arc(radius=R, start_angle=theta_cut, angle=np.pi - 2 * theta_cut, color="#26A69A", stroke_width=4.5)
        d.add(arc_cap)
        d.add(DashedVMobject(Line(UP * 0.45, UP * R, color="#FFD166", stroke_width=3), num_dashes=8))
        d.add(Dot(UP * 0.45, radius=0.045, color="#FFE082"), Dot(UP * R, radius=0.045, color="#FFE082"))
        d.add(MathTex(r"h", font_size=28, color="#FFD166").move_to(UP * 0.90 + RIGHT * 0.25))
        d.add(Line(ORIGIN, UP * 0.45 + RIGHT * r_c, color="#FF8A50", stroke_width=2.5))
        d.add(MathTex(r"R", font_size=26, color="#FF8A50").move_to(UP * 0.22 + RIGHT * 0.7))
        d.add(Dot(ORIGIN, radius=0.045, color="#FFE082"))
        return self.panel(d)

    def p_line_plane(self):
        d = VGroup()
        quad = [(-2.2, -1.1, 0), (2.0, -1.1, 0), (2.5, 1.1, 0), (-1.7, 1.1, 0)]
        d.add(Polygon(*[pr(p) for p in quad], fill_color="#1F3A57", fill_opacity=0.45, stroke_color="#4A7DB5", stroke_width=2.5))
        O = np.array([-0.3, -0.1, 0.0])
        v_end = np.array([1.5, 0.4, 1.45])
        v_proj = np.array([1.5, 0.4, 0.0])
        n_end = O + np.array([0, 0, 1.4])
        d.add(arrow3(O, n_end, "#FFD166", sw=4.5))
        d.add(MathTex(r"\vec{n}", font_size=30, color="#FFD166").move_to(pr(n_end) + UP * 0.25 + RIGHT * 0.1))
        d.add(arrow3(O, v_end, "#FF5252", sw=5.5))
        d.add(MathTex(r"\vec{v}", font_size=30, color="#FF5252").move_to(pr(v_end) + UP * 0.25 + RIGHT * 0.2))
        d.add(DashedVMobject(Line(pr(O), pr(v_proj), color="#4FC3F7", stroke_width=3.5), num_dashes=12))
        d.add(DashedVMobject(Line(pr(v_end), pr(v_proj), color=GREY, stroke_width=2.5), num_dashes=10))
        d.add(arc3(O, v_proj - O, v_end - O, 0.65, "#66D19E", sw=3.5))
        d.add(MathTex(r"\theta", font_size=28, color="#66D19E").move_to(pr(O + unit3(v_proj - O + v_end - O) * 0.9) + UP * 0.1))
        d.add(Dot(pr(O), radius=0.05, color="#FFE082"), Dot(pr(v_proj), radius=0.045, color="#FFE082"))
        return self.panel(d)

    def p_pt_plane(self):
        d = VGroup()
        quad = [(-2.2, -1.1, 0), (2.0, -1.1, 0), (2.5, 1.1, 0), (-1.7, 1.1, 0)]
        d.add(Polygon(*[pr(p) for p in quad], fill_color="#1F3A57", fill_opacity=0.45, stroke_color="#4A7DB5", stroke_width=2.5))
        A = np.array([-1.0, 0.1, 0.0])
        H = np.array([0.7, 0.2, 0.0])
        P = np.array([0.7, 0.2, 1.45])
        d.add(Line(pr(P), pr(H), color="#FF5252", stroke_width=5))
        d.add(MathTex(r"d", font_size=32, color="#FF5252").move_to(pr((P + H) / 2) + RIGHT * 0.28))
        d.add(arrow3(A, P, "#4FC3F7", sw=4.5))
        d.add(MathTex(r"\overrightarrow{AP}", font_size=28, color="#4FC3F7").move_to(pr((A + P) / 2) + UP * 0.25 + LEFT * 0.15))
        d.add(DashedVMobject(Line(pr(A), pr(H), color=GREY, stroke_width=2.5), num_dashes=12))
        n_end = A + np.array([0, 0, 1.3])
        d.add(arrow3(A, n_end, "#FFD166", sw=4.5))
        d.add(MathTex(r"\vec{n}", font_size=30, color="#FFD166").move_to(pr(n_end) + UP * 0.25))
        d.add(Dot(pr(A), radius=0.05, color="#FFE082"), Dot(pr(P), radius=0.055, color="#FFE082"), Dot(pr(H), radius=0.045, color="#FFE082"))
        d.add(MathTex(r"A", font_size=26, color="#FFE082").move_to(pr(A) + DOWN * 0.25))
        d.add(MathTex(r"P", font_size=26, color="#FFE082").move_to(pr(P) + UP * 0.25))
        d.add(MathTex(r"H", font_size=26, color="#FFE082").move_to(pr(H) + DOWN * 0.25 + RIGHT * 0.1))
        return self.panel(d)

    def p_d_vol(self):
        d = VGroup()
        A = np.array([0.1, 0.1, 1.4])
        B = np.array([-1.4, -0.9, -0.4])
        C = np.array([1.5, -0.8, -0.4])
        D = np.array([0.2, 1.3, -0.4])
        d.add(Polygon(pr(B), pr(C), pr(D), fill_color="#00897B", fill_opacity=0.25, stroke_color="#26A69A", stroke_width=3))
        for p1, p2, col in [(A, B, "#4FC3F7"), (A, C, "#FFD166"), (A, D, "#BA68C8"), (B, C, "#26A69A"), (C, D, "#26A69A"), (D, B, "#26A69A")]:
            d.add(Line(pr(p1), pr(p2), color=col, stroke_width=3.5))
        G = (B + C + D) / 3
        d.add(DashedVMobject(Line(pr(A), pr(G), color="#FF5252", stroke_width=4.5), num_dashes=12))
        d.add(Dot(pr(A), radius=0.05, color="#FFE082"), Dot(pr(G), radius=0.045, color="#FFE082"))
        d.add(MathTex(r"h=\frac{3V}{S}", font_size=28, color="#FF5252").move_to(pr((A + G) / 2) + RIGHT * 0.8))
        d.add(MathTex(r"S", font_size=28, color="#26A69A").move_to(pr(G) + DOWN * 0.35))
        return self.panel(d)

    def p_proj_area(self):
        d = VGroup()
        t_orig = [np.array([-1.2, -0.5, 0.4]), np.array([1.3, -0.6, 0.6]), np.array([0.2, 1.0, 1.4])]
        t_proj = [np.array([-1.2, -0.5, -0.6]), np.array([1.3, -0.6, -0.6]), np.array([0.2, 1.0, -0.6])]
        d.add(Polygon(*[pr(p) for p in t_orig], fill_color="#FF8A50", fill_opacity=0.35, stroke_color="#FF8A50", stroke_width=3.5))
        d.add(Polygon(*[pr(p) for p in t_proj], fill_color="#4FC3F7", fill_opacity=0.25, stroke_color="#4FC3F7", stroke_width=3))
        for p1, p2 in zip(t_orig, t_proj):
            d.add(DashedVMobject(Line(pr(p1), pr(p2), color=GREY, stroke_width=2), num_dashes=10))
        d.add(MathTex(r"S", font_size=32, color="#FF8A50").move_to(pr(sum(t_orig) / 3)))
        d.add(MathTex(r"S'", font_size=32, color="#4FC3F7").move_to(pr(sum(t_proj) / 3)))
        return self.panel(d)

    def p_min_angle(self):
        d = VGroup()
        quad = [(-2.2, -1.1, 0), (2.0, -1.1, 0), (2.5, 1.1, 0), (-1.7, 1.1, 0)]
        d.add(Polygon(*[pr(p) for p in quad], fill_color="#1F3A57", fill_opacity=0.45, stroke_color="#4A7DB5", stroke_width=2.5))
        O = np.array([-0.6, -0.2, 0.0])
        l_end = O + np.array([1.8, 0.3, 1.2])
        l0_end = O + np.array([1.8, 0.3, 0.0])
        m_end = O + np.array([1.2, 1.4, 0.0])
        d.add(Line(pr(O), pr(l_end), color="#FF5252", stroke_width=4.5))
        d.add(DashedVMobject(Line(pr(O), pr(l0_end), color="#4FC3F7", stroke_width=3.5), num_dashes=12))
        d.add(Line(pr(O), pr(m_end), color="#66D19E", stroke_width=4))
        d.add(DashedVMobject(Line(pr(l_end), pr(l0_end), color=GREY, stroke_width=2), num_dashes=10))
        d.add(arc3(O, l0_end - O, l_end - O, 0.7, "#FFD166", sw=3))
        d.add(arc3(O, l0_end - O, m_end - O, 0.65, "#4FC3F7", sw=3))
        d.add(arc3(O, m_end - O, l_end - O, 0.9, "#F06292", sw=3))
        d.add(MathTex(r"\theta_1", font_size=26, color="#FFD166").move_to(pr(O + unit3(l0_end - O + l_end - O) * 0.95)))
        d.add(MathTex(r"\theta_2", font_size=26, color="#4FC3F7").move_to(pr(O + unit3(l0_end - O + m_end - O) * 0.9)))
        d.add(MathTex(r"\varphi", font_size=26, color="#F06292").move_to(pr(O + unit3(m_end - O + l_end - O) * 1.15)))
        d.add(Dot(pr(O), radius=0.05, color="#FFE082"))
        return self.panel(d)

    def p_dir_cos(self):
        d = VGroup()
        O = ORIGIN
        ax_x = np.array([2.0, 0, 0])
        ax_y = np.array([0, 1.8, 0])
        ax_z = np.array([0, 0, 1.8])
        d.add(arrow3(O, ax_x, "#56646F", sw=2.5))
        d.add(arrow3(O, ax_y, "#56646F", sw=2.5))
        d.add(arrow3(O, ax_z, "#56646F", sw=2.5))
        d.add(MathTex(r"x", font_size=26, color="#56646F").move_to(pr(ax_x) + RIGHT * 0.2))
        d.add(MathTex(r"y", font_size=26, color="#56646F").move_to(pr(ax_y) + UP * 0.2))
        d.add(MathTex(r"z", font_size=26, color="#56646F").move_to(pr(ax_z) + UP * 0.25))
        u = np.array([1.3, 1.1, 1.2])
        d.add(arrow3(O, u, "#FF8A50", sw=5))
        d.add(arc3(O, ax_x, u, 0.7, "#FFD166", sw=3))
        d.add(arc3(O, ax_y, u, 0.7, "#66D19E", sw=3))
        d.add(arc3(O, ax_z, u, 0.7, "#BA68C8", sw=3))
        d.add(MathTex(r"\alpha", font_size=28, color="#FFD166").move_to(pr(unit3(ax_x + u) * 0.95)))
        d.add(MathTex(r"\beta", font_size=28, color="#66D19E").move_to(pr(unit3(ax_y + u) * 0.95)))
        d.add(MathTex(r"\gamma", font_size=28, color="#BA68C8").move_to(pr(unit3(ax_z + u) * 0.95)))
        d.add(Dot(pr(O), radius=0.05, color="#FFE082"))
        return self.panel(d)

    def p_tetra_vol(self):
        d = VGroup()
        O = ORIGIN
        a = np.array([1.8, 0.2, 0.1])
        b = np.array([0.3, 1.7, 0.2])
        c = np.array([0.2, 0.3, 1.4])
        d.add(Polygon(pr(O), pr(a), pr(b), fill_color="#1E88E5", fill_opacity=0.25, stroke_width=0))
        d.add(arrow3(O, a, "#4FC3F7", sw=4.5))
        d.add(arrow3(O, b, "#66D19E", sw=4.5))
        d.add(arrow3(O, c, "#FF5252", sw=4.5))
        d.add(Line(pr(a), pr(b), color="#78909C", stroke_width=3))
        d.add(Line(pr(a), pr(c), color="#78909C", stroke_width=3))
        d.add(Line(pr(b), pr(c), color="#78909C", stroke_width=3))
        d.add(MathTex(r"\vec{a}", font_size=28, color="#4FC3F7").move_to(pr(a) + RIGHT * 0.25))
        d.add(MathTex(r"\vec{b}", font_size=28, color="#66D19E").move_to(pr(b) + UP * 0.25))
        d.add(MathTex(r"\vec{c}", font_size=28, color="#FF5252").move_to(pr(c) + UP * 0.25))
        d.add(Dot(pr(O), radius=0.05, color="#FFE082"))
        return self.panel(d)

    def p_skew_dist(self):
        d = VGroup()
        l1_start = np.array([-2.0, -0.4, 0.65])
        l1_end = np.array([2.0, -0.4, 0.65])
        l2_start = np.array([0.3, -1.5, -0.65])
        l2_end = np.array([0.3, 1.5, -0.65])
        d.add(Line(pr(l1_start), pr(l1_end), color="#4FC3F7", stroke_width=4))
        d.add(Line(pr(l2_start), pr(l2_end), color="#66D19E", stroke_width=4))
        P1 = np.array([0.3, -0.4, 0.65])
        P2 = np.array([0.3, -0.4, -0.65])
        d.add(Line(pr(P1), pr(P2), color="#FF5252", stroke_width=6))
        d.add(Dot(pr(P1), radius=0.055, color="#FFE082"), Dot(pr(P2), radius=0.055, color="#FFE082"))
        d.add(MathTex(r"d", font_size=32, color="#FF5252").move_to(pr((P1 + P2) / 2) + RIGHT * 0.3))
        d.add(arrow3(P1, P1 + np.array([1.0, 0, 0]), "#4FC3F7", sw=4))
        d.add(arrow3(P2, P2 + np.array([0, 0.9, 0]), "#66D19E", sw=4))
        d.add(MathTex(r"\vec{a}", font_size=26, color="#4FC3F7").move_to(pr(P1 + np.array([1.2, 0, 0])) + UP * 0.2))
        d.add(MathTex(r"\vec{b}", font_size=26, color="#66D19E").move_to(pr(P2 + np.array([0, 1.1, 0])) + RIGHT * 0.2))
        return self.panel(d)

    def p_box_model(self):
        d = VGroup()
        a, b, c = 2.2, 1.6, 1.5
        pts = [
            (0, 0, 0), (a, 0, 0), (a, b, 0), (0, b, 0),
            (0, 0, c), (a, 0, c), (a, b, c), (0, b, c)
        ]
        edges = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]
        d.add(wire(pts, edges, dots=False, sw=2.0, colors=["#37474F"]))
        d.add(Line(pr(pts[0]), pr(pts[1]), color="#FF5252", stroke_width=5))
        d.add(Line(pr(pts[0]), pr(pts[3]), color="#40C4FF", stroke_width=5))
        d.add(Line(pr(pts[0]), pr(pts[4]), color="#69F0AE", stroke_width=5))
        d.add(DashedVMobject(Line(pr(pts[0]), pr(pts[6]), color="#FFD166", stroke_width=4), num_dashes=16))
        mid_diag = pr(np.array([a / 2, b / 2, c / 2]))
        d.add(Dot(mid_diag, radius=0.06, color="#FFD166"))
        d.add(MathTex(r"2R", font_size=28, color="#FFD166").move_to(mid_diag + UP * 0.35))
        d.add(MathTex(r"a", font_size=26, color="#FF5252").move_to(pr(np.array([a / 2, 0, 0])) + DOWN * 0.22))
        d.add(MathTex(r"b", font_size=26, color="#40C4FF").move_to(pr(np.array([0, b / 2, 0])) + LEFT * 0.25))
        d.add(MathTex(r"c", font_size=26, color="#69F0AE").move_to(pr(np.array([0, 0, c / 2])) + RIGHT * 0.25))
        return self.panel(d)

    def p_prism_sph(self):
        d = VGroup()
        d.add(Circle(radius=1.45, color="#FF8A50", stroke_width=3))
        r_b = 1.1; h_p = 1.4
        b_pts = [np.array([r_b * np.cos(np.radians(a)), r_b * np.sin(np.radians(a)), -h_p / 2]) for a in (90, 210, 330)]
        t_pts = [np.array([r_b * np.cos(np.radians(a)), r_b * np.sin(np.radians(a)), h_p / 2]) for a in (90, 210, 330)]
        for k in range(3):
            d.add(Line(pr(b_pts[k]), pr(b_pts[(k + 1) % 3]), color="#4FC3F7", stroke_width=3))
            d.add(Line(pr(t_pts[k]), pr(t_pts[(k + 1) % 3]), color="#66D19E", stroke_width=3))
            d.add(Line(pr(b_pts[k]), pr(t_pts[k]), color=PAL[k % len(PAL)], stroke_width=4))
        d.add(Dot(pr(ORIGIN), radius=0.05, color="#FFE082"))
        O1 = np.array([0, 0, -h_p / 2])
        V0 = b_pts[0]
        d.add(DashedVMobject(Line(pr(ORIGIN), pr(O1), color="#FFD166", stroke_width=3), num_dashes=8))
        d.add(DashedVMobject(Line(pr(O1), pr(V0), color="#4FC3F7", stroke_width=3), num_dashes=8))
        d.add(Line(pr(ORIGIN), pr(V0), color="#FF5252", stroke_width=4))
        d.add(MathTex(r"R", font_size=26, color="#FF5252").move_to(pr(V0 * 0.5) + UP * 0.2))
        d.add(MathTex(r"r", font_size=24, color="#4FC3F7").move_to(pr((O1 + V0) / 2) + DOWN * 0.2))
        d.add(MathTex(r"\frac{h}{2}", font_size=24, color="#FFD166").move_to(pr(O1 * 0.5) + LEFT * 0.3))
        return self.panel(d)

    def p_in_sph(self):
        d = VGroup()
        d.add(wire(TETRA, TETRA_E, sw=3.5, colors=["#78909C"]))
        r_in = 0.45
        d.add(Circle(radius=r_in, color="#FFD166", stroke_width=3).move_to(pr(ORIGIN)))
        d.add(DashedVMobject(Ellipse(width=2 * r_in, height=0.3 * r_in, color="#FFD166", stroke_width=2).move_to(pr(ORIGIN)), num_dashes=16))
        d.add(Dot(pr(ORIGIN), radius=0.05, color="#FFD166"))
        r_end = pr(ORIGIN + np.array([0.35, -0.2, -0.2]))
        d.add(Line(pr(ORIGIN), r_end, color="#FF5252", stroke_width=3.5))
        d.add(MathTex(r"r", font_size=28, color="#FF5252").move_to((pr(ORIGIN) + r_end) / 2 + UP * 0.22))
        return self.panel(d)

    def p_tetra_hv(self):
        d = VGroup()
        T = [(0.95, 0.95, 0.95), (0.95, -0.95, -0.95), (-0.95, 0.95, -0.95), (-0.95, -0.95, 0.95)]
        A = np.array(T[0])
        B, C, D0 = [np.array(p) for p in T[1:]]
        G = (B + C + D0) / 3
        d.add(Polygon(pr(B), pr(C), pr(D0), fill_color="#1E88E5", fill_opacity=0.20, stroke_color="#4FC3F7", stroke_width=3))
        for p1, p2, col in [(A, B, "#FF5252"), (A, C, "#FFD166"), (A, D0, "#BA68C8"),
                            (B, C, "#4FC3F7"), (C, D0, "#4FC3F7"), (D0, B, "#4FC3F7")]:
            d.add(Line(pr(p1), pr(p2), color=col, stroke_width=3.5))
        d.add(DashedVMobject(Line(pr(A), pr(G), color="#66D19E", stroke_width=5), num_dashes=14))
        d.add(Dot(pr(A), radius=0.055, color="#FFE082"), Dot(pr(G), radius=0.05, color="#FFE082"))
        d.add(MathTex(r"h", font_size=32, color="#66D19E").move_to(pr((A + G) / 2) + RIGHT * 0.35))
        d.add(MathTex(r"a", font_size=28, color="#FF5252").move_to(pr((A + B) / 2) + LEFT * 0.3))
        return self.panel(d)

    def p_dih_all(self):
        d = VGroup()
        A = unit3([1.0, 0.25, -0.40]) * 2.5
        B = unit3([-0.95, 0.30, -0.32]) * 2.5
        C = unit3([0.12, -0.18, 0.92]) * 2.5
        d.add(Polygon(pr(ORIGIN), pr(A), pr(C), fill_color="#1E88E5", fill_opacity=0.22, stroke_color="#4FC3F7", stroke_width=3))
        d.add(Polygon(pr(ORIGIN), pr(B), pr(C), fill_color="#00897B", fill_opacity=0.22, stroke_color="#66D19E", stroke_width=3))
        d.add(Line(pr(ORIGIN), pr(C), color="#FFD166", stroke_width=6))
        d.add(Line(pr(ORIGIN), pr(A), color="#4FC3F7", stroke_width=4))
        d.add(Line(pr(ORIGIN), pr(B), color="#66D19E", stroke_width=4))
        c_mid = C * 0.45
        d.add(arc3(c_mid, A, B, 0.7, "#FF5252", sw=4))
        d.add(MathTex(r"C", font_size=32, color="#FF5252").move_to(pr(c_mid + unit3(A + B) * 0.95)))
        d.add(Dot(pr(ORIGIN), radius=0.06, color="#FFE082"))
        return self.panel(d)

    def p_sin_tri(self):
        d = VGroup()
        A = unit3([1.0, 0.25, -0.40]) * 2.5
        B = unit3([-0.95, 0.30, -0.32]) * 2.5
        C = unit3([0.12, -0.18, 0.92]) * 2.5
        for p, col in [(A, "#FF5252"), (B, "#40C4FF"), (C, "#69F0AE")]:
            d.add(Line(pr(ORIGIN), pr(p), color=col, stroke_width=5))
        d.add(arc3(ORIGIN, B, C, 0.85, "#F06292", sw=3))
        d.add(arc3(ORIGIN, C, A, 0.85, "#BA68C8", sw=3))
        d.add(arc3(ORIGIN, A, B, 0.85, "#FFD166", sw=3))
        d.add(MathTex(r"\alpha", font_size=28, color="#F06292").move_to(pr(unit3(B + C) * 1.15)))
        d.add(MathTex(r"\beta", font_size=28, color="#BA68C8").move_to(pr(unit3(C + A) * 1.15)))
        d.add(MathTex(r"\gamma", font_size=28, color="#FFD166").move_to(pr(unit3(A + B) * 1.15)))
        d.add(Dot(pr(ORIGIN), radius=0.06, color="#FFE082"))
        return self.panel(d)

    def p_med(self):
        d = VGroup()
        T = [(0.1, 0.1, 1.45), (-1.4, -0.9, -0.45), (1.5, -0.8, -0.45), (0.2, 1.3, -0.45)]
        A, B, C, D0 = [np.array(p) for p in T]
        M = (B + C + D0) / 3
        d.add(Polygon(pr(B), pr(C), pr(D0), fill_color="#37474F", fill_opacity=0.25, stroke_color="#78909C", stroke_width=2.5))
        for p1, p2, col in [(A, B, "#4FC3F7"), (A, C, "#FFD166"), (A, D0, "#BA68C8"), (B, C, "#78909C"), (C, D0, "#78909C"), (D0, B, "#78909C")]:
            d.add(Line(pr(p1), pr(p2), color=col, stroke_width=3))
        d.add(Line(pr(A), pr(M), color="#FF5252", stroke_width=5.5))
        d.add(DashedVMobject(Line(pr(B), pr((C + D0) / 2), color=GREY, stroke_width=2), num_dashes=10))
        d.add(Dot(pr(A), radius=0.055, color="#FFE082"), Dot(pr(M), radius=0.05, color="#FF5252"))
        d.add(MathTex(r"m_A", font_size=32, color="#FF5252").move_to(pr((A + M) / 2) + RIGHT * 0.35))
        d.add(MathTex(r"M", font_size=26, color="#FFE082").move_to(pr(M) + DOWN * 0.25))
        return self.panel(d)

    def p_gram_det(self):
        d = VGroup()
        O = ORIGIN
        a1 = np.array([1.8, 0.2, 0.1])
        a2 = np.array([0.3, 1.7, 0.2])
        a3 = np.array([0.2, 0.3, 1.4])
        d.add(Polygon(pr(O), pr(a1), pr(a2), fill_color="#1E88E5", fill_opacity=0.22, stroke_width=0))
        d.add(arrow3(O, a1, "#FF5252", sw=5))
        d.add(arrow3(O, a2, "#40C4FF", sw=5))
        d.add(arrow3(O, a3, "#69F0AE", sw=5))
        d.add(Line(pr(a1), pr(a2), color="#78909C", stroke_width=3))
        d.add(Line(pr(a2), pr(a3), color="#78909C", stroke_width=3))
        d.add(Line(pr(a3), pr(a1), color="#78909C", stroke_width=3))
        d.add(MathTex(r"\vec{a}_1", font_size=28, color="#FF5252").move_to(pr(a1) + RIGHT * 0.3))
        d.add(MathTex(r"\vec{a}_2", font_size=28, color="#40C4FF").move_to(pr(a2) + UP * 0.28))
        d.add(MathTex(r"\vec{a}_3", font_size=28, color="#69F0AE").move_to(pr(a3) + UP * 0.28))
        d.add(Dot(pr(O), radius=0.055, color="#FFE082"))
        return self.panel(d)

    # ---------- 主流程 ----------
    def construct(self):
        self.add_wallpaper()
        op_t = Text("立体几何邪修之路", font=KAI, weight=BOLD, font_size=88)
        op_t.set_color_by_gradient("#FFD166", "#F59E62")
        op_s = Text("36 神式 · 炼气到登神", font=KAI, weight=BOLD, font_size=38, color="#4DB6AC")
        op_t.move_to(UP * 1.0)
        op_s.move_to(DOWN * 0.55)
        self.play(FadeIn(op_t, shift=DOWN * 0.3), FadeIn(op_s, shift=DOWN * 0.3), run_time=T_RUN)
        self.wait(0.40)
        self.cur_t, self.cur_f, self.cur_s, self.cur_plot = op_t, None, op_s, None

        for i in range(len(CARDS)):
            self.go_card(i)

        outs = [m for m in (self.cur_t, self.cur_f, self.cur_s, self.cur_plot) if m is not None]
        self.play(*[FadeOut(m) for m in outs], run_time=T_RUN)
        end = Text("邪修登神 · 功德圆满", font=KAI, weight=BOLD, font_size=72)
        end.set_color_by_gradient("#FFD166", "#F59E62")
        self.play(FadeIn(end, shift=UP * 0.25), run_time=0.35)
        self.wait(0.55)
        self.play(FadeOut(end), run_time=0.40)
