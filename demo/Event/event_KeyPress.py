#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""通过键盘方向键控制目标移动"""

from tkinter import Tk, Canvas


def app():
    """app"""
    win = Tk()
    canvas = Canvas(win, width=400, height=400)  # 设置画布
    canvas.pack()  # 显示画布

    def moverectangle(event):
        """绑定方向键"""
        if event.keysym == "Up":
            canvas.move(
                1, 0, -5)  # 移动的是 ID为1的事物【move（2,0,-5）则移动ID为2的事物】，使得横坐标加0，纵坐标减5
        elif event.keysym == "Down":
            canvas.move(1, 0, 5)
        elif event.keysym == "Left":
            canvas.move(1, -5, 0)
        elif event.keysym == "Right":
            canvas.move(1, 5, 0)

    # 事件ID可能跟程序的先后顺序有关，例如，下面先创建了200*200的矩形，后创建了20*20的矩形
    r = canvas.create_rectangle(180, 180, 220, 220, fill="red")  # 事件ID为1
    print(r)  # 打印ID验证一下
    m = canvas.create_rectangle(10, 10, 20, 20, fill="blue")  #事件ID为2
    print(m)  # 打印ID验证一下
    canvas.bind_all("<KeyPress-Up>", moverectangle)  #绑定方向键与函数
    canvas.bind_all("<KeyPress-Down>", moverectangle)
    canvas.bind_all("<KeyPress-Left>", moverectangle)
    canvas.bind_all("<KeyPress-Right>", moverectangle)
    win.mainloop()


if __name__ == '__main__':
    app()
