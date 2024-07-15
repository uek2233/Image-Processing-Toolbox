import tkinter as tk
from compression import CF
from resizing import RF
from clear import clear
import os
import subprocess


def show_frame(n, parent):
    pf = os.path.abspath(__file__)
    cf = CF(parent, pf)
    rf = RF(parent, pf)
    cf.init()
    rf.init()
    frame1 = cf.frame
    frame2 = rf.frame
    if n == 1:
        frame2.destroy()
        frame1.place(x=0, width=400, height=200)
    elif n == 2:
        frame1.destroy()
        frame2.place(x=0, width=400, height=200)
    elif n == 3:
        clear(cf.output_dir)
    elif n == 4:
        subprocess.Popen(f'explorer "{os.path.abspath(cf.output_dir)}"')


window = tk.Tk()
window.title('图片处理工具')
window.geometry('400x200')

menubar = tk.Menu(window)
menubar.add_command(label='图片压缩', command=lambda: show_frame(1, window))
menubar.add_command(label='图片缩小', command=lambda: show_frame(2, window))
img_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='其他', menu=img_menu)
img_menu.add_command(label='图片清理', command=lambda: show_frame(3, window))
img_menu.add_command(label='打开文件夹', command=lambda: show_frame(4, window))

show_frame(1, window)
window.config(menu=menubar)
window.mainloop()
