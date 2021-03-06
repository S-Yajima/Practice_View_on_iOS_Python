import ui
import threading
import math

# 円を描画するView
# 進行方向の角度と速度、色を保持する
# 円の描画はdraw()メソッド内で.ui.Pathクラスにて行う
class MyView(ui.View):
    draw_color = 'yellow'
    angle = 0
    speed = 1
    movement_x = 1.0
    movement_y = 0.0

    # 移動速度と角度,色を設定する
    def set_speed_angle_color(self, speed, angle, draw_color):
        self.speed = speed
        self.angle = angle
        self.draw_color = draw_color
        self.calc_movement()

    def upper_right(self):
        return (self.x + self.width)

    def lower_left(self):
        return (self.y + self.height)

    # 角度と速度から、x軸y軸に動く長さを計算する
    # x軸= cos 角度
    # y軸= sin 角度
    def calc_movement(self):
        if self.angle == 0:
            self.movement_x = 1.0
            self.movement_y = 0.0
        elif self.angle == 90:
            self.movement_x = 0.0
            self.movement_y = 1.0
        elif self.angle == 180:
            self.movement_x = -1.0
            self.movement_y = 0.0
        elif self.angle == 270:
            self.movement_x = 0.0
            self.movement_y = -1.0
        else:
            self.movement_x = math.cos(math.radians(self.angle))
            self.movement_y = math.sin(math.radians(self.angle))

    # 接触した壁の角度から、反射角度を計算して設定する
    def angle_with_wallangle(self, wallangle):
        new_angle = (self.angle + ((wallangle - self.angle) * 2)) % 360
        # print(new_angle)
        return new_angle

    # 中心同士の角度を計算して返す
    def center_angle(self, diff_x, diff_y):
        # 中心同士のx軸とy軸の位置の差分からatan()で角度を算出する
        center_angle = 90
        if diff_x != 0:  # ゼロ割り算を防ぐ
            center_angle = int(math.degrees(math.atan(diff_y / diff_x)))

        # 接触した円の位置関係から360°角度に変更する
        if diff_x < 0 and diff_y > 0:
            center_angle = (90 - abs(center_angle)) + 90
        elif diff_x < 0 and diff_y < 0:
            center_angle = abs(center_angle) + 180
        elif diff_x > 0 and diff_y < 0:
            center_angle = 360 + center_angle

        return center_angle

    # 円同士の接触と反射を処理する
    def reflect_subview(self):
        for subview in self.superview.subviews:
            if id(self) != id(subview):
                # 中心同士の距離を算出する
                diff_x = subview.center.x - self.center.x
                diff_y = subview.center.y - self.center.y
                diff_center = math.sqrt(abs(diff_x) ** 2 + abs(diff_y) ** 2)
                # 接触している場合
                if (self.width + subview.width) / 2 >= diff_center:
                    # 中心同士を結んだ線の角度
                    theta_center = self.center_angle(diff_x, diff_y)
                    diff_wall_angle = 90

                    # 進行方向の後方から接触されたかを判別
                    if abs(180 - abs(((self.angle + 180) % 360) - theta_center)) > 90:
                        self.angle = (self.angle + (((theta_center + 180) % 360) - self.angle) / 2) % 360
                    # 進行方向の前方から接触した場合
                    else:
                        self.angle = self.angle_with_wallangle((theta_center + 90) % 360)
                    self.calc_movement()

    # メインビューの端に到達した際の角度の変更
    def reflect_main(self):
        # メインビューの左右の壁に接触した場合は
        # 90°の壁に接触した前提で反射角度を計算し設定する
        if self.x <= 0 or self.upper_right() >= self.superview.width:
            self.angle = self.angle_with_wallangle(90)

        # メインビューの上下の壁に接触した場合は
        # 0°の壁に接触した前提で反射角度を計算し設定する
        if self.y <= 0 or self.lower_left() >= self.superview.height:
            self.angle = self.angle_with_wallangle(0)

        self.calc_movement()

    # 描画
    def draw(self):
        path = ui.Path.oval(0, 0, self.width, self.height)
        ui.set_color(self.draw_color)
        path.fill()

    # 移動
    def move(self):
        self.x = self.x + (self.movement_x * self.speed)
        self.y = self.y + (self.movement_y * self.speed)


# Timer イベントで呼び出される
def schedule(main_view):
    for sub_view in main_view.subviews:
        sub_view.reflect_subview()
        sub_view.reflect_main()

    for sub_view in main_view.subviews:
        sub_view.move()

    main_view.set_needs_display()

    if main_view.on_screen == True:
        t = threading.Timer(0.01, schedule, args=[main_view])
        t.start()


if __name__ == '__main__':
    # メイン画面の作成
    main_view = ui.View(frame=(0, 0, 375, 667))
    main_view.name = '進む角度を設定した8つの円を互いに反射'
    main_view.background_color = 'lightblue'

    sub_view_1 = MyView(frame=(10, 90, 70, 70))
    sub_view_1.set_speed_angle_color(3, 20, 'green')
    main_view.add_subview(sub_view_1)

    sub_view_2 = MyView(frame=(100, 100, 70, 70))
    sub_view_2.set_speed_angle_color(3, 20, 'yellow')
    main_view.add_subview(sub_view_2)

    sub_view_3 = MyView(frame=(200, 110, 70, 70))
    sub_view_3.set_speed_angle_color(3, 20, 'blue')
    main_view.add_subview(sub_view_3)

    sub_view_4 = MyView(frame=(300, 120, 70, 70))
    sub_view_4.set_speed_angle_color(3, 20, 'red')
    main_view.add_subview(sub_view_4)

    sub_view_5 = MyView(frame=(300, 500, 70, 70))
    sub_view_5.set_speed_angle_color(3, 250, 'green')
    main_view.add_subview(sub_view_5)

    sub_view_6 = MyView(frame=(290, 400, 70, 70))
    sub_view_6.set_speed_angle_color(3, 250, 'yellow')
    main_view.add_subview(sub_view_6)

    sub_view_7 = MyView(frame=(280, 300, 70, 70))
    sub_view_7.set_speed_angle_color(3, 250, 'blue')
    main_view.add_subview(sub_view_7)

    sub_view_8 = MyView(frame=(270, 200, 70, 70))
    sub_view_8.set_speed_angle_color(3, 250, 'red')
    main_view.add_subview(sub_view_8)

    main_view.present()

    t = threading.Timer(0.02, schedule, args=[main_view])
    t.start()