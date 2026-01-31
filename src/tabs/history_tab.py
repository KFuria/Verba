from __future__ import annotations
import tkinter as tk
from tkinter import ttk

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import App
    
from storage import get_history, is_favorite
from config import SURFACE, CARD, ON_SURFACE, PRIMARY, ON_PRIMARY, FONT_FAMILY, BORDER

def build_history_tab(app: App):
    """Build the history tab UI"""
    
    # Fixed listbox at top
    list_frame = ttk.Frame(app.history_tab, style="Card.TFrame")
    list_frame.pack(fill="x", padx=8, pady=(8,4))
    app.history_listbox = tk.Listbox(
        master=list_frame, height=6, bg=CARD, fg=ON_SURFACE,
        selectbackground=PRIMARY, selectforeground=ON_PRIMARY,
        font=(FONT_FAMILY, 9), relief="flat", highlightthickness=1,
        highlightcolor=PRIMARY, highlightbackground=BORDER 
    )
    app.history_listbox.pack(side="left", fill="x", expand=True)
    list_scroll = ttk.Scrollbar(list_frame, orient="vertical", command=app.history_listbox.yview)
    list_scroll.pack(side="right", fill="y")
    app.history_listbox.config(yscrollcommand=list_scroll.set)
    app.history_listbox.bind("<<ListboxSelect>>", lambda e: on_history_select(app,e))
    
    # Scrollable detail area
    app.history_canvas = tk.Canvas(app.history_tab, bg=SURFACE, highlightthickness=0)
    detail_scrollable = ttk.Scrollbar(app.history_tab, orient="vertical", command=app.history_canvas.yview)
    app.history_detail_frame = ttk.Frame(app.history_canvas, style="Card.TFrame")
    app.history_detail_frame.bind("<Configure>", lambda e: app.history_canvas.configure(scrollregion=app.history_canvas.bbox("all")))
    app.history_canvas.create_window((0,0), window=app.history_detail_frame, anchor="nw", width=265)
    app.history_canvas.configure(yscrollcommand=detail_scrollable.set)
    app.history_canvas.pack(side="left", fill="both", expand=True, padx=(8,0))
    detail_scrollable.pack(side="right", fill="y")
    app.history_canvas.bind("<Enter>", lambda e: app.history_canvas.bind_all("<MouseWheel>", lambda evt: on_history_scroll(app,evt)))
    app.history_canvas.bind("<Leave>", lambda e: app.history_canvas.unbind_all("<MouseWheel>"))

    app.history_detail_frame.columnconfigure(0, weight=1)
    wrap = 250
    row = 0
    
    # Placeholder label (shown when no word is selected)
    app.history_placeholder = ttk.Label(app.history_detail_frame, textvariable=app.history_detail_var, style="Meta.TLabel")
    app.history_placeholder.grid(row=row, column=0, sticky="w", padx=10, pady=(8, 4))
    row += 1
    
    # Word header with favorite button
    hist_header_frame = ttk.Frame(app.history_detail_frame, style="Card.TFrame")
    hist_header_frame.grid(row=row, column=0, pady=(12, 2), padx=10, sticky="ew")
    app.hist_word_label = ttk.Label(hist_header_frame, textvariable=app.hist_word_var, style="Header.TLabel")
    app.hist_word_label.pack(side="left")
    app.hist_fav_button = ttk.Button(hist_header_frame, textvariable=app.hist_favorite_var, style="Star.TButton", command=app.toggle_history_favorite, width=2)
    app.hist_fav_button.pack(side="right", padx=(4, 0))
    row += 1

    # Meta (part of speech)
    app.hist_meta_label = ttk.Label(app.history_detail_frame, textvariable=app.hist_meta_var, style="Meta.TLabel")
    app.hist_meta_label.grid(row=row, column=0, pady=(0, 2), padx=10, sticky="w")
    row += 1
    
    # Published date
    app.hist_published_label = ttk.Label(app.history_detail_frame, textvariable=app.hist_published_var, style="Meta.TLabel")
    app.hist_published_label.grid(row=row, column=0, pady=(0, 8), padx=10, sticky="w")
    row += 1

    # Short definition
    app.hist_short_def_label = ttk.Label(app.history_detail_frame, textvariable=app.hist_short_def_var, style="Bold.TLabel", wraplength=wrap, justify="left")
    app.hist_short_def_label.grid(row=row, column=0, padx=10, pady=(0, 6), sticky="w")
    row += 1

    # Full definition
    app.hist_def_label = ttk.Label(app.history_detail_frame, textvariable=app.hist_def_var, style="Body.TLabel", wraplength=wrap, justify="left")
    app.hist_def_label.grid(row=row, column=0, padx=10, pady=(0, 6), sticky="w")
    row += 1

    # Usage example
    app.hist_usage_label = ttk.Label(app.history_detail_frame, textvariable=app.hist_usage_var, style="Italic.TLabel", wraplength=wrap, justify="left")
    app.hist_usage_label.grid(row=row, column=0, padx=10, pady=(0, 10), sticky="w")
    row += 1

    # Examples header
    app.hist_examples_header = ttk.Label(app.history_detail_frame, text="Examples:", style="Bold.TLabel")
    app.hist_examples_header.grid(row=row, column=0, padx=10, pady=(6, 2), sticky="w")
    row += 1

    app.hist_examples_label = ttk.Label(app.history_detail_frame, textvariable=app.hist_examples_var, style="Body.TLabel", wraplength=wrap, justify="left")
    app.hist_examples_label.grid(row=row, column=0, padx=10, pady=(0, 10), sticky="w")
    row += 1

    # Did you know header
    app.hist_dyk_header = ttk.Label(app.history_detail_frame, text="Did you know?", style="Bold.TLabel")
    app.hist_dyk_header.grid(row=row, column=0, padx=10, pady=(6, 2), sticky="w")
    row += 1

    app.hist_dyk_label = ttk.Label(app.history_detail_frame, textvariable=app.hist_dyk_var, style="Body.TLabel", wraplength=wrap, justify="left")
    app.hist_dyk_label.grid(row=row, column=0, padx=10, pady=(0, 16), sticky="w")

def on_history_scroll(app: App, event: tk.Event) -> None:
    """Handle mouse wheel scroll on history tab."""
    app.history_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    
def load_history(app: App) -> None:
    """Load history data into the listbox."""
    app.history_data = get_history()
    app.history_listbox.delete(0, tk.END)
    for entry in app.history_data:
        app.history_listbox.insert(tk.END, entry.word)
    if not app.history_data:
        app.history_detail_var.set("No history yet.")


def on_history_select(app: App, event: tk.Event) -> None:
    """Handle selection of a word in history listbox."""
    if not app.history_listbox.curselection():
        return
    index = app.history_listbox.curselection()[0]
    entry = app.history_data[index]

    # Hide placeholder
    app.history_detail_var.set("")

    # Update favorite button state
    app.hist_favorite_var.set("★" if is_favorite(entry.word) else "☆")

    app.hist_word_var.set(entry.word)
    app.hist_meta_var.set(f"{entry.pronunciation}  •  {entry.part_of_speech}" if entry.pronunciation else entry.part_of_speech)
    # Extract date only from published (e.g., "Mon, 20 Jan 2025 00:00:00 -0500" -> "20 Jan 2025")
    date_only = entry.published
    if entry.published:
        parts = entry.published.split()
        if len(parts) >= 4:
            date_only = f"{parts[1]} {parts[2]} {parts[3]}"
    app.hist_published_var.set(f"Published: {date_only}" if date_only else "")
    app.hist_short_def_var.set(entry.short_definition)
    app.hist_def_var.set(entry.definition)
    app.hist_usage_var.set(f"{entry.usage_example}" if entry.usage_example else "")
    app.hist_examples_var.set(entry.examples)
    app.hist_dyk_var.set(entry.did_you_know)

    # Show/hide headers based on content
    if entry.examples:
        app.hist_examples_header.grid()
    else:
        app.hist_examples_header.grid_remove()
    if entry.did_you_know:
        app.hist_dyk_header.grid()
    else:
        app.hist_dyk_header.grid_remove()