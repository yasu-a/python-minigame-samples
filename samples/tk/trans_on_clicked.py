# クリックすると状態が変化する図形

import tkinter

root = tkinter.Tk()  # Tkを生成
root.resizable(width=False, height=False)  # ウィンドウのサイズを変更できないようにする
root.geometry("500x200")  # ウィンドウのサイズを指定する（ピクセル単位）
cvs = tkinter.Canvas(root)  # 図形や画像を描画するキャンバスを作成する
cvs.pack(fill="both", expand=True)  # キャンバスをウィンドウ全体に広がるように配置する

N_ENTITIES = 3  # 物体の数
object_x = []  # 物体のx座標
object_y = []  # 物体のy座標
object_state = []  # 物体の状態


# 物体の位置と状態の初期化
def init_objects():
    for i in range(N_ENTITIES):  # 物体それぞれについて
        x, y, state = 25 + i * 50, 50, 0
        object_x.append(x)
        object_y.append(y)
        object_state.append(state)


init_objects()


# クリックされたら呼ばれる
def clicked(e: tkinter.Event):
    global object_state

    for i in range(N_ENTITIES):  # 物体それぞれについて
        x, y = object_x[i], object_y[i]  # x, y座標（円の中心）を取り出して
        if (x - e.x) ** 2 + (y - e.y) ** 2 < 25 ** 2:  # 物体のx, y座標からマウスポインタの距離が25未満なら
            # その物体の状態を切り替える
            if object_state[i] == 0:
                object_state[i] = 1
            else:
                object_state[i] = 0


root.bind("<Button-1>", clicked)


# メインで行う描画処理
def render():
    for i in range(N_ENTITIES):
        x, y, state = object_x[i], object_y[i], object_state[i]
        if state == 0:
            fill_color = "Red"
        else:
            fill_color = "Blue"
        cvs.create_oval(x - 25, y - 25, x + 25, y + 25, fill=fill_color)


def main():
    cvs.delete("all")  # 全部消す
    render()  # 描画する
    root.after(1000 // 60, main)  # 60FPS


main()
root.mainloop()  # Tkのメインループに入る
