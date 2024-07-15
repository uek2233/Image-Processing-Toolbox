import tkinter as tk
import tkinter.messagebox as tm
from tkinter import filedialog
import os
import shutil
from PIL import Image
import subprocess


class CF(object):
    def __init__(self, parent, cp):
        self.cp = cp
        self.output_dir = None
        self.default_path = self.check_path()
        self.user_path = None
        self.save_path = None
        self.supported_formats = ['png', 'jpg', 'jpeg', 'bmp', 'webp', 'svg']
        self.frame = tk.Frame(parent, bg='skyblue')
        self.t = tk.Text(self.frame, height=5)
        self.b = tk.Button(self.frame, text='运行', bg='#FFF68F', command=self.run)
        self.var = tk.StringVar()
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
                            from_=1,
                            to=95,
                            orient=tk.HORIZONTAL,
                            length=200,
                            showvalue=True,  # 是否显示当前滑块的值
                            tickinterval=21,
                            resolution=1
                        )

    def init(self):
        self.t.place(x=20, y=80, width=360, height=100)
        self.b.place(x=345, y=20)
        self.var.set('A')
        self.select_save_path()
        self.r1.place(x=20, y=5)
        self.r2.place(x=20, y=35)
        self.s.set(85)
        self.s.place(x=130, y=0)

    def run(self):
        t_n = 0
        f_n = 0
        if self.save_path == self.default_path:
            self.delay_image()
        fp, fn, fs = self.choose_files()
        for i in range(len(fs)):
            if fs[i] in self.supported_formats:
                t_n += 1
                op = os.path.join(self.save_path, fn[i].split('.')[0]) + '.' + fs[i]
                self.t.insert('insert', f'压缩完成: {fp[i]}\n')
                self.zip(fp[i], op)
            else:
                f_n += 1
                self.t.insert('insert', f'非法文件: {fp[i]}\n')
        self.t.insert('1.0', f'成功压缩{t_n}个文件，压缩失败{f_n}个文件。\n')
        subprocess.Popen(f'explorer "{os.path.abspath(self.save_path)}"')

    def zip(self, ip, op):
        image = Image.open(ip)
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        image.save(op, "jpeg", optimize=True, quality=int(self.s.get()))

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

    def choose_files(self):
        files_path = []
        files_name = []
        files_suffix = []
        file_paths = filedialog.askopenfilenames(
            title="Select Files",
            filetypes=[("All files", "*.*"), ("PNG files", "*.png"), ("JPG files", "*.jpg"), ("JPG files", "*.jpeg")]
        )
        self.t.delete('1.0', 'end')
        for file_path in file_paths:
            self.t.insert('insert', f'导入: {file_path}\n')
            file_name = file_path.split('/')[-1]
            file_suffix = file_path.split('.')[-1]
            files_path.append(file_path)
            files_name.append(file_name)
            files_suffix.append(file_suffix)
        return files_path, files_name, files_suffix

    def check_path(self):
        dir_path = os.path.dirname(self.cp)
        output_path = os.path.join(dir_path, 'output')
        self.output_dir = output_path
        output_c_path = os.path.join(output_path, 'image_compression')
        output_r_path = os.path.join(output_path, 'image_resizing')
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        if not os.path.exists(output_c_path):
            os.makedirs(output_c_path)
        if not os.path.exists(output_r_path):
            os.makedirs(output_r_path)
        return output_c_path

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
