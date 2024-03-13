# カーソルに〇がついてくるやつ

import tkinter
import numpy as np
import time

root = tkinter.Tk()
cvs = tkinter.Canvas()

m_pos = np.array([0, 0])


# <Motion>イベントはマウスポインタの位置が変化した時しか呼ばれない
# def move(evt: tkinter.Event):
#     global m_pos
#     m_pos = m_pos + ([evt.x, evt.y] - m_pos) * 0.1
#
#
# root.bind("<Motion>", move)

def get_mouse_pos():
    # https://stackoverflow.com/questions/22925599/mouse-position-python-tkinter
    abs_coord_x = root.winfo_pointerx() - root.winfo_rootx()
    abs_coord_y = root.winfo_pointery() - root.winfo_rooty()
    return np.array([abs_coord_x, abs_coord_y]).astype(float)


OVAL_RADIUS = 5
TARGET_FPS = 60


def main():
    ts = time.time()

    global m_pos
    m_pos = m_pos + (get_mouse_pos() - m_pos) * 0.05

    cvs.delete("all")
    oval_start, oval_end = m_pos - OVAL_RADIUS, m_pos + OVAL_RADIUS
    cvs.create_oval(*oval_start, *oval_end, fill="red")

    te = time.time()
    root.after(int((1 / TARGET_FPS - (te - ts)) * 1000), main)


root.resizable(width=False, height=False)

cvs.pack()
main()
root.mainloop()
