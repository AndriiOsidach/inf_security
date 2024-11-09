from tkinter import ttk

COLORS = {
    'bg_main': "#1E1E1E",
    'fg_main': "#FFFFFF",
    'bg_accent': "#404040",
    'bg_button': "#333333",
    'bg_button_active': "#4A4A4A",
    'neon_green': "#39FF14",
    'gray': "#808080",
}


def apply_styles(root):
    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure("TFrame", background=COLORS['bg_main'])
    style.configure("TButton",
                    padding=6,
                    relief="flat",
                    background=COLORS['bg_button'],
                    foreground=COLORS['fg_main'])
    style.map("TButton",
              background=[('active', COLORS['bg_button_active'])])
    style.configure("TLabel",
                    background=COLORS['bg_main'],
                    foreground=COLORS['fg_main'],
                    font=("Arial", 14))
    style.configure("TEntry",
                    fieldbackground=COLORS['bg_accent'],
                    foreground=COLORS['fg_main'],
                    insertcolor=COLORS['fg_main'],
                    font=("Arial", 12))
    style.configure("Header.TLabel",
                    font=("Arial", 28, "bold"),
                    foreground=COLORS['fg_main'])
    style.configure("TLabelframe",
                    background=COLORS['bg_main'],
                    foreground=COLORS['fg_main'])
    style.configure("TLabelframe.Label",
                    background=COLORS['bg_main'],
                    foreground=COLORS['fg_main'])

    style.configure("Launcher.TButton",
                    padding=10,
                    width=15,
                    font=("Arial", 14))
    style.configure("Launcher.TLabel",
                    font=("Arial", 18),
                    background=COLORS['bg_main'],
                    foreground=COLORS['fg_main'])

    # Neon green progress bar
    style.configure("Neon.Horizontal.TProgressbar",
                    troughcolor=COLORS['bg_accent'],
                    background=COLORS['neon_green'],
                    lightcolor=COLORS['neon_green'],
                    darkcolor=COLORS['neon_green'],
                    bordercolor=COLORS['bg_accent'])

    # Gray checkbox
    style.configure("Gray.TCheckbutton",
                    background=COLORS['bg_main'],
                    foreground=COLORS['gray'],
                    font=("Arial", 12))
    style.map("Gray.TCheckbutton",
              background=[('active', COLORS['bg_main'])])

    # New styles for larger text
    style.configure("Large.TLabel",
                    font=("Arial", 14),
                    background=COLORS['bg_main'],
                    foreground=COLORS['fg_main'])
    style.configure("Large.TButton",
                    font=("Arial", 14),
                    padding=8)

    return style
