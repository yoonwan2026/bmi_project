
from modules.health_gui import HealthManagerGUI
import tkinter as tk


def main():
    root = tk.Tk()
    app = HealthManagerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
