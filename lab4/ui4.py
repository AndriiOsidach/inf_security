import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from lab4.rsa import RSA


class UI:
    def __init__(self, root):
        self.root = root
        self.root.title("RSA File Encryption")
        self.root.geometry("900x600")
        self.root.configure(bg='#1E1E1E')  # Dark background

        self.setup_styles()
        self.rsa = RSA()

        # Main container with padding
        main_container = ttk.Frame(root, padding="20")
        main_container.pack(fill=tk.BOTH, expand=True)

        # Create notebook with custom styling
        self.notebook = ttk.Notebook(main_container)
        self.keys_tab = ttk.Frame(self.notebook, padding="20")
        self.encrypt_tab = ttk.Frame(self.notebook, padding="20")
        self.decrypt_tab = ttk.Frame(self.notebook, padding="20")
        self.performance_tab = ttk.Frame(self.notebook, padding="20")

        # Add tabs with icons
        self.notebook.add(self.keys_tab, text=" 🔑 Keys ")
        self.notebook.add(self.encrypt_tab, text=" 🔒 Encrypt ")
        self.notebook.add(self.decrypt_tab, text=" 🔓 Decrypt ")
        self.notebook.add(self.performance_tab, text=" 📊 Performance ")

        self.notebook.pack(expand=True, fill='both')

        self._setup_keys_tab()
        self._setup_encrypt_tab()
        self._setup_decrypt_tab()
        self._setup_performance_tab()

        # Status bar at the bottom
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(root, textvariable=self.status_var,
                                  style='Status.TLabel')
        self.status_bar.pack(fill=tk.X, padx=5, pady=5)

    def setup_styles(self):
        """Configure custom styles for the application"""
        style = ttk.Style()
        style.theme_use('clam')  # Use clam theme as base

        # Define colors
        colors = {
            'bg_main': "#1E1E1E",
            'fg_main': "#FFFFFF",
            'bg_accent': "#404040",
            'bg_button': "#333333",
            'bg_button_active': "#4A4A4A",
            'neon_green': "#39FF14",
            'gray': "#808080"
        }

        # Configure general styles
        style.configure('.',
                      background=colors['bg_main'],
                      foreground=colors['fg_main'],
                      font=('Arial', 12))

        # Notebook style
        style.configure('TNotebook',
                      background=colors['bg_main'],
                      borderwidth=0)
        style.configure('TNotebook.Tab',
                      background=colors['bg_accent'],
                      foreground=colors['fg_main'],
                      padding=[10, 5],
                      font=('Arial', 12))
        style.map('TNotebook.Tab',
                 background=[('selected', colors['bg_button_active'])],
                 foreground=[('selected', colors['neon_green'])])

        # Frame styles
        style.configure('TFrame',
                      background=colors['bg_main'])
        style.configure('TLabelframe',
                      background=colors['bg_main'],
                      foreground=colors['fg_main'])
        style.configure('TLabelframe.Label',
                      background=colors['bg_main'],
                      foreground=colors['fg_main'],
                      font=('Arial', 12))

        # Button styles
        style.configure('TButton',
                      background=colors['bg_button'],
                      foreground=colors['fg_main'],
                      padding=8,
                      font=('Arial', 12))
        style.map('TButton',
                 background=[('active', colors['bg_button_active'])])

        # Label styles
        style.configure('TLabel',
                      background=colors['bg_main'],
                      foreground=colors['fg_main'],
                      font=('Arial', 12))
        style.configure('Header.TLabel',
                      font=('Arial', 24, 'bold'))
        style.configure('Status.TLabel',
                      background=colors['bg_accent'],
                      padding=5)

        # Entry styles
        style.configure('TEntry',
                      fieldbackground=colors['bg_accent'],
                      foreground=colors['fg_main'],
                      padding=5)

        # Combobox styles
        style.configure('TCombobox',
                      fieldbackground=colors['bg_accent'],
                      background=colors['bg_accent'],
                      foreground=colors['fg_main'],
                      selectbackground=colors['bg_button_active'],
                      selectforeground=colors['neon_green'])

        return style

    def _setup_keys_tab(self):
        """Setup the keys management tab with improved layout"""
        # Header
        header = ttk.Label(self.keys_tab,
                         text="RSA Key Management",
                         style='Header.TLabel')
        header.pack(fill='x', pady=(0, 20))

        # Key Generation Section
        gen_frame = ttk.LabelFrame(self.keys_tab,
                                text="Generate New Keys",
                                padding=15)
        gen_frame.pack(fill='x', padx=5, pady=5)

        key_size_frame = ttk.Frame(gen_frame)
        key_size_frame.pack(fill='x', pady=5)

        ttk.Label(key_size_frame, text="Key Size:").pack(side=tk.LEFT, padx=5)
        key_sizes = ['2048', '3072', '4096']
        self.key_size_var = tk.StringVar(value='2048')
        key_size_combo = ttk.Combobox(key_size_frame,
                                    textvariable=self.key_size_var,
                                    values=key_sizes,
                                    width=10,
                                    state='readonly')
        key_size_combo.pack(side=tk.LEFT, padx=5)

        ttk.Button(gen_frame,
                 text="Generate Keys",
                 command=self._generate_keys).pack(pady=10)

        # Key Storage Section
        storage_frame = ttk.LabelFrame(self.keys_tab,
                                    text="Key Storage",
                                    padding=15)
        storage_frame.pack(fill='x', padx=5, pady=15)

        btn_frame = ttk.Frame(storage_frame)
        btn_frame.pack(fill='x', pady=5)

        ttk.Button(btn_frame,
                 text="Save Keys",
                 command=self._save_keys).pack(side=tk.LEFT, padx=5)

        ttk.Button(btn_frame,
                 text="Load Keys",
                 command=self._load_keys).pack(side=tk.LEFT, padx=5)

    def _setup_encrypt_tab(self):
        """Setup the encryption tab with improved layout"""
        # Header
        header = ttk.Label(self.encrypt_tab,
                         text="File Encryption",
                         style='Header.TLabel')
        header.pack(fill='x', pady=(0, 20))

        # File selection frame
        file_frame = ttk.LabelFrame(self.encrypt_tab,
                                 text="Select File",
                                 padding=15)
        file_frame.pack(fill='x', padx=5, pady=5)

        self.encrypt_file_var = tk.StringVar()
        file_entry = ttk.Entry(file_frame,
                            textvariable=self.encrypt_file_var,
                            width=50)
        file_entry.pack(fill='x', pady=5)

        ttk.Button(file_frame,
                 text="Browse",
                 command=lambda: self._browse_file(self.encrypt_file_var)).pack()

        # Action buttons
        ttk.Button(self.encrypt_tab,
                 text="Encrypt File",
                 command=self._encrypt_file).pack(pady=20)

    def _setup_decrypt_tab(self):
        """Setup the decryption tab with improved layout"""
        # Header
        header = ttk.Label(self.decrypt_tab,
                         text="File Decryption",
                         style='Header.TLabel')
        header.pack(fill='x', pady=(0, 20))

        # File selection frame
        file_frame = ttk.LabelFrame(self.decrypt_tab,
                                 text="Select File",
                                 padding=15)
        file_frame.pack(fill='x', padx=5, pady=5)

        self.decrypt_file_var = tk.StringVar()
        file_entry = ttk.Entry(file_frame,
                            textvariable=self.decrypt_file_var,
                            width=50)
        file_entry.pack(fill='x', pady=5)

        ttk.Button(file_frame,
                 text="Browse",
                 command=lambda: self._browse_file(self.decrypt_file_var)).pack()

        # Action buttons
        ttk.Button(self.decrypt_tab,
                 text="Decrypt File",
                 command=self._decrypt_file).pack(pady=20)

    def _setup_performance_tab(self):
        """Setup the performance testing tab"""
        # Header
        header = ttk.Label(self.performance_tab,
                         text="Performance Testing",
                         style='Header.TLabel')
        header.pack(fill='x', pady=(0, 20))

        # Test configuration frame
        test_frame = ttk.LabelFrame(self.performance_tab,
                                 text="Test Configuration",
                                 padding=15)
        test_frame.pack(fill='x', padx=5, pady=5)

        # File size selection
        size_frame = ttk.Frame(test_frame)
        size_frame.pack(fill='x', pady=5)

        ttk.Label(size_frame, text="Test file size (MB):").pack(side=tk.LEFT, padx=5)
        self.size_var = tk.StringVar(value="1")
        size_entry = ttk.Entry(size_frame,
                            textvariable=self.size_var,
                            width=10)
        size_entry.pack(side=tk.LEFT, padx=5)

        # Run test button
        ttk.Button(test_frame,
                 text="Run Performance Test",
                 command=self._run_performance_test).pack(pady=10)

        # Results display
        results_frame = ttk.LabelFrame(self.performance_tab,
                                    text="Test Results",
                                    padding=15)
        results_frame.pack(fill='both', expand=True, padx=5, pady=5)

        self.result_text = tk.Text(results_frame,
                                height=10,
                                width=40,
                                font=('Consolas', 15    ),
                                bg='#404040',
                                fg='#FFFFFF',
                                insertbackground='#FFFFFF')
        self.result_text.pack(fill='both', expand=True)

    # Rest of the existing methods remain the same
    def _browse_file(self, var):
        filename = filedialog.askopenfilename()
        if filename:
            var.set(filename)

    def _generate_keys(self):
        try:
            key_size = int(self.key_size_var.get())
            self.rsa.generate_keys(key_size=key_size)
            self.status_var.set("Keys generated successfully!")
            messagebox.showinfo("Success", "Keys generated successfully!")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to generate keys: {str(e)}")

    def _save_keys(self):
        try:
            private_path = filedialog.asksaveasfilename(
                defaultextension=".pem",
                filetypes=[("PEM files", "*.pem")],
                title="Save Private Key"
            )
            if not private_path:
                return

            public_path = filedialog.asksaveasfilename(
                defaultextension=".pem",
                filetypes=[("PEM files", "*.pem")],
                title="Save Public Key"
            )
            if not public_path:
                return

            self.rsa.save_keys(private_path, public_path)
            self.status_var.set("Keys saved successfully!")
            messagebox.showinfo("Success", "Keys saved successfully!")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to save keys: {str(e)}")

    def _load_keys(self):
        try:
            private_path = filedialog.askopenfilename(
                filetypes=[("PEM files", "*.pem")],
                title="Select Private Key"
            )
            if not private_path:
                return

            public_path = filedialog.askopenfilename(
                filetypes=[("PEM files", "*.pem")],
                title="Select Public Key"
            )
            if not public_path:
                return

            self.rsa.load_keys(private_path, public_path)
            self.status_var.set("Keys loaded successfully!")
            messagebox.showinfo("Success", "Keys loaded successfully!")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to load keys: {str(e)}")

    def _encrypt_file(self):
        try:
            input_path = self.encrypt_file_var.get()
            if not input_path:
                messagebox.showwarning("Warning", "Please select a file to encrypt")
                return

            output_path = filedialog.asksaveasfilename(
                defaultextension=".enc",
                filetypes=[("Encrypted files", "*.enc")],
                title="Save Encrypted File"
            )
            if not output_path:
                return

            self.rsa.encrypt_file(input_path, output_path)
            self.status_var.set("File encrypted successfully!")
            messagebox.showinfo("Success", "File encrypted successfully!")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to encrypt file: {str(e)}")

    def _decrypt_file(self):
        try:
            input_path = self.decrypt_file_var.get()
            if not input_path:
                messagebox.showwarning("Warning", "Please select a file to decrypt")
                return

            output_path = filedialog.asksaveasfilename(
                title="Save Decrypted File"
            )
            if not output_path:
                return

            self.rsa.decrypt_file(input_path, output_path)
            self.status_var.set("File decrypted successfully!")
            messagebox.showinfo("Success", "File decrypted successfully!")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to decrypt file: {str(e)}")

    def _run_performance_test(self):
        """Run performance tests"""
        try:
            file_size = int(self.size_var.get())
            rsa_enc_time, rsa_dec_time, rc5_enc_time, rc5_dec_time = self.rsa.measure_performance(file_size)

            results = (
                f"File size: {file_size} MB\n"
                f"---------------------\n"
                f"RSA\n"
                f"Encryption speed: {(file_size / rsa_enc_time):.2f} MB/s\n"
                f"Decryption speed: {(file_size / rsa_dec_time):.2f} MB/s\n"
                f"---------------------\n"
                f"RC5\n"
                f"Encryption speed: {(file_size / rc5_enc_time):.2f} MB/s\n"
                f"Decryption speed: {(file_size / rc5_dec_time):.2f} MB/s\n"
            )

            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, results)
            self.status_var.set("Performance test completed successfully!")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to run performance test: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = UI(root)
    root.mainloop()