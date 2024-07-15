import os
import shutil
import tkinter.messagebox as tm


def clear(path):
    folder_path = path
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
                tm.showinfo(title='通知', message=f'Failed to delete {file_path}. Reason: {e}')
                # print('insert', f'Failed to delete {file_path}. Reason: {e}')
        tm.showinfo(title='通知', message=f'{path} 文件夹清理完成')
    else:
        tm.showinfo(title='通知', message=f'The folder {folder_path} does not exist.')
        # print('insert', f'The folder {folder_path} does not exist.')
