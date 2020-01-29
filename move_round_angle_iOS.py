
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
    # x軸 = cos 角度
    # y軸 = sin 角度
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


def schedule(main_view):
    for sub_view in main_view.subviews:
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
    main_view.name = '進む角度を設定した円を描画し動かす'
    main_view.background_color = 'lightblue'
    # main_view.background_color = 'black'

    sub_view_1 = MyView(frame=(100, 100, 70, 70))
    sub_view_1.set_speed_angle_color(3, 20, 'yellow')
    main_view.add_subview(sub_view_1)

    sub_view_2 = MyView(frame=(200, 110, 70, 70))
    sub_view_2.set_speed_angle_color(3, 20, 'blue')
    main_view.add_subview(sub_view_2)

    sub_view_3 = MyView(frame=(300, 120, 70, 70))
    sub_view_3.set_speed_angle_color(3, 20, 'red')
    main_view.add_subview(sub_view_3)

    sub_view_4 = MyView(frame=(300, 500, 70, 70))
    sub_view_4.set_speed_angle_color(3, 250, 'yellow')
    main_view.add_subview(sub_view_4)

    sub_view_5 = MyView(frame=(290, 400, 70, 70))
    sub_view_5.set_speed_angle_color(3, 250, 'blue')
    main_view.add_subview(sub_view_5)

    sub_view_6 = MyView(frame=(280, 300, 70, 70))
    sub_view_6.set_speed_angle_color(3, 250, 'red')
    main_view.add_subview(sub_view_6)

    main_view.present()

    t = threading.Timer(0.02, schedule, args=[main_view])
    t.start()