import database
from ui import App
import tkinter as tk

if __name__ == "__main__":
    database.init_db()
    root = tk.Tk()
    app = App(root)
    root.mainloop()
