import importlib
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

import styles


class Launcher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Launcher")
        self.geometry("800x600")
        self.configure(bg=styles.COLORS['bg_main'])
        self.style = styles.apply_styles(self)
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="20 20 20 20")
        main_frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(main_frame, text="Information Security Technologies", style="Header.TLabel").pack(pady=20)

        self.content_frame = ttk.Frame(main_frame)
        self.content_frame.pack(expand=True, fill=tk.BOTH)

        self.show_home()

    def show_home(self):
        self.clear_content_frame()

        ttk.Label(self.content_frame, text="Select a lab to begin:", style="Launcher.TLabel").pack(pady=10)

        button_frame = ttk.Frame(self.content_frame)
        button_frame.pack(pady=10)

        for i in range(1, 6):
            ttk.Button(button_frame, text=f"Lab {i}", command=lambda x=i: self.launch_lab(x),
                       style="Launcher.TButton").pack(pady=5)

        ttk.Button(self.content_frame, text="Exit", command=self.quit, style="Launcher.TButton").pack(pady=20)

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def launch_lab(self, lab_number):
        lab_dir = f"lab{lab_number}"

        if not os.path.isdir(lab_dir):
            messagebox.showerror("Error", f"Lab {lab_number} directory not found.")
            return

        sys.path.insert(0, lab_dir)

        try:
            lab_module = importlib.import_module(f"ui{lab_number}")
            lab_class = getattr(lab_module, f"UI")

            lab_window = tk.Toplevel(self)
            lab_window.title(f"Lab {lab_number}")
            if lab_number == 5:
                lab_window.geometry("600x170")  # Adjusted to match Lab1's geometry
            lab_window.configure(bg=styles.COLORS['bg_main'])
            styles.apply_styles(lab_window)

            lab_class(lab_window)
            lab_window.mainloop()
        except ImportError as e:
            messagebox.showerror("Error", f"Failed to import Lab {lab_number}: {str(e)}")
        except AttributeError as e:
            messagebox.showerror("Error", f"Lab {lab_number} is not properly implemented: {str(e)}")
        finally:
            sys.path.pop(0)  # Remove the lab directory from sys.path


if __name__ == "__main__":
    app = Launcher()
    app.mainloop()
