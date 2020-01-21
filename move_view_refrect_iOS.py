import ui
import threading

# メインビューの上を移動するビューを定義する。
class MyView(ui.View):
    speed = 1               # 移動するピクセル数。速度。
    direction_x = True      # 横軸に移動する方向を示すフラグ。True=右。False=左。
    direction_y = True      # 縦軸に移動する方向を示すフラグ。True=下。False=上。

    def upper_right(self):
        return (self.x + self.width)

    def lower_left(self):
        return (self.y + self.height)

    # メインビューの端に到達しているかを判別し進行方向を変更する。
    def reflect_mainview(self):
        # 縦軸の進行方向を算出する
        s_height = self.superview.height
        if self.direction_y == True:
            if self.lower_left() >= s_height:
                self.direction_y = False
        else:
            if self.y <= 0:
                self.direction_y = True

        # 横軸の進行方向を算出する
        s_width = self.superview.width
        if self.direction_x == True:
            if self.upper_right() >= s_width:
                self.direction_x = False
        else:
            if self.x <= 0:
                self.direction_x = True

    # サブビューの位置関係を算出し移動する方向を更新する。
    # 2つのViewを包む矩形を変数combined_x, combined_y, combined_w, combined_hに格納する。
    # 2つのViewを包む矩形の縦と横が共に、2つの矩形の縦と横の合計値と同じか小さい場合
    # 2つのViewは接触していると判別し進行方向を変更する。
    def reflect_subview(self):
        for subview in self.superview.subviews:
            if (id(self) != id(subview)):
                combined_x, combined_y, combined_w, combined_h = 0, 0, 0, 0
                if self.x <= subview.x:
                    combined_x = self.x
                else:
                    combined_x = subview.x

                if self.y <= subview.y:
                    combined_y = self.y
                else:
                    combined_y = subview.y

                if self.upper_right() >= subview.upper_right():
                    combined_w = self.upper_right() - combined_x
                else:
                    combined_w = subview.upper_right() - combined_x

                if self.lower_left() >= subview.lower_left():
                    combined_h = self.lower_left() - combined_y
                else:
                    combined_h = subview.lower_left() - combined_y

                if (self.height + subview.height) >= combined_h and \
                    (self.width + subview.width) >= combined_w:
                    if (self.height + subview.height) - combined_h < \
                            (self.width + subview.width) - combined_w:
                        self.direction_y = not (self.direction_y)
                    else:
                        self.direction_x = not (self.direction_x)

    # ビューを移動させる処理
    def move(self):
        self.reflect_subview()
        self.reflect_mainview()

        if self.direction_x == True:
            self.x = self.x + self.speed
        else:
            self.x = self.x - self.speed

        if self.direction_y == True:
            self.y = self.y + self.speed
        else:
            self.y = self.y - self.speed


def schedule(main_view, sub_view_1, sub_view_2):
    sub_view_1.move()
    sub_view_2.move()
    main_view.set_needs_display()

    if main_view.on_screen == True:
        t = threading.Timer(0.01, schedule, args=[main_view, sub_view_1, sub_view_2])
        t.start()


def main():
    # メイン画面の作成
    main_view = ui.View(frame=(0, 0, 375, 667))
    main_view.name = 'Viewを互いに反射させる'
    main_view.background_color = 'lightblue'

    # サブビューの作成
    sub_view_lightgreen = MyView(frame=(0, 0, 150, 150))
    sub_view_lightgreen.background_color = 'lightgreen'
    sub_view_lightgreen.speed = 1
    main_view.add_subview(sub_view_lightgreen)

    # サブビューの追加
    sub_view_red = MyView(frame=(180, 180, 50, 50))
    sub_view_red.background_color = 'red'
    sub_view_red.speed = 2
    main_view.add_subview(sub_view_red)

    main_view.present()

    t = threading.Thread(target=schedule, args=[main_view, sub_view_lightgreen, sub_view_red])
    t.start()


if __name__ == '__main__':
    main()
