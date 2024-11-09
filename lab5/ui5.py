import os
from tkinter import Tk, Frame, Text, Button, Label, filedialog, messagebox
from lab5.dss import DigitalSignatureLogic


class UI:
    def __init__(self, master):
        self.master = master
        master.title("Digital Signature Application")

        self.logic = DigitalSignatureLogic()
        self.private_key_loaded = False

        self.frame = Frame(master)
        self.frame.pack()

        self.label = Label(self.frame, text="Enter text to sign:")
        self.label.pack(pady=5)

        self.text_input = Text(self.frame, height=5, width=50)
        self.text_input.pack(pady=5)

        self.button_frame = Frame(self.frame)
        self.button_frame.pack(pady=10)

        self.load_keys_button = Button(self.button_frame, text="Load Keys", command=self.handle_load_keys)
        self.load_keys_button.pack(side="left", padx=5)

        self.generate_keys_button = Button(self.button_frame, text="Generate Keys", command=self.handle_generate_keys)
        self.generate_keys_button.pack(side="left", padx=5)

        self.sign_text_button = Button(self.button_frame, text="Sign Text", command=self.handle_sign_text)
        self.sign_text_button.pack(side="left", padx=5)

        self.sign_file_button = Button(self.button_frame, text="Sign File", command=self.handle_sign_file)
        self.sign_file_button.pack(side="left", padx=5)

        self.verify_signature_button = Button(self.button_frame, text="Verify Signature",
                                              command=self.handle_verify_signature)
        self.verify_signature_button.pack(side="left", padx=5)

    def handle_generate_keys(self):
        messagebox.showinfo("Generate Keys", "Select folder to save the keys.")
        folder = filedialog.askdirectory()
        if not folder:
            messagebox.showerror("Error", "No folder selected.")
            return

        private_key_pem, public_key_pem = self.logic.generate_keys()
        with open(os.path.join(folder, "private_key.pem"), "wb") as f:
            f.write(private_key_pem)
        with open(os.path.join(folder, "public_key.pem"), "wb") as f:
            f.write(public_key_pem)

        messagebox.showinfo("Keys Generated", f"Keys saved to {folder}.")

    def handle_load_keys(self):
        messagebox.showinfo("Load Keys", "Select private key file.")
        private_key_path = filedialog.askopenfilename(filetypes=[("PEM Files", "*.pem")])
        if not private_key_path:
            messagebox.showerror("Error", "No private key selected.")
            return

        messagebox.showinfo("Load Keys", "Select public key file.")
        public_key_path = filedialog.askopenfilename(filetypes=[("PEM Files", "*.pem")])
        if not public_key_path:
            messagebox.showerror("Error", "No public key selected.")
            return

        self.logic.load_keys(private_key_path, public_key_path)
        self.private_key_loaded = True
        messagebox.showinfo("Keys Loaded", "Keys successfully loaded.")

    def handle_sign_text(self):
        if not self.private_key_loaded:
            messagebox.showerror("Error", "Load keys before signing.")
            return

        text = self.text_input.get("1.0", "end-1c").strip()
        if not text:
            messagebox.showerror("Error", "Text field is empty.")
            return

        signature = self.logic.sign_text(text)
        messagebox.showinfo("Signature", f"Signature: {signature.hex()}")

        file_path = filedialog.asksaveasfilename(defaultextension=".sig", filetypes=[("Signature Files", "*.sig")])
        if file_path:
            with open(file_path, "wb") as f:
                f.write(signature)
            messagebox.showinfo("Signature Saved", f"Signature saved to {file_path}.")

    def handle_sign_file(self):
        if not self.private_key_loaded:
            messagebox.showerror("Error", "Load keys before signing.")
            return

        messagebox.showinfo("Sign File", "Select file to sign.")
        file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
        if not file_path:
            messagebox.showerror("Error", "No file selected.")
            return

        with open(file_path, "rb") as f:
            file_content = f.read()
        signature = self.logic.sign_file(file_content)
        messagebox.showinfo("Signature", f"Signature: {signature.hex()}")

        sig_file_path = filedialog.asksaveasfilename(defaultextension=".sig", filetypes=[("Signature Files", "*.sig")])
        if sig_file_path:
            with open(sig_file_path, "wb") as f:
                f.write(signature)
            messagebox.showinfo("Signature Saved", f"Signature saved to {sig_file_path}.")

    def handle_verify_signature(self):
        if not self.private_key_loaded:
            messagebox.showerror("Error", "Load public key before verifying.")
            return

        messagebox.showinfo("Verify Signature", "Select file to verify.")
        file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
        if not file_path:
            messagebox.showerror("Error", "No file selected.")
            return

        with open(file_path, "rb") as f:
            file_content = f.read()

        messagebox.showinfo("Verify Signature", "Select signature file.")
        sig_file_path = filedialog.askopenfilename(filetypes=[("Signature Files", "*.sig")])
        if not sig_file_path:
            messagebox.showerror("Error", "No signature file selected.")
            return

        with open(sig_file_path, "rb") as f:
            signature = f.read()

        try:
            self.logic.verify_signature(self.logic.public_key, file_content, signature)
            messagebox.showinfo("Verification", "Signature is valid.")
        except Exception:
            messagebox.showerror("Verification", "Signature is invalid.")


if __name__ == "__main__":
    root = Tk()
    app = UI(root)
    root.mainloop()
