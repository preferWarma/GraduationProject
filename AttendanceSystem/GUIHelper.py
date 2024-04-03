import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox
from SqlController import sqlController


def AddScrollbarToText(text_widget):
    """
    为Text组件添加滚动条
    :param text_widget: 需要添加滚动条的Text组件, 通常为tk.Text, 需要放在Frame中且含有master属性 (master属性为Text所在的容器)
    """
    container = text_widget.master  # 获取Text所在的容器（通常为Frame）

    scrollbar = ttk.Scrollbar(container, orient="vertical", command=text_widget.yview)  # 创建Scrollbar, 设置纵向滚动
    scrollbar.grid(row=0, column=1, sticky="ns")  # 将Scrollbar放在Text的右侧
    text_widget.config(yscrollcommand=scrollbar.set)  # 设置Text的纵向滚动命令为Scrollbar的set方法

    # 设置网格布局的权重，以便调整大小时Text和Scrollbar可以适应
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)


class InsertRecordWindow(tk.Toplevel):
    def __init__(self, parent, onExit: callable = None):
        """
        创建一个选择时间的窗口, 用于选择年、月、日、时、分、秒, 并返回选择的时间
        :param parent: 父窗口, 需要有一个idEntry组件, 用于判断当前的人员编号
        """
        super().__init__(parent)
        self.parent = parent

        self.title("选择时间")
        self.geometry("265x275")

        # 添加窗口关闭的回调函数
        self.onExit = onExit

        # 设置对应的变量
        self.yearVar = tk.StringVar()
        self.monthVar = tk.StringVar()
        self.dayVar = tk.StringVar()
        self.hourVar = tk.StringVar()
        self.minuteVar = tk.StringVar()
        self.secondVar = tk.StringVar()

        # 设置默认值为当前时间
        datetime_now = datetime.now()
        self.yearVar.set(str(datetime_now.year))
        self.monthVar.set(str(datetime_now.month))
        self.dayVar.set(str(datetime_now.day))
        self.hourVar.set(str(datetime_now.hour))
        self.minuteVar.set(str(datetime_now.minute))
        self.secondVar.set(str(datetime_now.second))

        # 创建控件: 年、月、日、时、分、秒
        ttk.Label(self, text="Year:").grid(row=0, column=0, padx=5, pady=5)
        self.yearCombobox = ttk.Combobox(self, textvariable=self.yearVar, state="readonly",
                                         values=[str(year) for year in range(1900, 2100)], width=12)
        self.yearCombobox.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self, text="Month:").grid(row=1, column=0, padx=5, pady=5)
        self.monthCombobox = ttk.Combobox(self, textvariable=self.monthVar, state="readonly",
                                          values=[str(month) for month in range(1, 13)], width=12)
        self.monthCombobox.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self, text="Day:").grid(row=2, column=0, padx=5, pady=5)
        self.dayCombobox = ttk.Combobox(self, textvariable=self.dayVar, state="readonly",
                                        values=[str(day) for day in range(1, 32)], width=12)
        self.dayCombobox.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self, text="Hour:").grid(row=3, column=0, padx=5, pady=5)
        self.hourCombobox = ttk.Combobox(self, textvariable=self.hourVar, state="readonly",
                                         values=[str(hour) for hour in range(24)], width=12)
        self.hourCombobox.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self, text="Minute:").grid(row=4, column=0, padx=5, pady=5)
        self.minuteCombobox = ttk.Combobox(self, textvariable=self.minuteVar, state="readonly",
                                           values=[str(minute) for minute in range(60)], width=12)
        self.minuteCombobox.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self, text="Second:").grid(row=5, column=0, padx=5, pady=5)
        self.secondCombobox = ttk.Combobox(self, textvariable=self.secondVar, state="readonly",
                                           values=[str(second) for second in range(60)], width=12)
        self.secondCombobox.grid(row=5, column=1, padx=5, pady=5)

        # 选择记录类型
        self.recordTypeVar = tk.StringVar()
        self.recordTypeVar.set("签到")
        ttk.Label(self, text="Record Type:").grid(row=6, column=0, padx=5, pady=5)
        self.recordTypeCombobox = ttk.Combobox(self, textvariable=self.recordTypeVar, state="readonly",
                                               values=["签到", "签退"], width=12)
        self.recordTypeCombobox.grid(row=6, column=1, padx=5, pady=5)

        # 创建确认按钮
        self.okButton = ttk.Button(self, text="OK", command=self.ok)
        self.okButton.grid(row=7, column=0, columnspan=2, pady=5)

    def ok(self):

        selectedDatetime = datetime(int(self.yearVar.get()), int(self.monthVar.get()),
                                    int(self.dayVar.get()),
                                    int(self.hourVar.get()), int(self.minuteVar.get()),
                                    int(self.secondVar.get()))
        if selectedDatetime > datetime.now():
            messagebox.showerror("错误", "选择的时间不能晚于当前时间")
            return
        else:
            employeeId = self.parent.idEntry.get()
            if messagebox.askokcancel("确认", f"确定要插入记录吗？\n时间: {selectedDatetime}\n人员编号: {employeeId}"):
                if self.recordTypeVar.get() == "签到":
                    sqlController.InsertAttendanceRecord(employeeId, selectedDatetime, 0)
                else:
                    sqlController.InsertAttendanceRecord(employeeId, selectedDatetime, 1)
                if self.onExit:  # 如果有回调函数
                    self.onExit()
                self.destroy()  # 调用完成后关闭窗口


class DeleteRecordWindow(tk.Toplevel):
    def __init__(self, parent, onExit=None):
        super().__init__(parent)
        self.master = parent
        self.title("删除确认窗口")

        # 添加窗口关闭的回调函数
        def OnExit():
            if onExit:
                onExit()
            self.destroy()

        self.onExit = OnExit
        self.protocol("WM_DELETE_WINDOW", OnExit)   # 设置窗口关闭时的回调函数

        # 创建选择类型标签和ComboBox
        self.labelType = ttk.Label(self, text="选择类型:")
        self.labelType.grid(row=0, column=0, padx=5, pady=5)

        self.typeCombBox = ttk.Combobox(self, values=["记录编号", "人员编号"], state='readonly')
        self.typeCombBox.grid(row=0, column=1, padx=5, pady=5)
        self.typeCombBox.current(0)  # 默认选择第一个选项

        # 创建编号标签和输入框
        self.labelNumber = ttk.Label(self, text="编号:")
        self.labelNumber.grid(row=1, column=0, padx=5, pady=5)

        self.entry = ttk.Entry(self)
        self.entry.grid(row=1, column=1, padx=5, pady=5)

        # 创建查询结果标签的Frame
        self.frame = ttk.Frame(self)
        self.frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        # 创建查询结果标签
        self.resultShowText = tk.Text(self.frame, wrap="word", height=10, width=50)
        self.resultShowText.grid(row=0, column=0)
        # 为查询结果标签添加滚动条
        AddScrollbarToText(self.resultShowText)

        # 创建查询按钮
        self.searchButton = ttk.Button(self, text="查询", command=self.searchNumber)
        self.searchButton.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # 创建删除按钮
        self.deleteButton = ttk.Button(self, text="删除", command=self.deleteEntry, state="disabled")
        self.deleteButton.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def searchNumber(self):
        # 获取选择的类型和编号
        selectedType = self.typeCombBox.get()
        number = self.entry.get()

        resultText = "记录号\t人员号\t记录时间\t\t\t类型\n"
        # 在查询结果标签中显示查询信息
        if selectedType == "记录编号":
            result = sqlController.SelectAttendanceRecordByRecordID(number)
            if result:
                if result.type == 0:
                    resultText += f"{result.recordID}\t{result.employeeID}\t{result.datetime}\t\t\t签到\n"
                else:
                    resultText += f"{result.recordID}\t{result.employeeID}\t{result.datetime}\t\t\t签退\n"
            else:
                resultText += "无记录"
        else:
            result = sqlController.SelectAttendanceRecordByEmployeeID(number)
            if result:
                for record in result:
                    if record.type == 0:
                        resultText += f"{record.recordID}\t{record.employeeID}\t{record.datetime}\t\t\t签到\n"
                    else:
                        resultText += f"{record.recordID}\t{record.employeeID}\t{record.datetime}\t\t\t签退\n"
            else:
                resultText += "无记录"

        self.resultShowText.delete("1.0", "end")
        self.resultShowText.insert(tk.END, resultText)

        # 查询后启用删除按钮
        if result:  # 如果查询结果不为空
            self.deleteButton.config(state="normal")

    def deleteEntry(self):
        # 二次确认对话框
        if messagebox.askokcancel("删除确认", "确定要删除吗？"):
            # 删除数据库中的记录
            selectedType = self.typeCombBox.get()
            number = self.entry.get()
            if selectedType == "记录编号":
                sqlController.DeleteAttendanceRecordByRecordId(number)
            else:
                sqlController.DeleteAttendanceRecordByEmployeeID(number)

            # 删除后关闭自身
            self.onExit()


class TestApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Main App")
        self.geometry("400x200")

        self.selectedDatetime = None  # 用于保存选择的时间
        self.selectedRecordType = None  # 用于保存选择的记录类型

        self.dateTimePickerButton = ttk.Button(self, text="Select Date Time", command=self.openDatetimePicker)
        self.dateTimePickerButton.pack(pady=20)

        # 增加一个标签, 用于显示选择的时间
        self.selectedDatetimeLabel = ttk.Label(self, text="")
        self.selectedDatetimeLabel.pack(pady=20)

        # 增加一个按钮, 用于显示选择的时间
        self.showSelectedDatetimeButton = ttk.Button(self, text="Show Selected Date Time",
                                                     command=self.showSelectedDatetime)
        self.showSelectedDatetimeButton.pack(pady=20)

    def openDatetimePicker(self):
        datetimePicker = InsertRecordWindow(self)
        datetimePicker.grab_set()  # 阻止与其他窗口的交互, 直到该窗口关闭
        self.wait_window(datetimePicker)  # 等待窗口关闭

    def showSelectedDatetime(self):
        if self.selectedDatetime:
            self.selectedDatetimeLabel.config(text=f"{self.selectedDatetime.strftime('%Y-%m-%d %H:%M:%S')}"
                                                   f"\t{self.selectedRecordType}")
        else:
            self.selectedDatetimeLabel.config(text="No Date Time Selected")


def TestScrollBar():
    root = tk.Tk()
    root.geometry("300x200")

    # 创建一个Text组件
    text = tk.Text(root, wrap="word")
    text.grid(row=0, column=0, sticky="nsew")

    # 添加内容
    for i in range(50):
        text.insert("end", f"Line {i}\n")

    # 调用函数为Text添加滚动条
    AddScrollbarToText(text)

    root.mainloop()


def TestDateTimePicker():
    app = TestApp()
    app.mainloop()


def TestDeleteRecordWindow():
    root = tk.Tk()
    app = DeleteRecordWindow(root)
    app.mainloop()


if __name__ == "__main__":
    # TestScrollBar()
    # TestDateTimePicker()
    TestDeleteRecordWindow()
