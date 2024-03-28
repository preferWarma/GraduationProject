import tkinter as tk
from AttendanceSystem import MainGUI

if __name__ == '__main__':
    root = tk.Tk()
    app = MainGUI.MainGUI(root)
    root.geometry("1000x600")
    root.mainloop()
