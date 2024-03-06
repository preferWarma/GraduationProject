import tkinter as tk
from AttendanceSystem import GUI

if __name__ == '__main__':
    root = tk.Tk()
    app = GUI.AdminGui(root)
    root.geometry("1000x600")
    root.mainloop()
