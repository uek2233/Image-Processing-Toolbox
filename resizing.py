import tkinter as tk
import tkinter.messagebox as tm
from tkinter import filedialog
import os
import shutil
from PIL import Image
import subprocess


def select_file(text_widget):
    file_paths = filedialog.askopenfilename(
        title="Select Files",
        filetypes=[("All files", "*.*"), ("PNG files", "*.png"), ("JPG files", "*.jpg")]
    )
    # 打印选中的文件路径
    for file_path in file_paths:
        print(file_path)
        text_widget.insert('insert', file_path + '\n')


def resizing_frame(parent):
    frame = tk.Frame(parent, bg='orange')
    t = tk.Text(frame, height=5)
    t.place(x=20, y=80, width=360, height=100)
    b = tk.Button(frame, text='select file', command=lambda: select_file(t))
    b.pack()
    return frame


class RF(object):
    def __init__(self, parent, cp):
        self.cp = cp
        self.default_path = self.check_path()
        self.user_path = None
        self.save_path = None
        self.ip = ''
        self.op = ''
        self.w = 0
        self.h = 0
        self.rate = 0
        self.run_num = 0
        self.supported_formats = ['png', 'jpg', 'jpeg', 'bmp', 'webp', 'svg']
        self.frame = tk.Frame(parent, bg='skyblue')
        self.t = tk.Text(self.frame)
        self.var = tk.StringVar()
        self.var1 = tk.StringVar()
        self.var2 = tk.StringVar()
        self.var3 = tk.StringVar()
        self.l1 = tk.Label(self.frame, text='原始分辨率:', bg='skyblue')
        self.l2 = tk.Label(self.frame, text='缩放后分辨率:', bg='skyblue')
        self.l3 = tk.Label(self.frame, textvariable=self.var1, bg='skyblue')
        self.l4 = tk.Label(self.frame, textvariable=self.var2, bg='skyblue')
        self.b1 = tk.Button(self.frame, textvariable=self.var3, bg='#FFF68F', command=self.run)
        self.r1 = tk.Radiobutton(self.frame,
                                 bg='skyblue',
                                 text='默认保存路径',
                                 variable=self.var,
                                 value='A',
                                 command=self.select_save_path)
        self.r2 = tk.Radiobutton(self.frame,
                                 bg='skyblue',
                                 text='选择保存路径',
                                 variable=self.var,
                                 value='B',
                                 command=self.select_save_path)
        self.s = tk.Scale(
                            self.frame,
                            # label='压缩比例',
                            bg='skyblue',
                            highlightbackground='skyblue',
                            from_=0,
                            to=100,
                            orient=tk.HORIZONTAL,
                            length=360,
                            showvalue=True,  # 是否显示当前滑块的值
                            tickinterval=25,
                            resolution=1,
                            command=self.show_rate)

    def init(self):
        self.t.place(x=20, y=130, width=360, height=50)
        self.var.set('A')
        self.var3.set('文件')
        self.select_save_path()
        self.r1.place(x=20, y=5)
        self.r2.place(x=20, y=35)
        self.s.place(x=20, y=60)
        self.s.set(50)
        self.rate = self.s.get()
        self.l1.place(x=150, y=7)
        self.l2.place(x=150, y=37)
        self.l3.place(x=240, y=7)
        self.l4.place(x=240, y=37)
        self.b1.place(x=345, y=20)
        # self.b2.place(x=345, y=45)

    def run(self):
        self.run_num += 1
        if self.save_path == self.default_path:
            self.delay_image()
        if self.var3.get() == '文件' and self.run_num == 1:
            self.choose_image()
            self.var3.set('运行')
            self.var2.set(f'{int(self.w*0.5)}x{int(self.h*0.5)}')
            # self.frame.update()

        if self.var3.get() == '运行' and self.run_num == 2:
            nw = int(self.w * self.rate / 100)
            nh = int(self.h * self.rate / 100)
            size = tuple([nw, nh])
            self.reshape(self.ip, self.op, size)
            self.var3.set('文件')
            self.run_num = 0
            subprocess.Popen(f'explorer "{os.path.abspath(self.save_path)}"')

    def show_rate(self, v):
        if self.var3.get() == '运行':
            self.rate = int(v)
            nw = int(self.w * self.rate / 100)
            nh = int(self.h * self.rate / 100)
            self.var2.set(f'{nw}x{nh}')
            return nw, nh

    def choose_image(self):
        fp, fn, fs = self.choose_file()
        self.ip = fp
        if fp == '':
            tm.showwarning(title='警告', message='未选择图片文件')
        else:
            if fs in self.supported_formats:
                self.image_meg(fp)
                self.op = os.path.join(self.save_path, fn.split('.')[0]) + '.' + fs

    def image_meg(self, ip):
        image = Image.open(ip)
        width, height = image.size
        self.var1.set(f'{width}x{height}')
        self.w = width
        self.h = height

    @staticmethod
    def reshape(ip, op, size):
        with Image.open(ip) as img:
            img.thumbnail(size)
            img.save(op)

    def select_save_path(self):
        if self.var.get() == 'A':
            self.t.delete('1.0', 'end')  # 清空text,从第一行第一个字开始到最后一个字结束
            self.t.insert('insert', '使用默认路径:' + self.default_path + '\n')
            self.save_path = self.default_path
        elif self.var.get() == 'B':
            self.user_path = filedialog.askdirectory()
            self.t.delete('1.0', 'end')
            self.save_path = self.user_path
            if self.save_path == '':
                tm.showwarning(title='警告', message='未选择保存文件夹')
            else:
                self.t.insert('insert', '用户指定路径:' + self.user_path + '\n')

    def choose_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Files",
            filetypes=[("All files", "*.*"), ("PNG files", "*.png"), ("JPG files", "*.jpg"), ("JPG files", "*.jpeg")]
        )
        self.t.delete('1.0', 'end')
        self.t.insert('insert', f'导入: {file_path}\n')
        file_name = file_path.split('/')[-1]
        file_suffix = file_path.split('.')[-1]
        return file_path, file_name, file_suffix

    def check_path(self):
        dir_path = os.path.dirname(self.cp)
        output_path = os.path.join(dir_path, 'output')
        output_c_path = os.path.join(output_path, 'image_compression')
        output_r_path = os.path.join(output_path, 'image_resizing')
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        if not os.path.exists(output_c_path):
            os.makedirs(output_c_path)
        if not os.path.exists(output_r_path):
            os.makedirs(output_r_path)
        return output_r_path

    def delay_image(self):
        folder_path = self.save_path
        if os.path.exists(folder_path):
            # 遍历文件夹中的所有文件和子文件夹
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                try:
                    # 检查路径是文件还是文件夹
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)  # 删除文件或符号链接
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)  # 删除文件夹及其所有内容
                except Exception as e:
                    self.t.insert('insert', f'Failed to delete {file_path}. Reason: {e}')
        else:
            self.t.insert('insert', f'The folder {folder_path} does not exist.')
