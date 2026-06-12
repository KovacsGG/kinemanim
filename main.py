from manim import *

config.verbosity = "WARNING"
config.background_color= WHITE

VMobject.set_default(stroke_color=BLACK)
VMobject.set_default(stroke_width=1)
Dot.set_default(color=BLACK)
SingleStringMathTex.set_default(font_size=30)


class Arm(VMobject):
    def __init__(self, length: float, angle: float, end: VMobject, **kwargs):
        super().__init__(**kwargs)
        self.ground = DashedLine(ORIGIN, RIGHT)
        self.joint = VGroup(
            Circle(0.2).set_fill(GREY, 1),
            Dot(),
        )

        self.end = end.copy().shift(RIGHT * length).rotate(angle * DEGREES, about_point=self.joint.get_center())
        self.stick = (Rectangle(BLACK, length, .2)
            .set_fill(GREY, 1)
            .shift(UP * length / 2)
            .rotate((angle - 90) * DEGREES, about_point=self.joint.get_center())
         )

        self.l = MathTex(r"\l_1")
        self.arc = Angle.from_three_points(RIGHT, ORIGIN, self.end.get_center(), radius=.5)
        
        self.add(self.ground, self.arc, self.stick, self.joint, self.end)

    def get_arc_label_pos(self):
        t = Angle(self.ground, Line(self.joint.get_center(), self.end.get_center()), radius=0.8)
        return t.point_from_proportion(0.5)
        


class ArmAnim(Scene):
    def construct(self):
        theta1 = ValueTracker(170)
        theta2 = ValueTracker(-80)
        arm2 = Arm(2, theta2.get_value(), Dot())
        arm1 = Arm(2, theta1.get_value(), arm2)
        
        arm1.add_updater(
            lambda x: x.become(Arm(2, theta1.get_value(), arm2.update()))
        )
        arm2.add_updater(
            lambda x: x.become(Arm(2, theta2.get_value(), Dot()))
        )

        l1 = MathTex(r"\l_1")
        l1.add_updater(lambda x: x.next_to(arm1.stick.point_from_proportion(0.25), LEFT), call_updater=True)
        l2 = MathTex(r"\l_2")
        l2.add_updater(lambda x: x.next_to(arm1.end.stick.point_from_proportion(0.25), LEFT), call_updater=True)
        t1 = MathTex(r"\Theta_1")
        t1.add_updater(lambda x: x.move_to(arm1.get_arc_label_pos()), call_updater=True)
        t2 = MathTex(r"\Theta_2")
        t2.add_updater(lambda x: x.move_to(arm1.end.get_arc_label_pos()), call_updater=True)
        X_x = Variable(0, "x", num_decimal_places=2)
        X_x.value.set_color(BLACK)
        X_x.add_updater(lambda x: x.tracker.set_value(arm1.end.end.get_x()), call_updater=True)
        X_y = Variable(0, "y", num_decimal_places=2, color=BLACK)
        X_y.value.set_color(BLACK)
        X_y.add_updater(lambda x: x.tracker.set_value(arm1.end.end.get_y()), call_updater=True)
        p = VGroup(
            X_x,
            X_y,
        ).arrange(DOWN)
        p.add_updater(
            lambda x: x.next_to(arm1.end.end, RIGHT),
            call_updater=True
        )

        self.add(arm1, l1, l2, t1, t2, p, X_x, X_y)
        self.play(
            theta2.animate.set_value(30),
            theta1.animate.set_value(-50),
            run_time=4,
            rate_func=linear
        )
        #self.play(arm2.anim_angle(-60))
        

import cv2
from scipy import interpolate

img = cv2.imread("theta1.png")[:, :, 0] == 0
xs = []
ys = []
for col in range(img.shape[1]):
    x = col / img.shape[1]
    idx = np.argwhere(img[:, col])
    y = idx.sum() / idx.size
    y = y / img.shape[0]
    y = 1 - y
    xs.append(x)
    ys.append(y)
xs = np.array(xs)
ys = np.array(ys)

f = interpolate.interp1d(xs, ys, kind="linear")