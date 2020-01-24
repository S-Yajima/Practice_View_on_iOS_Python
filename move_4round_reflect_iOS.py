#
# 4つの円をTimerイベントで動かし、メインビューの端との接触および、
# 円同士の接触で反射して進行方向を変えます。
#

import ui
import threading
import math


class MyView(ui.View):
    draw_color = 'yellow'
    speed = 1
    direction_x = True
    direction_y = True

    def upper_right(self):
        return (self.x + self.width)

    def lower_left(self):
        return (self.y + self.height)

    def reflect_main(self):
        if self.x <= 0:
            self.direction_x = True
        elif self.upper_right() >= self.superview.width:
            self.direction_x = False

        if self.y <= 0:
            self.direction_y = True
        elif self.lower_left() >= self.superview.height:
            self.direction_y = False

    # 円同士の反射を判別します。
    # ２つの円の中心のX軸の距離の2乗＋Y軸の距離の2乗の平方根から
    # 中心同士の距離を算出し、互いの半径を足した長さと同じか
    # それ未満であれば接触していると判定します。
    def reflect_subview(self):
        for subview in self.superview.subviews:
            if id(self) != id(subview):
                if math.sqrt(abs(self.center.x - subview.center.x) ** 2 + abs(self.center.y - subview.center.y) ** 2) <= \
                        (self.width / 2) + (subview.width / 2):
                    if self.center.x < subview.center.x:
                        self.direction_x = False
                    else:
                        self.direction_x = True

                    if self.center.y < subview.center.y:
                        self.direction_y = False
                    else:
                        self.direction_y = True

    # ui.Viewのdraw()メソッドで円を描画しています。
    def draw(self):
        path = ui.Path.oval(0, 0, self.width, self.height)
        ui.set_color(self.draw_color)
        path.fill()

    # 移動
    def move(self):
        if self.direction_x == True:
            self.x = self.x + self.speed
        else:
            self.x = self.x - self.speed

        if self.direction_y == True:
            self.y = self.y + self.speed
        else:
            self.y = self.y - self.speed

# Timer
def schedule(main_view):
    for sub_view in main_view.subviews:
        sub_view.reflect_subview()
        sub_view.reflect_main()

    for sub_view in main_view.subviews:
        sub_view.move()

    main_view.set_needs_display()

    if main_view.on_screen == True:
        t = threading.Timer(0.02, schedule, args=[main_view])
        t.start()


if __name__ == '__main__':
    # メイン画面の作成
    main_view = ui.View(frame=(0, 0, 375, 667))
    main_view.name = 'Viewに円を描画し動かす'
    main_view.background_color = 'lightblue'

    # サブビューの追加
    sub_view_1 = MyView(frame=(100, 100, 120, 120))
    sub_view_1.draw_color = 'yellow'
    main_view.add_subview(sub_view_1)

    sub_view_2 = MyView(frame=(200, 300, 80, 80))
    sub_view_2.draw_color = 'blue'
    sub_view_2.speed = 2
    main_view.add_subview(sub_view_2)

    sub_view_3 = MyView(frame=(300, 300, 60, 60))
    sub_view_3.draw_color = 'red'
    sub_view_3.speed = 3
    main_view.add_subview(sub_view_3)

    sub_view_4 = MyView(frame=(40, 300, 140, 140))
    sub_view_4.draw_color = 'green'
    sub_view_4.speed = 1
    main_view.add_subview(sub_view_4)

    main_view.present()

    t = threading.Timer(0.01, schedule, args=[main_view])
    t.start()