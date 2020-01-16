#
# サブビューがメインビュー上を移動する
# サブビューがメインビューの端に到達すると反射する
# ビューの移動はサブビューのframeの数値の変更により行う。
# 描画はメインビューのメソッドset_needs_display()によって実行する。
# iOS上でのみ動作する
#

import ui
import console
import time
import threading

# ui.View を継承する
# Timer実行ごとに移動する速度(pixel数)と縦横移動する方向をメンバに保持する
class MyView(ui.View):
    speed = 1
    direction_x = True
    direction_y = True

    # メインビュー上を移動する。自身(サブビュー)のframeの値を計算する。
    def move(self):
        if self.direction_y == True:
            if self.y + self.height >= self.superview.height:
                self.direction_y = False
        else:
            if self.y <= 0:
                self.direction_y = True

        if self.direction_x == True:
            if self.x + self.width >= self.superview.width:
                self.direction_x = False
        else:
            if self.x <= 0:
                self.direction_x = True

        if self.direction_x == True:
            self.x = self.x + self.speed
        else:
            self.x = self.x - self.speed

        if self.direction_y == True:
            self.y = self.y + self.speed
        else:
            self.y = self.y - self.speed

# Timerによって繰り返し呼び出されるイベント関数
# 複数のViewを引数にとる
def schedule(main_view, sub_view, sub_view_2):
    sub_view.move()
    sub_view_2.move()
    main_view.set_needs_display()

    t = threading.Timer(0.01, schedule, args=[main_view, sub_view, sub_view_2])
    t.start()


def main():
    # メイン画面の作成
    main_view = MyView(frame=(0, 0, 375, 667))
    main_view.name = 'Viewの練習'
    main_view.background_color = 'lightblue'

    # サブビューの作成
    sub_view = MyView(frame=(0, 0, 120, 120))
    sub_view.background_color = 'lightgreen'
    main_view.add_subview(sub_view)

    # サブビューの追加
    sub_view_2 = MyView(frame=(180, 80, 50, 50))
    sub_view_2.background_color = 'red'
    sub_view_2.speed = 3
    main_view.add_subview(sub_view_2)
    # メインビューを描画する。サブビューも自動的に描画される。
    main_view.present()

    t = threading.Thread(target=schedule, args=[main_view, sub_view, sub_view_2])
    t.start()


if __name__ == '__main__':
    main()