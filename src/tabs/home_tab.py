from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import App

from storage import get_history, is_favorite
from config import SURFACE, CARD, ON_SURFACE, PRIMARY, ON_PRIMARY, FONT_FAMILY, BORDER

def build_home_tab(app: App) -> None:
    """Build the home tab UI."""
    
    # Fixed listbox on the left side
    list_frame = ttk.Frame(app.home_tab, style="Card.TFrame")
    list_frame.pack(side="left",fill="y", padx=(4,4), pady=(8,8))
    
    # Header
    app.list_frame_header = ttk.Frame(list_frame, style="Card.TFrame")
    app.list_frame_header.pack(side="top", fill="x")
    app.history_header = ttk.Label(app.list_frame_header, text="History", style="Bold.TLabel")
    app.history_header.pack(side="left", fill="x", padx=(4,0))
    app.history_refresh_btn = ttk.Button(app.list_frame_header, text="↻", style="Icon.TButton", command=lambda: app.refresh(), width=2)
    app.history_refresh_btn.pack(side="right", fill="x", padx=(0,4))
    
    # listbox
    app.history_listbox = tk.Listbox(
        master=list_frame, height=20, bg=CARD, fg=ON_SURFACE,
        selectbackground=PRIMARY, selectforeground=ON_PRIMARY,
        font=(FONT_FAMILY, 9), relief="flat", highlightthickness=1,
        highlightcolor=PRIMARY, highlightbackground=BORDER 
    )
    app.history_listbox.pack(side="left", fill="y", expand=True)
    
    # listbox scroll
    list_scroll = ttk.Scrollbar(list_frame, orient="vertical", style="TScrollbar", command=app.history_listbox.yview)
    list_scroll.pack(side="right", fill="y")
    app.history_listbox.config(yscrollcommand=list_scroll.set)
    app.history_listbox.bind("<<ListboxSelect>>", lambda e: on_home_select(app,e))
    
    # Scrollable detail area
    app.home_canvas = tk.Canvas(app.home_tab, bg=SURFACE, highlightthickness=0)
    app.home_content = ttk.Frame(app.home_canvas, style="Card.TFrame")
    app.home_content.bind("<Configure>", lambda e: app.home_canvas.configure(scrollregion=app.home_canvas.bbox("all")))
    app.home_canvas.create_window((0, 0), window=app.home_content, anchor="nw", width=280)
    app.home_canvas.pack(side="left", fill="both", expand=True)
    # Bind mousewheel only when hovering over home canvas
    app.home_canvas.bind("<Enter>", lambda e: app.home_canvas.bind_all("<MouseWheel>", lambda evt: on_home_scroll(app, evt)))
    app.home_canvas.bind("<Leave>", lambda e: app.home_canvas.unbind_all("<MouseWheel>"))

    app.home_content.columnconfigure(0, weight=1)
    wrap = 260

    row = 0
    # Header row with word and favorite star
    header_frame = ttk.Frame(app.home_content, style="Card.TFrame")
    header_frame.grid(row=row, column=0, pady=(12, 2), padx=10, sticky="ew")

    header = ttk.Label(header_frame, textvariable=app.word_var, style="Header.TLabel", wraplength=220)
    header.pack(side="left")

    app.fav_button = ttk.Button(header_frame, textvariable=app.favorite_var, style="Star.TButton", command=app.toggle_home_favorite, width=2)
    app.fav_button.pack(side="right", padx=(4, 0))
    row += 1

    # Meta (part_of_speech and date published)
    meta = ttk.Label(app.home_content, textvariable=app.meta_var, style="Meta.TLabel")
    meta.grid(row=row, column=0, pady=(0, 8), padx=10, sticky="w")
    row += 1
    
    # Published date
    app.published_label = ttk.Label(app.home_content, textvariable=app.published_var, style="Meta.TLabel")
    app.published_label.grid(row=row, column=0, pady=(0, 8), padx=10, sticky="w")
    row += 1

    # Short definition (bold)
    app.short_def_label = ttk.Label(app.home_content, textvariable=app.short_def_var, style="Bold.TLabel",wraplength=wrap, justify="left")
    app.short_def_label.grid(row=row, column=0, padx=10, pady=(0, 6), sticky="w")
    row += 1

    # Full definition
    app.home_definition_label = ttk.Label(app.home_content, textvariable=app.definition_var, style="Body.TLabel", wraplength=wrap, justify="left")
    app.home_definition_label.grid(row=row, column=0, padx=10, pady=(0, 6), sticky="w")
    row += 1

    # Usage example
    usage_label = ttk.Label(app.home_content, textvariable=app.usage_var, style="Italic.TLabel", wraplength=wrap, justify="left")
    usage_label.grid(row=row, column=0, padx=10, pady=(0, 10), sticky="w")
    row += 1

    # Examples section
    examples_header = ttk.Label(app.home_content, text="Examples:", style="Bold.TLabel")
    examples_header.grid(row=row, column=0, padx=10, pady=(6, 2), sticky="w")
    row += 1

    app.home_examples_label = ttk.Label(app.home_content, textvariable=app.examples_var, style="Body.TLabel", wraplength=wrap, justify="left")
    app.home_examples_label.grid(row=row, column=0, padx=10, pady=(0, 10), sticky="w")
    row += 1

    # Did You Know section
    dyk_header = ttk.Label(app.home_content, text="Did you know?", style="Bold.TLabel")
    dyk_header.grid(row=row, column=0, padx=10, pady=(6, 2), sticky="w")
    row += 1

    app.home_dyk_label = ttk.Label(app.home_content, textvariable=app.dyk_var, style="Body.TLabel", wraplength=wrap, justify="left")
    app.home_dyk_label.grid(row=row, column=0, padx=10, pady=(0, 16), sticky="w")


def on_home_scroll(app: App, event: tk.Event) -> None:
    """Handle mouse wheel scroll on home tab."""
    app.home_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
def load_home(app: App) -> None:
    """Load history data into the listbox."""
    app.history_data = get_history()
    app.history_listbox.delete(0, tk.END)
    if app.history_data:
        for entry in app.history_data:
            app.history_listbox.insert(tk.END, entry.word)
        app.history_listbox.selection_set(0)
        app.history_listbox.see(0)
    
    
def on_home_select(app: App, event: tk.Event) -> None:
    """Handle selection of a word in history listbox."""
    if not app.history_listbox.curselection():
        return
    index = app.history_listbox.curselection()[0]
    entry = app.history_data[index]
    
    app.current_entry = entry

    # Update UI vars to show selected word
    app.word_var.set(entry.word)
    app.meta_var.set(f"{entry.pronunciation}  •  {entry.part_of_speech}" if entry.pronunciation else entry.part_of_speech)
    # Extract date only from published (e.g., "Mon, 20 Jan 2025 00:00:00 -0500" -> "20 Jan 2025")
    date_only = entry.published
    if entry.published:
        parts = entry.published.split()
        if len(parts) >= 4:
            date_only = f"{parts[1]} {parts[2]} {parts[3]}"
    app.published_var.set(f"Published: {date_only}" if date_only else "")
    app.short_def_var.set(entry.short_definition)
    app.definition_var.set(entry.definition)
    app.usage_var.set(f"{entry.usage_example}" if entry.usage_example else "")
    app.examples_var.set(entry.examples)
    app.dyk_var.set(entry.did_you_know)
    app.favorite_var.set("★" if is_favorite(entry.word) else "☆")
