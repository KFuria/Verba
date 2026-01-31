import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk

from rss_client import fetch_latest_word, WordEntry
from storage import add_history, toggle_favorite
from tabs import (
    build_home_tab,
    build_history_tab,
    build_favorites_tab,
    build_flashcards_tab,
    load_history,
    load_favorites,
    load_flashcards,
)

from config import BACKGROUND

from config import setup_styles

class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Verba")
        self.geometry("300x580")
        self.resizable(False, False)
        self.configure(bg=BACKGROUND)
        
        self._set_window_icon()
        self._set_dark_title_bar()
        setup_styles(self)
        
        # Home StringVars
        self.word_var = tk.StringVar(value="Loading...")
        self.meta_var = tk.StringVar(value="")
        self.definition_var = tk.StringVar(value="")
        self.short_def_var = tk.StringVar(value="")
        self.usage_var = tk.StringVar(value="")
        self.examples_var = tk.StringVar(value="")
        self.dyk_var = tk.StringVar(value="")
        self.favorite_var = tk.StringVar(value="☆")
        self.history_detail_var = tk.StringVar(value="Select a word to see details.")
        self.favorites_detail_var = tk.StringVar(value="Select a word to see details.")
        
        # History StringVars
        self.hist_word_var = tk.StringVar(value="")
        self.hist_meta_var = tk.StringVar(value="")
        self.hist_published_var = tk.StringVar(value="")
        self.hist_favorite_var = tk.StringVar(value="☆")
        self.hist_short_def_var = tk.StringVar(value="")
        self.hist_usage_var = tk.StringVar(value="")
        self.hist_def_var = tk.StringVar(value="")
        self.hist_examples_var = tk.StringVar(value="")
        self.hist_dyk_var = tk.StringVar(value="")

        # Favorites StringVars
        self.fav_word_var = tk.StringVar(value="")
        self.fav_meta_var = tk.StringVar(value="")
        self.fav_short_def_var = tk.StringVar(value="")
        self.fav_usage_var = tk.StringVar(value="")
        self.fav_def_var = tk.StringVar(value="")
        self.fav_examples_var = tk.StringVar(value="")
        self.fav_dyk_var = tk.StringVar(value="")

        # Flashcard StringVars
        self.flashcard_title_var = tk.StringVar(value="No cards yet")
        self.flashcard_body_var = tk.StringVar(value="Add words to history to start.")
        
        # Notebook
        self.notebook = ttk.Notebook(self, style="TNotebook")
        self.notebook.pack(fill="both", expand=True, padx=4, pady=(4, 0))

        self.home_tab = ttk.Frame(self.notebook, style="Card.TFrame")
        self.history_tab = ttk.Frame(self.notebook, style="Card.TFrame")
        self.favorites_tab = ttk.Frame(self.notebook, style="Card.TFrame")
        self.flashcards_tab = ttk.Frame(self.notebook, style="Card.TFrame")

        self.notebook.add(self.home_tab, text="Home")
        self.notebook.add(self.history_tab, text="History")
        self.notebook.add(self.favorites_tab, text="Favorites")
        self.notebook.add(self.flashcards_tab, text="Flashcards")

        # Footer with refresh button at bottom
        footer_bar = ttk.Frame(self, style="Card.TFrame")
        footer_bar.pack(fill="x", padx=4, pady=(0, 4))
        refresh_btn = ttk.Button(footer_bar, text="↻", style="Icon.TButton", command=self.refresh, width=2)
        refresh_btn.pack(pady=4)
        
        
        build_home_tab(self)
        build_history_tab(self)
        build_favorites_tab(self)
        build_flashcards_tab(self)

        
        self.current_entry: WordEntry | None = None
        self.history_data: list[WordEntry] = []
        self.favorites_data: list[WordEntry] = []
        self.flashcards: list[WordEntry] = []
        self.flashcard_index = 0
        self.flashcard_flipped = False

        self.after(100, self.refresh)  
        
    def _set_window_icon(self) -> None:
        icon_name = "icon.ico"
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            icon_path = Path(sys._MEIPASS) / icon_name
        else:
            icon_path = Path(__file__).resolve().parent.parent / icon_name

        if icon_path.exists():
            try:
                self.iconbitmap(str(icon_path))
            except tk.TclError:
                pass
    
    def _set_dark_title_bar(self) -> None:
        """Enable dark mode for the Windows title bar."""
        if sys.platform != "win32":
            return
        try:
            import ctypes
            self.update()  # Ensure window is created
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE,
                ctypes.byref(ctypes.c_int(1)), ctypes.sizeof(ctypes.c_int)
            )
        except Exception:
            pass
            
    def refresh(self) -> None:
        entry = fetch_latest_word()
        self.current_entry = entry
        self.word_var.set(f"{entry.word}  ({entry.pronunciation})" if entry.pronunciation else entry.word)
        
        # Extract date from published (e.g., "Mon, 20 Jan 2025 00:00:00 -0500" -> "20 Jan 2025")
        date_only = entry.published
        if entry.published:
            parts = entry.published.split()
            if len(parts) >= 4:
                date_only = f"{parts[1]} {parts[2]} {parts[3]}"
        
        self.meta_var.set(f"{entry.part_of_speech}  •  {date_only}" if entry.part_of_speech else date_only)
        self.short_def_var.set(entry.short_definition)
        self.definition_var.set(entry.definition)
        self.usage_var.set(entry.usage_example)
        self.examples_var.set(entry.examples)
        self.dyk_var.set(entry.did_you_know)
        
        add_history(entry)
        self.favorite_var.set("☆")
        load_history(self)
        load_favorites(self)
        load_flashcards(self)

    def toggle_home_favorite(self) -> None:
        """Toggle favorite status for the current word entry."""
        if not self.current_entry:
            return
        is_fav = toggle_favorite(self.current_entry)
        self.favorite_var.set("★" if is_fav else "☆")
        load_favorites(self)

    def toggle_history_favorite(self) -> None:
        """Toggle favorite status for the currently selected history entry."""
        if not hasattr(self, 'history_listbox') or not self.history_listbox.curselection():
            return
        index = self.history_listbox.curselection()[0]
        entry = self.history_data[index]
        is_fav = toggle_favorite(entry)
        self.hist_favorite_var.set("★" if is_fav else "☆")
        load_favorites(self)

if __name__ == "__main__":
    app = App()
    app.mainloop()