import tkinter as tk
from tkinter import ttk, Entry, Label

import cv2
from PIL import Image, ImageTk

from AttendanceSystem.Manager import manager


class AdminGui:
    def __init__(self, master):
        self.master = master
        master.title("管理员界面")

        # 左侧按钮容器
        left_frame = tk.Frame(master, padx=20, pady=20)
        left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # 在顶部居中显示Label
        label = tk.Label(master, text="管理员界面", font=("Helvetica", 20))
        label.pack(side=tk.TOP, pady=20)

        # 创建按钮样式
        self.style = ttk.Style()
        # 设置按钮样式，包括宽度和高度
        self.style.configure("TButton", padding=(10, 5, 10, 5), width=30, height=15)

        # 左侧按钮
        btnAdd = ttk.Button(left_frame, text="新增人员", command=self.addPerson, style="TButton")
        btnView = ttk.Button(left_frame, text="查看人员信息", command=self.viewPerson, style="TButton")
        btnEdit = ttk.Button(left_frame, text="修改人员信息", command=self.editPerson, style="TButton")
        btnDelete = ttk.Button(left_frame, text="删除人员", command=self.deletePerson, style="TButton")

        btnAdd.pack(side=tk.TOP, pady=10)
        btnView.pack(side=tk.TOP, pady=10)
        btnEdit.pack(side=tk.TOP, pady=10)
        btnDelete.pack(side=tk.TOP, pady=10)

        # 右侧摄像头输入流显示框
        self.videoLabel = ttk.Label(master)
        self.videoLabel.pack(side=tk.RIGHT, padx=10)

        # 打开摄像头
        self.cap = cv2.VideoCapture(0)
        self.showVideo()

    def showVideo(self):
        _, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.videoLabel.imgtk = imgtk
        self.videoLabel.configure(image=imgtk)
        self.videoLabel.after(10, self.showVideo)  # 10ms后调用showVideo

    def addPerson(self):
        # 实现新增人员的逻辑
        AddPersonWindow(self.master, self)
        pass

    def viewPerson(self):
        # 实现查看人员信息的逻辑
        pass

    def editPerson(self):
        # 实现修改人员信息的逻辑
        pass

    def deletePerson(self):
        # 实现删除人员的逻辑
        pass


class AddPersonWindow(tk.Toplevel):
    def __init__(self, master, adminGui):
        tk.Toplevel.__init__(self, master)
        self.title("新增人员窗口")
        self.adminGui = adminGui  # 保存AdminGUI实例

        # 创建第1行的Label和Entry
        self.labelName = Label(self, text="姓名:")
        self.entryName = Entry(self)
        self.labelName.grid(row=1, column=0, padx=10, pady=10)
        self.entryName.grid(row=1, column=1, padx=10, pady=10)

        # 创建录入人脸按钮
        self.faceButton = ttk.Button(self, text="录入人脸", command=self.recordFace, style="TButton")
        self.faceButton.grid(row=2, column=0, columnspan=2, pady=10)

        # 成员变量保存Id和姓名
        self.personId = None
        self.personName = None

    def recordFace(self):
        # 获取输入的Id和姓名
        self.personName = self.entryName.get()

        # 实现录入人脸的逻辑，可以使用self.personId和self.personName和self.adminGui.cap
        manager.AddPerson(self.personName, self.adminGui.cap)

    def checkName(self, _name: str):
        # 检查姓名是否正确
        pass


if __name__ == '__main__':
    root = tk.Tk()
    app = AdminGui(root)
    root.geometry("1000x600")
    root.mainloop()
