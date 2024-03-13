import tkinter

root = tkinter.Tk()  # Tkを生成
root.resizable(width=False, height=False) # ウィンドウのサイズを変更できないようにする
root.geometry("500x200")  # ウィンドウのサイズを指定する（ピクセル単位）
cvs = tkinter.Canvas(root)  # 図形や画像を描画するキャンバスを作成する
cvs.pack(fill="both", expand=True)  # キャンバスをウィンドウ全体に広がるように配置する
root.mainloop()  # Tkのメインループに入る
