# クリックすると状態が変化する図形（オブジェクト指向版）

import tkinter

root = tkinter.Tk()  # Tkを生成
root.resizable(width=False, height=False)  # ウィンドウのサイズを変更できないようにする
root.geometry("500x200")  # ウィンドウのサイズを指定する（ピクセル単位）
cvs = tkinter.Canvas(root)  # 図形や画像を描画するキャンバスを作成する
cvs.pack(fill="both", expand=True)  # キャンバスをウィンドウ全体に広がるように配置する


class Object:
    def __init__(self, x, y, radius, state=0):
        self.__x = x  # x座標
        self.__y = y  # y座標
        self.__radius = radius  # 半径
        self.__state = state  # 状態を表す数値

    def render(self, cvs: tkinter.Canvas):
        # 描画
        fill_color = "Red" if self.__state == 0 else "Blue"  # 色は状態によって変える
        cvs.create_oval(
            self.__x - self.__radius,
            self.__y - self.__radius,
            self.__x + self.__radius,
            self.__y + self.__radius,
            fill=fill_color,
        )

    def switch_state(self):
        # 状態切り替え
        if self.__state == 0:
            self.__state = 1
        else:
            self.__state = 0

    def __contains__(self, p: tuple[int, int]):
        x, y = p
        # 点が物体に含まれるか判定
        return (self.__x - x) ** 2 + (self.__y - y) ** 2 < self.__radius ** 2


objects = []  # すべての物体


# 物体の位置と状態の初期化
def init_objects():
    for i in range(3):  # 物体それぞれについて
        x, y = 25 + i * 50, 50
        obj = Object(x=x, y=y, radius=25)
        objects.append(obj)


init_objects()


# クリックされたら呼ばれる
def clicked(e: tkinter.Event):
    for obj in objects:  # 物体それぞれについて
        if (e.x, e.y) in obj:  # マウスポインタの位置が物体に含まれていたら
            obj.switch_state()  # 物体の状態を切り替える


root.bind("<Button-1>", clicked)


# メインで行う描画処理
def render():
    for obj in objects:
        obj.render(cvs)


def main():
    cvs.delete("all")  # 全部消す
    render()  # 描画する
    root.after(1000 // 60, main)  # 60FPS


main()
root.mainloop()  # Tkのメインループに入る
