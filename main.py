import tkinter as tk
from AttendanceSystem.MainGUI import MainGUI

if __name__ == '__main__':
    root = tk.Tk()
    app = MainGUI(root)
    root.geometry("1000x600")
    root.mainloop()
