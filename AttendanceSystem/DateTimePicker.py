import tkinter as tk
from datetime import datetime
from tkinter import ttk


class DateTimePicker(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("选择时间")
        self.geometry("220x250")

        # 最后要返回的时间以及错误提示信息
        self.parent = parent
        self.errorLabel = None

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

        # 创建确认按钮
        self.okButton = ttk.Button(self, text="OK", command=self.ok)
        self.okButton.grid(row=6, column=0, columnspan=2, pady=5)

    def ok(self):
        try:
            # 将选择的时间赋值给父窗口的selected_datetime
            self.parent.selectedDatetime = datetime(int(self.yearVar.get()), int(self.monthVar.get()),
                                                    int(self.dayVar.get()),
                                                    int(self.hourVar.get()), int(self.minuteVar.get()),
                                                    int(self.secondVar.get()))
            self.destroy()
        except ValueError:
            # 如果输入的时间不合法, 则在下方显示提示信息
            self.errorLabel = ttk.Label(self, text="Invalid Date Time", foreground="red")


class TestApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Main App")
        self.geometry("400x200")

        self.selectedDatetime = None

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
        datetimePicker = DateTimePicker(self)
        datetimePicker.grab_set()  # 阻止与其他窗口的交互, 直到该窗口关闭
        self.wait_window(datetimePicker)  # 等待窗口关闭

    def showSelectedDatetime(self):
        if self.selectedDatetime:
            self.selectedDatetimeLabel.config(text=self.selectedDatetime.strftime('%Y-%m-%d %H:%M:%S'))
        else:
            self.selectedDatetimeLabel.config(text="No Date Time Selected")


if __name__ == "__main__":
    app = TestApp()
    app.configure(background='black')
    app.mainloop()
