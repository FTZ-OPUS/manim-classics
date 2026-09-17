"""
甜甜圈体积推导 —— Manim CE 0.21 复刻
竖屏 1080x1920 (9:16), 30fps, 约24秒
帕普斯定理: V = 2πR · πr² = 2π²Rr²
"""
from manim import *
import numpy as np

# ============ 竖屏配置 ============
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.frame_rate = 30

# ============ 配色 ============
BG = BLACK
GREEN_FILL = "#66BB6A"
GREEN_STROKE = "#C8E6C9"
GREEN_DARK = "#2E7D32"
GOLD = "#FFD54F"
GREY = "#AAAAAA"
WHITE_T = WHITE

# ============ 几何参数 ============
R_BIG = 2.0       # 旋转半径（圆心到z轴）
R_SMALL = 0.72    # 圆盘半径 / 环面小管半径
SCENE_UP = 1.5    # 3D场景整体上移量

# ============ 辅助函数 ============
def torus_pt(u, v):
    """环面参数方程: u绕z轴, v绕管心"""
    return np.array([
        (R_BIG + R_SMALL * np.cos(v)) * np.cos(u),
        (R_BIG + R_SMALL * np.cos(v)) * np.sin(u),
        R_SMALL * np.sin(v) + SCENE_UP
    ])

def shift3d(mob):
    """把3D对象整体上移"""
    mob.shift([0, 0, SCENE_UP])
    return mob

def make_torus_wires(u_max=2*PI, n_lat=10, n_lon=8, color=GREEN_STROKE, lw=0.8, op=0.7):
    """环面线框（经纬线）"""
    g = VGroup()
    for i in range(n_lat):
        v = i * 2 * PI / n_lat
        n_pts = max(6, int(u_max * 8))
        pts = [torus_pt(u, v) for u in np.linspace(0, u_max, n_pts)]
        g.add(VMobject().set_points_as_corners(pts).make_smooth())
    for i in range(n_lon + 1):
        u = i * u_max / n_lon if n_lon > 0 else 0
        pts = [torus_pt(u, v) for v in np.linspace(0, 2*PI, 30)]
        g.add(VMobject().set_points_as_corners(pts).make_smooth())
    g.set_stroke(color, width=lw, opacity=op)
    return g

def make_torus_surface(u_max=2*PI, opacity=0.35):
    """环面半透明填充"""
    s = Surface(
        lambda u, v: torus_pt(u, v),
        u_range=[0, u_max],
        v_range=[0, 2*PI],
        resolution=(max(12, int(u_max*5)), 14),
        fill_color=GREEN_FILL,
        fill_opacity=opacity,
        stroke_width=0,
    )
    return s

def make_full_torus():
    """完整环面 = 填充 + 线框"""
    return VGroup(make_torus_surface(2*PI, 0.38),
                  make_torus_wires(2*PI, 10, 8))

def make_disk_at(theta, fill_op=0.55):
    """在角度theta处的圆盘（x-z平面，圆心距z轴R_BIG）"""
    disk = Circle(radius=R_SMALL, fill_color=GREEN_FILL, fill_opacity=fill_op,
                  stroke_color=WHITE, stroke_width=1.5)
    disk.rotate(PI/2, RIGHT)
    disk.rotate(theta, OUT)
    disk.move_to([R_BIG*np.cos(theta), R_BIG*np.sin(theta), SCENE_UP])
    dot = Dot(radius=0.04, color=WHITE)
    dot.move_to([R_BIG*np.cos(theta), R_BIG*np.sin(theta), SCENE_UP])
    return VGroup(disk, dot)

def make_centroid_arc(theta, color=WHITE, lw=2.0, op=0.85):
    """圆心走过的轨迹弧（半径R_BIG，在z=SCENE_UP平面）"""
    if theta < 0.02:
        return VMobject()
    n_pts = max(6, int(theta * 10))
    pts = [[R_BIG*np.cos(u), R_BIG*np.sin(u), SCENE_UP] for u in np.linspace(0, theta, n_pts)]
    arc = VMobject().set_points_as_corners(pts).make_smooth()
    arc.set_stroke(color, width=lw, opacity=op)
    return arc

def make_dashed_centroid_circle():
    """完整的圆心轨迹虚线圆"""
    pts = [[R_BIG*np.cos(u), R_BIG*np.sin(u), SCENE_UP] for u in np.linspace(0, 2*PI, 60)]
    c = VMobject().set_points_as_corners(pts).make_smooth()
    c.set_stroke(WHITE, width=1.5, opacity=0.55)
    c = DashedVMobject(c, num_dashes=40)
    return c


class TorusVolume(ThreeDScene):
    def construct(self):
        self.camera.background_color = BG
        self.set_camera_orientation(phi=66*DEGREES, theta=-42*DEGREES, distance=13.5)

        self.fixed_mobs = VGroup()
        self.cur_formula = None

        self.stage_cover()
        self.stage_question()
        self.stage_disk_rotation()
        self.stage_point_sweep()
        self.stage_rotate_to_torus()
        self.stage_centroid()
        self.stage_final()
        self.stage_outro()

    # ---------- 工具 ----------
    def fix(self, mob, y):
        mob.move_to([0, y, 0])
        self.add_fixed_in_frame_mobjects(mob)
        self.fixed_mobs.add(mob)
        return mob

    def clear_fixed(self):
        for m in self.fixed_mobs:
            self.remove_fixed_in_frame_mobjects(m)
        self.fixed_mobs = VGroup()

    def swap_title(self, new_text, font_size=38):
        """替换顶部标题文字（淡入淡出）"""
        old = None
        for m in self.fixed_mobs:
            if isinstance(m, Text):
                old = m
                break
        new = Text(new_text, font_size=font_size, color=WHITE_T)
        new.move_to([0, 5.8, 0])
        self.add_fixed_in_frame_mobjects(new)
        self.fixed_mobs.add(new)
        new.set_opacity(0)
        if old:
            self.play(old.animate.set_opacity(0), new.animate.set_opacity(1), run_time=0.45)
            self.remove_fixed_in_frame_mobjects(old)
            self.fixed_mobs -= old
        else:
            self.play(new.animate.set_opacity(1), run_time=0.4)
        return new

    def swap_formula(self, new_tex, font_size=52, color=WHITE_T):
        """替换底部公式（淡入淡出，避免残留）"""
        old = self.cur_formula
        new = MathTex(new_tex, font_size=font_size, color=color)
        new.move_to([0, -5.2, 0])
        self.add_fixed_in_frame_mobjects(new)
        self.fixed_mobs.add(new)
        new.set_opacity(0)
        if old:
            self.play(old.animate.set_opacity(0), new.animate.set_opacity(1), run_time=0.55)
            self.remove_fixed_in_frame_mobjects(old)
            self.fixed_mobs -= old
        else:
            self.play(new.animate.set_opacity(1), run_time=0.4)
        self.cur_formula = new
        return new

    # ========== 1. 封面 ==========
    def stage_cover(self):
        cover = ImageMobject("/Users/fengtianzhu/Doubao/chats/2026-09-16/new-chat/cover.png")
        cover.height = 16
        cover.move_to(ORIGIN)
        self.add_fixed_in_frame_mobjects(cover)
        self.wait(0.5)
        self.play(FadeOut(cover), run_time=0.35)
        self.remove_fixed_in_frame_mobjects(cover)

    # ========== 2. 问题引入 ==========
    def stage_question(self):
        title = Text("甜甜圈的体积是多少？", font_size=40, color=WHITE_T)
        self.fix(title, 5.8)

        vq = MathTex("V = ?", font_size=60, color=WHITE_T)
        self.fix(vq, -5.2)
        self.cur_formula = vq

        torus = make_full_torus()
        self.add(torus)

        self.begin_ambient_camera_rotation(rate=0.18)
        self.wait(0.8)

        # 右侧截面圆
        cross_section = make_disk_at(0, fill_op=0.6)
        self.play(FadeIn(cross_section, shift=RIGHT*0.3), run_time=0.5)
        self.wait(0.3)

        self.stop_ambient_camera_rotation()
        self.play(FadeOut(torus), FadeOut(cross_section), run_time=0.45)
        # 保留标题和公式，进入下一段
        self._torus_question = None

    # ========== 3. 圆盘绕z轴旋转 + R,r + A=πr² ==========
    def stage_disk_rotation(self):
        # 标题从"甜甜圈的体积是多少？"换成"一个圆盘绕 z 轴旋转。"
        self.swap_title("一个圆盘绕 z 轴旋转。")

        # 3D坐标系
        axes = self.make_axes()
        self.add(axes)

        disk = make_disk_at(0, fill_op=0.55)
        self.add(disk)

        self.begin_ambient_camera_rotation(rate=0.12)
        self.wait(0.4)

        # R 标注
        R_line = Line3D([0,0,SCENE_UP], [R_BIG,0,SCENE_UP], color=WHITE, thickness=0.015)
        R_label = MathTex("R", font_size=36, color=WHITE)
        R_label.move_to([R_BIG*0.5, 0.3, SCENE_UP+0.3])
        self.play(Create(R_line), FadeIn(R_label), run_time=0.4)

        # r 标注
        r_line = Line3D([R_BIG,0,SCENE_UP], [R_BIG,0,SCENE_UP+R_SMALL], color=WHITE, thickness=0.012)
        r_label = MathTex("r", font_size=36, color=WHITE)
        r_label.move_to([R_BIG+0.35, 0, SCENE_UP+R_SMALL*0.5])
        self.play(Create(r_line), FadeIn(r_label), run_time=0.4)
        self.wait(0.2)

        # 公式 V=? → A=πr²
        self.swap_formula("A = \\pi r^2", font_size=56)
        self.wait(0.3)
        self.stop_ambient_camera_rotation()

        self._disk = disk
        self._axes = axes
        self._R_line = R_line
        self._R_label = R_label
        self._r_line = r_line
        self._r_label = r_label

    # ========== 4. x处的点扫过圆 + V=∫2πx dA ==========
    def stage_point_sweep(self):
        self.swap_title("位于 x 处的点扫过一个圆。")

        # 圆盘上偏上的点
        point_pos = [R_BIG, 0, SCENE_UP + R_SMALL * 0.55]
        pt = Dot3D(point_pos, color=WHITE, radius=0.06)
        self.add(pt)

        # x标注线
        x_line = Line3D([0, 0, point_pos[2]], point_pos, color=WHITE, thickness=0.015)
        x_label = MathTex("x", font_size=36, color=WHITE)
        x_label.move_to([R_BIG*0.4, 0.3, point_pos[2]+0.2])
        self.play(FadeIn(pt), Create(x_line), FadeIn(x_label), run_time=0.45)
        self.wait(0.2)

        # 点扫过的圆轨迹（虚线）
        sweep_pts = [[R_BIG*np.cos(u), R_BIG*np.sin(u), point_pos[2]] for u in np.linspace(0, 2*PI, 60)]
        sweep_circle = VMobject().set_points_as_corners(sweep_pts).make_smooth()
        sweep_circle.set_stroke(WHITE, width=1.5, opacity=0.5)
        sweep_circle = DashedVMobject(sweep_circle, num_dashes=36)
        self.play(Create(sweep_circle), run_time=0.6)
        self.wait(0.2)

        # 公式 A=πr² → V=∫2πx dA
        self.swap_formula("V = \\int 2\\pi x \\, dA", font_size=52)
        self.wait(0.3)

        # 清理标注，保留圆盘和公式
        self.play(FadeOut(self._R_line), FadeOut(self._R_label),
                  FadeOut(self._r_line), FadeOut(self._r_label),
                  FadeOut(x_line), FadeOut(x_label), FadeOut(pt),
                  FadeOut(sweep_circle), FadeOut(self._axes),
                  run_time=0.35)

    # ========== 5. 圆盘旋转生成环面 ==========
    def stage_rotate_to_torus(self):
        theta = ValueTracker(0)

        disk_moving = always_redraw(lambda: make_disk_at(theta.get_value(), 0.55))

        def partial_torus():
            t = theta.get_value()
            if t < 0.03:
                return VGroup()
            surf = make_torus_surface(t, 0.32)
            wires = make_torus_wires(t, n_lat=8, n_lon=max(2, int(t/(PI/3))), lw=0.6, op=0.55)
            return VGroup(surf, wires)
        torus_growing = always_redraw(partial_torus)
        centroid_arc = always_redraw(lambda: make_centroid_arc(theta.get_value()))

        self.remove(self._disk)
        self.add(torus_growing, centroid_arc, disk_moving)

        self.begin_ambient_camera_rotation(rate=0.10)
        self.play(theta.animate.set_value(2*PI), run_time=3.5, rate_func=linear)
        self.stop_ambient_camera_rotation()

        # 替换为完整环面
        full_torus = make_full_torus()
        self.remove(torus_growing, centroid_arc, disk_moving)
        self.add(full_torus)
        self._torus = full_torus

        centroid_full = make_centroid_arc(2*PI, WHITE, 2.0, 0.8)
        self.add(centroid_full)
        self._centroid_path = centroid_full

        self.wait(0.3)

    # ========== 6. x的平均值在圆心 + x̄=(1/A)∫x dA=R ==========
    def stage_centroid(self):
        self.swap_title("x 的平均值位于圆心。")

        centroid_dashed = make_dashed_centroid_circle()
        self.play(Create(centroid_dashed), run_time=0.6)
        self._centroid_dashed = centroid_dashed

        self.begin_ambient_camera_rotation(rate=0.12)
        self.wait(0.5)

        self.swap_formula(r"\bar{x} = \frac{1}{A} \int x \, dA = R", font_size=46)
        self.wait(0.6)
        self.stop_ambient_camera_rotation()

    # ========== 7. 最终公式 ==========
    def stage_final(self):
        self.swap_title("面积乘以移动距离。")

        self.swap_formula(r"V = 2\pi R \cdot \pi r^2 = 2\pi^2 R r^2",
                          font_size=44, color=GOLD)

        # 截面圆沿轨迹移动
        self.begin_ambient_camera_rotation(rate=0.10)
        move_theta = ValueTracker(0)
        moving_disk = always_redraw(lambda: make_disk_at(move_theta.get_value(), 0.4))
        self.add(moving_disk)
        self.play(move_theta.animate.set_value(2*PI), run_time=2.2, rate_func=linear)
        self.remove(moving_disk)
        self.wait(0.3)

        # 底部灰色注脚
        footnote = Text("只有质心才重要。", font_size=30, color=GREY)
        self.fix(footnote, -6.5)
        self.wait(0.9)
        self.stop_ambient_camera_rotation()

    # ========== 8. 收尾 ==========
    def stage_outro(self):
        fade_anims = [FadeOut(m) for m in self.fixed_mobs]
        self.play(*fade_anims, run_time=0.7)
        self.clear_fixed()

        if hasattr(self, '_centroid_path'):
            self.play(FadeOut(self._centroid_path), run_time=0.4)
        if hasattr(self, '_centroid_dashed'):
            self.play(FadeOut(self._centroid_dashed), run_time=0.4)

        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(1.8)
        self.stop_ambient_camera_rotation()

        self.play(FadeOut(self._torus), run_time=0.6)
        self.wait(0.2)

    # ========== 3D坐标系 ==========
    def make_axes(self):
        g = VGroup()
        # z轴虚线
        z_axis = VMobject().set_points_as_corners([[0,0,SCENE_UP-3.2], [0,0,SCENE_UP+3.2]])
        z_axis.set_stroke(WHITE, width=2, opacity=0.7)
        z_axis = DashedVMobject(z_axis, num_dashes=20)
        g.add(z_axis)
        # x轴
        x_axis = Line3D([0,0,SCENE_UP], [2.8,0,SCENE_UP], color=WHITE, thickness=0.015)
        x_axis.set_opacity(0.8)
        g.add(x_axis)
        # y轴
        y_axis = Line3D([0,0,SCENE_UP], [0,2.0,SCENE_UP], color=WHITE, thickness=0.015)
        y_axis.set_opacity(0.8)
        g.add(y_axis)
        # 标注
        x_lb = MathTex("x", font_size=30, color=WHITE).move_to([3.0, 0, SCENE_UP+0.15])
        y_lb = MathTex("y", font_size=30, color=WHITE).move_to([0, 2.2, SCENE_UP+0.15])
        z_lb = MathTex("z", font_size=30, color=WHITE).move_to([0.15, 0, SCENE_UP+3.4])
        g.add(x_lb, y_lb, z_lb)
        return g
