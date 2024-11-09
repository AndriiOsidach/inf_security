import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import styles
from lab3.rc5 import encrypt_file_rc5, decrypt_file_rc5


class UI:
    def __init__(self, master):
        self.master = master
        self.master.title("RC5 File Encryption/Decryption")
        self.master.geometry("900x600")
        self.master.configure(bg=styles.COLORS['bg_main'])
        self.style = styles.apply_styles(self.master)
        self.create_widgets()

    def create_widgets(self):
        main_container = ttk.Frame(self.master, padding="20 20 20 20")
        main_container.pack(expand=True, fill=tk.BOTH)

        ttk.Label(main_container, text="RC5 File Encryption/Decryption", style="Header.TLabel").pack(pady=(0, 20))

        # Password input
        password_frame = ttk.Frame(main_container)
        password_frame.pack(fill=tk.X, pady=10)
        ttk.Label(password_frame, text="Enter password:", style="Large.TLabel").pack(side=tk.LEFT, padx=(0, 10))
        self.password_entry = ttk.Entry(password_frame, show="*", width=40, font=("Arial", 12))
        self.password_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Show password checkbox (gray)
        self.show_password_var = tk.BooleanVar()
        self.show_password_check = ttk.Checkbutton(password_frame, text="Show password",
                                                   variable=self.show_password_var,
                                                   command=self.toggle_password_visibility,
                                                   style="Gray.TCheckbutton")
        self.show_password_check.pack(side=tk.LEFT, padx=(10, 0))

        # File selection
        file_frame = ttk.Frame(main_container)
        file_frame.pack(fill=tk.X, pady=10)
        self.file_label = ttk.Label(file_frame, text="No file selected", style="Large.TLabel")
        self.file_label.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.select_file_button = ttk.Button(file_frame, text="Select File", command=self.select_file,
                                             style="Large.TButton")
        self.select_file_button.pack(side=tk.RIGHT)

        # Action buttons
        button_frame = ttk.Frame(main_container)
        button_frame.pack(pady=20)
        self.encrypt_button = ttk.Button(button_frame, text="Encrypt", command=self.encrypt_file, style="Large.TButton")
        self.encrypt_button.pack(side=tk.LEFT, padx=5)
        self.decrypt_button = ttk.Button(button_frame, text="Decrypt", command=self.decrypt_file, style="Large.TButton")
        self.decrypt_button.pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Close", command=self.master.destroy, style="Large.TButton").pack(side=tk.LEFT,
                                                                                                        padx=5)

        # Results frame
        results_frame = ttk.Frame(main_container)
        results_frame.pack(expand=True, fill=tk.BOTH, pady=20)
        results_frame.columnconfigure(0, weight=1)

        self.result_text = tk.Text(results_frame, height=10, width=80, wrap=tk.WORD, font=("Consolas", 12),
                                   bg=styles.COLORS['bg_accent'], fg=styles.COLORS['fg_main'],
                                   insertbackground=styles.COLORS['fg_main'])
        self.result_text.grid(row=0, column=0, sticky="nsew")

        # Progress bar (neon green)
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_container, variable=self.progress_var, maximum=100,
                                            style="Neon.Horizontal.TProgressbar")
        self.progress_bar.pack(fill=tk.X, pady=10)

        # Status label
        self.status_label = ttk.Label(main_container, text="", style="Large.TLabel")
        self.status_label.pack(pady=5)

    def select_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_label.config(text=file_path)

    def encrypt_file(self):
        self.process_file(encrypt_file_rc5, "encrypted")

    def decrypt_file(self):
        self.process_file(decrypt_file_rc5, "decrypted")

    def process_file(self, function, operation):
        file_path = self.file_label.cget("text")
        password = self.password_entry.get()

        if file_path == "No file selected":
            messagebox.showerror("Error", "Please select a file first.")
            return

        if not password:
            messagebox.showerror("Error", "Please enter a password.")
            return

        default_extension = ".enc" if operation == "encrypted" else ".dec"
        output_file = filedialog.asksaveasfilename(defaultextension=default_extension)
        if not output_file:
            return

        self.disable_interface()
        self.progress_var.set(0)
        self.status_label.config(text=f"{operation.capitalize()} in progress...")

        thread = threading.Thread(target=self.run_process, args=(function, file_path, password, output_file, operation))
        thread.start()

    def run_process(self, function, file_path, password, output_file, operation):
        try:
            result = function(file_path, password, output_file, self.update_progress)
            self.master.after(0, self.update_result, f"File successfully {operation}:\n{result}")
        except Exception as e:
            self.master.after(0, self.update_result, f"Error during {operation}:\n{str(e)}")
        finally:
            self.master.after(0, self.enable_interface)
            self.master.after(0, self.clear_inputs)
            self.master.after(0, self.status_label.config, {"text": ""})

    def update_result(self, result):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)
        self.result_text.config(state=tk.DISABLED)

    def disable_interface(self):
        self.encrypt_button.config(state=tk.DISABLED)
        self.decrypt_button.config(state=tk.DISABLED)
        self.password_entry.config(state=tk.DISABLED)
        self.result_text.config(state=tk.DISABLED)
        self.select_file_button.config(state=tk.DISABLED)  # Disable the Select File button

    def enable_interface(self):
        self.encrypt_button.config(state=tk.NORMAL)
        self.decrypt_button.config(state=tk.NORMAL)
        self.password_entry.config(state=tk.NORMAL)
        self.result_text.config(state=tk.NORMAL)
        self.select_file_button.config(state=tk.NORMAL)  # Enable the Select File button

    def clear_inputs(self):
        self.password_entry.delete(0, tk.END)
        self.file_label.config(text="No file selected")
        self.progress_var.set(0)

    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def update_progress(self, progress):
        self.progress_var.set(progress)
        self.master.update_idletasks()


if __name__ == "__main__":
    root = tk.Tk()
    app = UI(root)
    root.mainloop()
