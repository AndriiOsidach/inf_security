import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import styles
from lab2 import utils2
from lab2.md5 import MD5


class UI:
    def __init__(self, master):
        self.master = master
        self.master.title("MD5 Hasher")
        self.master.geometry("900x700")
        self.master.configure(bg=styles.COLORS['bg_main'])
        self.style = styles.apply_styles(self.master)
        self.md5 = MD5()
        self.create_widgets()
        self.is_operation_running = False
        self.cancel_operation = False

    def create_widgets(self):
        main_container = ttk.Frame(self.master, padding="20 20 20 20")
        main_container.pack(expand=True, fill=tk.BOTH)

        ttk.Label(main_container, text="MD5 Hasher", style="Header.TLabel").pack(pady=(0, 20))

        input_frame = ttk.Frame(main_container)
        input_frame.pack(fill=tk.X, pady=10)
        ttk.Label(input_frame, text="Enter text to hash:").pack(side=tk.LEFT, padx=(0, 10))
        self.input_field = ttk.Entry(input_frame, width=50)
        self.input_field.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.hash_button = ttk.Button(input_frame, text="Hash", command=self.hash_input)
        self.hash_button.pack(side=tk.LEFT, padx=(10, 0))

        output_frame = ttk.LabelFrame(main_container, text="MD5 Hash Result", padding="10 10 10 10")
        output_frame.pack(expand=True, fill=tk.BOTH, pady=20)
        self.output_text = tk.Text(output_frame, height=5, wrap=tk.WORD, font=("Consolas", 10),
                                   bg=styles.COLORS['bg_accent'], fg=styles.COLORS['fg_main'])
        self.output_text.pack(expand=True, fill=tk.BOTH)

        progress_frame = ttk.Frame(main_container)
        progress_frame.pack(fill=tk.X, pady=10)
        self.progress_identifier = ttk.Label(progress_frame, text="")
        self.progress_identifier.pack(anchor=tk.W, pady=(0, 5))
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100,
                                            style="Neon.Horizontal.TProgressbar")
        self.progress_bar.pack(fill=tk.X)

        self.style.configure("Neon.Horizontal.TProgressbar",
                             troughcolor=styles.COLORS['bg_main'],
                             background="#39FF14",
                             darkcolor="#39FF14",
                             lightcolor="#39FF14")

        button_frame = ttk.Frame(main_container)
        button_frame.pack(pady=20)

        self.run_tests_button = ttk.Button(button_frame, text="Run Tests", command=self.run_tests)
        self.run_tests_button.pack(side=tk.LEFT, padx=5)
        self.save_hash_button = ttk.Button(button_frame, text="Save Hash", command=self.save_hash)
        self.save_hash_button.pack(side=tk.LEFT, padx=5)
        self.hash_file_button = ttk.Button(button_frame, text="Hash File", command=self.hash_file)
        self.hash_file_button.pack(side=tk.LEFT, padx=5)
        self.check_integrity_button = ttk.Button(button_frame, text="Check File Integrity",
                                                 command=self.check_file_integrity)
        self.check_integrity_button.pack(side=tk.LEFT, padx=5)
        self.cancel_button = ttk.Button(button_frame, text="Cancel", command=self.cancel_operation_handler,
                                        state=tk.DISABLED)
        self.cancel_button.pack(side=tk.LEFT, padx=5)
        self.close_button = ttk.Button(button_frame, text="Close", command=self.master.destroy)
        self.close_button.pack(side=tk.LEFT, padx=5)

        self.ui_elements = [
            self.input_field, self.hash_button, self.run_tests_button, self.save_hash_button,
            self.hash_file_button, self.check_integrity_button, self.close_button
        ]

    def set_ui_state(self, state):
        for element in self.ui_elements:
            element.config(state=state)
        self.output_text.config(state=state)
        self.is_operation_running = (state == 'disabled')
        self.cancel_button.config(state='normal' if state == 'disabled' else 'disabled')

    def set_progress_identifier(self, text):
        self.progress_identifier.config(text=text)

    def clear_fields(self):
        self.input_field.delete(0, tk.END)
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state='disabled')

    def hash_input(self):
        input_text = self.input_field.get().strip()
        if input_text:
            self.clear_fields()
            self.set_ui_state('disabled')
            self.progress_var.set(0)
            self.set_progress_identifier("Hashing input text...")
            self.cancel_operation = False
            threading.Thread(target=self._hash_input_thread, args=(input_text,), daemon=True).start()
        else:
            messagebox.showwarning("Warning", "Please enter text to hash.")

    def _hash_input_thread(self, input_text):
        hash_result = self.md5.hash(input_text)
        if not self.cancel_operation:
            self.master.after(0, self._update_hash_result, hash_result)

    def run_tests(self):
        self.clear_fields()
        self.set_ui_state('disabled')
        self.progress_var.set(0)
        self.set_progress_identifier("Running MD5 tests...")
        self.cancel_operation = False
        threading.Thread(target=self._run_tests_thread, daemon=True).start()

    def _run_tests_thread(self):
        results = utils2.run_md5_tests()
        if not self.cancel_operation:
            self.master.after(0, self._update_test_results, results)

    def _update_test_results(self, results):
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, results)
        self.output_text.config(state='disabled')
        self.progress_var.set(100)
        self.set_progress_identifier("MD5 tests completed")
        self.set_ui_state('normal')

    def save_hash(self):
        hash_result = self.output_text.get(1.0, tk.END).strip()
        if hash_result:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt")
            if file_path:
                utils2.save_to_file(file_path, hash_result)
                messagebox.showinfo("Success", f"Hash saved to {file_path}")
        else:
            messagebox.showwarning("Warning", "No hash result to save.")

    def update_progress(self, value):
        self.progress_var.set(value)
        self.master.update_idletasks()

    def hash_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.clear_fields()
            self.set_ui_state('disabled')
            self.progress_var.set(0)
            self.set_progress_identifier(f"Hashing file: {file_path}")
            self.cancel_operation = False
            threading.Thread(target=self._hash_file_thread, args=(file_path,), daemon=True).start()

    def _hash_file_thread(self, file_path):
        def progress_callback(value):
            if self.cancel_operation:
                return False
            self.master.after(0, self.update_progress, value)
            return True

        hash_result = self.md5.hash_file(file_path, progress_callback=progress_callback)
        if not self.cancel_operation:
            self.master.after(0, self._update_hash_result, hash_result)

    def _update_hash_result(self, hash_result):
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, hash_result)
        self.output_text.config(state='disabled')
        self.progress_var.set(100)
        self.set_progress_identifier("Hashing completed")
        self.set_ui_state('normal')

    def check_file_integrity(self):
        file_path = filedialog.askopenfilename(title="Select file to check")
        if not file_path:
            return

        hash_file_path = filedialog.askopenfilename(title="Select MD5 hash file", filetypes=[("Text files", "*.txt")])
        if not hash_file_path:
            return

        self.clear_fields()
        self.set_ui_state('disabled')
        self.progress_var.set(0)
        self.set_progress_identifier(f"Checking integrity of file: {file_path}")
        self.cancel_operation = False
        threading.Thread(target=self._check_integrity_thread, args=(file_path, hash_file_path), daemon=True).start()

    def _check_integrity_thread(self, file_path, hash_file_path):
        def progress_callback(value):
            if self.cancel_operation:
                return False
            self.master.after(0, self.update_progress, value)
            return True

        is_valid = utils2.check_file_integrity(file_path, hash_file_path, progress_callback=progress_callback)
        if not self.cancel_operation:
            self.master.after(0, self._show_integrity_result, is_valid)

    def _show_integrity_result(self, is_valid):
        if is_valid:
            messagebox.showinfo("File Integrity", "File integrity check passed.")
        else:
            messagebox.showerror("File Integrity", "File integrity check failed.")
        self.progress_var.set(100)
        self.set_progress_identifier("Integrity check completed")
        self.set_ui_state('normal')

    def cancel_operation_handler(self):
        self.cancel_operation = True
        self.set_progress_identifier("Operation cancelled")
        self.set_ui_state('normal')
        self.progress_var.set(0)
        self.clear_fields()


if __name__ == "__main__":
    root = tk.Tk()
    md5_hasher = UI(root)
    root.mainloop()
