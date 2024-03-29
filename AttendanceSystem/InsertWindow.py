import tkinter as tk
from tkinter import ttk

import cv2

from FaceRecognition.FaceCollect import faceCollect
from FaceRecognition.FeatureCompute import featureCompute
from AttendanceSystem.Employee import CheckName, CheckPosition, CheckSalary, CheckAge, CheckGender


class InsertWindow:
    def __init__(self, master, parentMaster=None):
        self.master = master
        self.parentMaster = parentMaster

        self.master.title("增加人员")
        self.frame = ttk.Frame(master, padding="10")
        self.frame.grid(row=0, column=0)

        # 创建标题
        titleLabel = ttk.Label(self.frame, text="增加人员窗口\n", font=("", 20), foreground="blue")
        titleLabel.grid(row=0, column=0, columnspan=2)

        # 姓名
        self.nameLabel = ttk.Label(self.frame, text="姓名: ")
        self.nameLabel.grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(0, 18))
        self.nameEntry = ttk.Entry(self.frame)
        self.nameEntry.grid(row=1, column=1, pady=(0, 18))

        # 职位
        self.positionLabel = ttk.Label(self.frame, text="职位: ")
        self.positionLabel.grid(row=3, column=0, sticky=tk.W, padx=(0, 10), pady=(0, 18))
        self.positionEntry = ttk.Entry(self.frame)
        self.positionEntry.grid(row=3, column=1, pady=(0, 18))

        # 薪资
        self.salaryLabel = ttk.Label(self.frame, text="薪资: ")
        self.salaryLabel.grid(row=5, column=0, sticky=tk.W, padx=(0, 10), pady=(0, 18))
        self.salaryEntry = ttk.Entry(self.frame)
        self.salaryEntry.grid(row=5, column=1, pady=(0, 18))

        # 年龄
        self.ageLabel = ttk.Label(self.frame, text="年龄: ")
        self.ageLabel.grid(row=7, column=0, sticky=tk.W, padx=(0, 10), pady=(0, 18))
        self.ageEntry = ttk.Entry(self.frame)
        self.ageEntry.grid(row=7, column=1, pady=(0, 18))

        # 性别
        self.genderLabel = ttk.Label(self.frame, text="性别: ")
        self.genderLabel.grid(row=9, column=0, sticky=tk.W, padx=(0, 10), pady=(0, 18))
        self.genderCombobox = ttk.Combobox(self.frame, values=["男", "女"], state="readonly", width=17)
        self.genderCombobox.grid(row=9, column=1, pady=(0, 18))

        self.faceVar = tk.IntVar()
        self.faceVar.set(0)

        self.insertVar = tk.IntVar()
        self.insertVar.set(0)

        # 创建人脸录入成功与否的提示标签
        self.faceInsertResultToggle = ttk.Checkbutton(self.frame, text="", state=tk.DISABLED, variable=self.faceVar)
        self.faceInsertResultToggle.grid(row=11, column=0, padx=(0, 10), pady=(0, 10))

        # 创建录入人脸按钮
        confirmButton = ttk.Button(self.frame, text="录入人脸", width=25, command=self.faceInsertCmd)
        confirmButton.grid(row=11, column=1, pady=(0, 10))

        # 暂时保存录入的人脸信息
        self.faceInfo = None

        # 创建一个添加人员成功的提示标签
        self.employeeInsertResultToggle = ttk.Checkbutton(self.frame, text="", state=tk.DISABLED,
                                                          variable=self.insertVar)
        self.employeeInsertResultToggle.grid(row=12, column=0, padx=(0, 10))

        # 创建确认添加按钮
        confirmButton = ttk.Button(self.frame, text="确认添加", width=25, command=self.employeeInsertCmd)
        confirmButton.grid(row=12, column=1)

        # 创建一个提示标签
        self.tipLabel = ttk.Label(self.frame, text="\n", foreground="red")
        self.tipLabel.grid(row=13, column=0, columnspan=2)

    def faceInsertCmd(self):
        print("录入人脸")
        faceImageList = faceCollect.GetFaceListFromVideo(self.parentMaster.camera)
        self.faceInfo = featureCompute.GetMeanFeature(faceImageList)
        self.faceVar.set(1)

    def employeeInsertCmd(self):
        print("确认添加")
        name = self.nameEntry.get()
        position = self.positionEntry.get()
        salary = self.salaryEntry.get()
        age = self.ageEntry.get()
        gender = self.genderCombobox.get()

        # 提示词先清空
        self.tipLabel.config(text="")

        if self.faceVar.get() == 0:
            self.tipLabel.config(text="请先录入人脸")
            return

        tipLabelText = "以下内容不合法:(请检查后重新输入)\n"

        if not CheckName(name):
            tipLabelText += "姓名\n"
        if not CheckPosition(position):
            tipLabelText += "职位\n"
        if not CheckSalary(salary):
            tipLabelText += "薪资\n"
        if not CheckAge(age):
            tipLabelText += "年龄\n"
        if not CheckGender(gender):
            tipLabelText += "性别\n"

        if tipLabelText != "以下内容不合法:(请检查后重新输入)\n":
            self.tipLabel.config(text=tipLabelText)
            return

        self.insertVar.set(1)
        self.faceInsertResultToggle.after(2000, lambda: self.faceVar.set(0))
        self.employeeInsertResultToggle.after(2000, lambda: self.insertVar.set(0))

        # TODO: 添加到数据库
        # 添加成功提示
        self.tipLabel.config(text="添加成功")
        self.tipLabel.after(2000, lambda: self.tipLabel.config(text=""))


if __name__ == "__main__":
    # 创建主窗口
    root = tk.Tk()
    root_1 = tk.Tk()
    root_1.title("摄像头")
    root_1.camera = cv2.VideoCapture(0)
    # 创建 AddPersonWindow 实例作为主窗口的子窗口
    insertWindow = InsertWindow(root, root_1)
    # 开始主循环
    root.mainloop()
