import tkinter as tk
from tkinter import ttk


class QueryWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("查询界面")

        # 划分左右两个Frame
        self.leftFrame = ttk.Frame(self)
        self.leftFrame.grid(row=0, column=0, padx=10, pady=10)

        self.rightFrame = ttk.Frame(self)
        self.rightFrame.grid(row=0, column=1, padx=10, pady=10)

        # 创建一个标签作为标题
        self.titleLabel = ttk.Label(self.leftFrame, text="查询界面\n", font=("", 20), foreground="blue")
        self.titleLabel.grid(row=0, column=0, columnspan=2)

        # 创建一个标签作为提示语
        self.tooltipLabel = ttk.Label(self.leftFrame, text="选择查询条件\n", font=("", 10))
        self.tooltipLabel.grid(row=1, column=0)

        # 创建两个复选框
        self.nameVar = tk.IntVar()
        self.idVar = tk.IntVar()

        # 复选框字体大小
        style = ttk.Style()
        style.configure("TCheckbutton", font=("", 12))

        self.nameCheck = ttk.Checkbutton(self.leftFrame, text="姓名", variable=self.nameVar, onvalue=1, offvalue=0,
                                         style="TCheckbutton", command=self.nameSelectCmd)
        self.nameCheck.grid(row=2, column=0, sticky='w')

        # 创建一个空白标签, 用于美观
        self.spaceLabel = ttk.Label(self.leftFrame, text=" ")
        self.spaceLabel.grid(row=3, column=0)

        self.idCheck = ttk.Checkbutton(self.leftFrame, text="编号", variable=self.idVar, onvalue=1, offvalue=0,
                                       style="TCheckbutton", command=self.idSelectCmd)
        self.idCheck.grid(row=4, column=0, sticky='w')

        # 创建输入框
        self.inputBox = ttk.Entry(self.leftFrame)
        self.inputBox.grid(row=2, column=1, rowspan=1)

        # 创建确认按钮
        self.confirmButton = ttk.Button(self.leftFrame, text="查询", command=self.confirmButtonClick, width=20)
        self.confirmButton.grid(row=4, column=1)

        # 创建用于显示查询结果的文本框
        self.queryResults = tk.Text(self.rightFrame, width=60, height=20)
        self.queryResults.grid(row=0, column=0)

    def nameSelectCmd(self):
        # 根据当前勾选的复选框状态，取消另一个复选框的勾选状态
        if self.nameVar.get() == 1:
            self.idVar.set(0)

    def idSelectCmd(self):
        if self.idVar.get() == 1:
            self.nameVar.set(0)

    def confirmButtonClick(self):
        # 获取输入框的内容
        inputText = self.inputBox.get()
        # 根据复选框的状态，执行相应的操作
        if self.nameVar.get() == 1:
            # Name被勾选
            # 在右侧文本框中显示查询结果
            self.queryResults.insert(tk.END, f"查询Name: {inputText}\n")
        elif self.idVar.get() == 1:
            # ID被勾选
            # 在右侧文本框中显示查询结果
            self.queryResults.insert(tk.END, f"查询ID: {inputText}\n")


if __name__ == '__main__':
    root = tk.Tk()
    queryWindow = QueryWindow(root)
    root.mainloop()
