import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import styles
from lab1 import lcg, utils1


class UI:
    def __init__(self, master):
        self.master = master
        self.master.title("Random Number Generator")
        self.master.geometry("900x700")
        self.master.configure(bg=styles.COLORS['bg_main'])
        self.style = styles.apply_styles(self.master)
        self.lcg_generator = lcg.LCG()
        self.create_widgets()

    def create_widgets(self):
        main_container = ttk.Frame(self.master, padding="20 20 20 20")
        main_container.pack(expand=True, fill=tk.BOTH)

        ttk.Label(main_container, text="Random Number Generation", style="Header.TLabel").pack(pady=(0, 20))

        input_frame = ttk.Frame(main_container)
        input_frame.pack(fill=tk.X, pady=10)

        ttk.Label(input_frame, text="Enter length of random sequence:").pack(side=tk.LEFT, padx=(0, 10))
        self.input_field = ttk.Entry(input_frame, width=15)
        self.input_field.pack(side=tk.LEFT)
        ttk.Button(input_frame, text="Generate", command=self.generate_sequences).pack(side=tk.LEFT, padx=(10, 0))

        results_frame = ttk.Frame(main_container)
        results_frame.pack(expand=True, fill=tk.BOTH, pady=20)
        results_frame.columnconfigure(0, weight=1)
        results_frame.columnconfigure(1, weight=1)

        lcg_frame = ttk.LabelFrame(results_frame, text="LCG Sequence", padding="10 10 10 10")
        lcg_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        system_frame = ttk.LabelFrame(results_frame, text="System Sequence", padding="10 10 10 10")
        system_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        self.lcg_result = tk.Text(lcg_frame, height=10, width=40, wrap=tk.WORD, font=("Consolas", 10),
                                  bg=styles.COLORS['bg_accent'], fg=styles.COLORS['fg_main'],
                                  insertbackground=styles.COLORS['fg_main'])
        self.lcg_result.pack(expand=True, fill=tk.BOTH)

        self.system_result = tk.Text(system_frame, height=10, width=40, wrap=tk.WORD, font=("Consolas", 10),
                                     bg=styles.COLORS['bg_accent'], fg=styles.COLORS['fg_main'],
                                     insertbackground=styles.COLORS['fg_main'])
        self.system_result.pack(expand=True, fill=tk.BOTH)

        self.lcg_result_label = ttk.Label(lcg_frame, text="", justify=tk.LEFT)
        self.lcg_result_label.pack(pady=(10, 0), anchor="w")

        self.system_result_label = ttk.Label(system_frame, text="", justify=tk.LEFT)
        self.system_result_label.pack(pady=(10, 0), anchor="w")

        button_frame = ttk.Frame(main_container)
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="Save LCG Sequence", command=lambda: self.save_sequence("lcg")).pack(side=tk.LEFT,
                                                                                                           padx=5)
        ttk.Button(button_frame, text="Save System Sequence", command=lambda: self.save_sequence("system")).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Close", command=self.master.destroy).pack(side=tk.LEFT, padx=5)

    def generate_sequences(self):
        input_value = self.input_field.get().strip()

        try:
            n = int(input_value)
            if n <= 0:
                messagebox.showerror("Error", "Input must be a positive integer.")
                return
        except ValueError:
            messagebox.showerror("Error", "You should enter a number, not text.")
            return

        lcg_seq = self.lcg_generator.generate_sequence(n)
        system_seq = utils1.generate_system_sequence(n)

        self.lcg_result.delete(1.0, tk.END)
        self.system_result.delete(1.0, tk.END)

        if n < 1000:
            self.lcg_result.insert(tk.END, ", ".join(map(str, lcg_seq)))
            self.system_result.insert(tk.END, ", ".join(map(str, system_seq)))
        else:
            self.lcg_result.insert(tk.END, "Too many numbers to display")
            self.system_result.insert(tk.END, "Too many numbers to display")

        lcg_period = utils1.calculate_period(lcg_seq)
        system_period = utils1.calculate_period(system_seq)
        lcg_pi_estimate = utils1.estimate_pi(lcg_seq)
        system_pi_estimate = utils1.estimate_pi(system_seq)

        lcg_pi_text = f"{lcg_pi_estimate:.6f}" if isinstance(lcg_pi_estimate, float) else str(lcg_pi_estimate)
        system_pi_text = f"{system_pi_estimate:.6f}" if isinstance(system_pi_estimate, float) else str(
            system_pi_estimate)

        self.lcg_result_label.config(text=f"Period: {lcg_period}\nπ Estimate: {lcg_pi_text}")
        self.system_result_label.config(text=f"Period: {system_period}\nπ Estimate: {system_pi_text}")

    def save_sequence(self, seq_type):
        filename = filedialog.asksaveasfilename(defaultextension=".txt")
        if filename:
            with open(filename, "w") as f:
                if seq_type == "lcg":
                    f.write(self.lcg_result.get(1.0, tk.END))
                else:
                    f.write(self.system_result.get(1.0, tk.END))


if __name__ == "__main__":
    root = tk.Tk()
    lab1 = UI(root)
    root.mainloop()
