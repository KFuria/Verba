import tkinter as tk
from tkinter import ttk

# Dark color palette
PRIMARY = "#7C4DFF"        # Purple accent
PRIMARY_DARK = "#651FFF"   # Darker purple
SECONDARY = "#448AFF"      # Blue accent
BACKGROUND = "#1E1E2E"     # Dark background
SURFACE = "#2D2D3F"        # Slightly lighter surface
CARD = "#363649"           # Card background
ON_PRIMARY = "#FFFFFF"     # White text on primary
ON_SURFACE = "#E4E4E7"     # Light text on surface
TEXT_SECONDARY = "#A1A1AA" # Muted text
TEXT_MUTED = "#71717A"     # Even more muted
BORDER = "#3F3F5A"         # Subtle borders

# Font family
FONT_FAMILY = "Consolas"


def setup_styles(app) -> None:
    style = ttk.Style(app)
    style.theme_use("clam")
    style.configure(".", background=BACKGROUND, foreground=ON_SURFACE)
    
    style.configure("TNotebook", background=BACKGROUND, borderwidth=0)
    style.configure("TNotebook.Tab", background=SURFACE, foreground=TEXT_SECONDARY, padding=(8, 4), font=(FONT_FAMILY, 8))
    style.map("TNotebook.Tab", background=[("selected", PRIMARY)], foreground=[("selected", ON_PRIMARY)])

    style.configure("Card.TFrame", background=SURFACE)
    style.configure("Header.TLabel", background=SURFACE, foreground=PRIMARY, font=(FONT_FAMILY, 14, "bold"))
    style.configure("Meta.TLabel", background=SURFACE, foreground=TEXT_SECONDARY, font=(FONT_FAMILY, 8))
    style.configure("Body.TLabel", background=SURFACE, foreground=ON_SURFACE, font=(FONT_FAMILY, 9))
    style.configure("Bold.TLabel", background=SURFACE, foreground=ON_SURFACE, font=(FONT_FAMILY, 9, "bold"))
    style.configure("Italic.TLabel", background=SURFACE, foreground=TEXT_MUTED, font=(FONT_FAMILY, 8, "italic"))
    style.configure("Status.TLabel", background=SURFACE, foreground=TEXT_MUTED, font=(FONT_FAMILY, 7))
    style.configure("Primary.TButton", background=PRIMARY, foreground=ON_PRIMARY, font=(FONT_FAMILY, 8, "bold"), padding=(8, 4))
    style.map("Primary.TButton", background=[("active", PRIMARY_DARK)])
    style.configure("Secondary.TButton", background=CARD, foreground=ON_SURFACE, font=(FONT_FAMILY, 8), padding=(8, 4))
    style.map("Secondary.TButton", background=[("active", BORDER)])
    style.configure("Flashcard.TLabel", background=SURFACE, foreground=PRIMARY, font=(FONT_FAMILY, 12, "bold"))
    style.configure("FlashcardBody.TLabel", background=SURFACE, foreground=ON_SURFACE, font=(FONT_FAMILY, 9))
    style.configure("TScrollbar", background=SURFACE, troughcolor=BACKGROUND, bordercolor=SURFACE, arrowcolor=CARD, arrowsize=8)
    style.map("TScrollbar", 
              background=[('disabled', SURFACE)], 
              troughcolor=[('disabled', BACKGROUND)], 
              bordercolor=[('disabled', SURFACE)])
    style.configure("Icon.TButton", background=SURFACE, foreground=PRIMARY, font=("Segoe UI Symbol", 12), padding=(2, 0), borderwidth=0, relief="flat")
    style.map("Icon.TButton", background=[("active", CARD)])
    style.configure("Star.TButton", background=SURFACE, foreground="#FFD700", font=("Segoe UI Symbol", 14), padding=(0, 0), borderwidth=0, relief="flat")
    style.map("Star.TButton", background=[("active", CARD)])