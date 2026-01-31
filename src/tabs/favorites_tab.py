from __future__ import annotations
import tkinter as tk
from tkinter import ttk

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import App
    
from storage import get_favorites, toggle_favorite
from config import SURFACE, CARD, ON_SURFACE, PRIMARY, ON_PRIMARY, FONT_FAMILY, BORDER


def build_favorites_tab(app: App) -> None:
    """Build the favorites tab UI."""
    
    # Fixed listbox at top
    list_frame = ttk.Frame(app.favorites_tab, style="Card.TFrame")
    list_frame.pack(fill="x", padx=8, pady=(8,4))
    app.favorites_listbox = tk.Listbox(
        master=list_frame, height=6, bg=CARD, fg=ON_SURFACE,
        selectbackground=PRIMARY, selectforeground=ON_PRIMARY,
        font=(FONT_FAMILY, 9), relief="flat", highlightthickness=1,
        highlightcolor=PRIMARY, highlightbackground=BORDER
    )
    app.favorites_listbox.pack(side="left", fill="x", expand=True)
    list_scroll = ttk.Scrollbar(list_frame, orient="vertical", command=app.favorites_listbox.yview)
    list_scroll.pack(side="right", fill="y")
    app.favorites_listbox.config(yscrollcommand=list_scroll.set)
    app.favorites_listbox.bind("<<ListboxSelect>>", lambda e: on_favorites_select(app,e))

    # Remove button below listbox
    remove_button = ttk.Button(app.favorites_tab, text="Remove", style="Primary.TButton", command=lambda: remove_selected_favorite(app))
    remove_button.pack(pady=(4, 4))

    # Scrollable detail area
    app.favorites_canvas = tk.Canvas(app.favorites_tab, bg=SURFACE, highlightthickness=0)
    detail_scrollbar = ttk.Scrollbar(app.favorites_tab, orient="vertical", command=app.favorites_canvas.yview)
    app.favorites_detail_frame = ttk.Frame(app.favorites_canvas, style="Card.TFrame")
    app.favorites_detail_frame.bind("<Configure>", lambda e: app.favorites_canvas.configure(scrollregion=app.favorites_canvas.bbox("all")))
    app.favorites_canvas.create_window((0, 0), window=app.favorites_detail_frame, anchor="nw", width=265)
    app.favorites_canvas.configure(yscrollcommand=detail_scrollbar.set)
    app.favorites_canvas.pack(side="left", fill="both", expand=True, padx=(8,0))
    detail_scrollbar.pack(side="right", fill="y")
    app.favorites_canvas.bind("<Enter>", lambda e: app.favorites_canvas.bind_all("<MouseWheel>", lambda evt: on_favorites_scroll(app, evt)))
    app.favorites_canvas.bind("<Leave>", lambda e: app.favorites_canvas.unbind_all("<MouseWheel>"))

    app.favorites_detail_frame.columnconfigure(0, weight=1)
    wrap = 250
    row = 0

    # Placeholder label (shown when no selection)
    app.favorites_placeholder = ttk.Label(app.favorites_detail_frame, textvariable=app.favorites_detail_var, style="Meta.TLabel")
    app.favorites_placeholder.grid(row=row, column=0, sticky="w", padx=10, pady=(8, 4))
    row += 1

    # Word header
    app.fav_word_label = ttk.Label(app.favorites_detail_frame, textvariable=app.fav_word_var, style="Header.TLabel")
    app.fav_word_label.grid(row=row, column=0, pady=(12, 2), padx=10, sticky="w")
    row += 1

    # Meta (part of speech)
    app.fav_meta_label = ttk.Label(app.favorites_detail_frame, textvariable=app.fav_meta_var, style="Meta.TLabel")
    app.fav_meta_label.grid(row=row, column=0, pady=(0, 8), padx=10, sticky="w")
    row += 1

    # Short definition
    app.fav_short_def_label = ttk.Label(app.favorites_detail_frame, textvariable=app.fav_short_def_var, style="Bold.TLabel", wraplength=wrap, justify="left")
    app.fav_short_def_label.grid(row=row, column=0, padx=10, pady=(0, 6), sticky="w")
    row += 1

    # Full definition
    app.fav_def_label = ttk.Label(app.favorites_detail_frame, textvariable=app.fav_def_var, style="Body.TLabel", wraplength=wrap, justify="left")
    app.fav_def_label.grid(row=row, column=0, padx=10, pady=(0, 6), sticky="w")
    row += 1

    # Usage example
    app.fav_usage_label = ttk.Label(app.favorites_detail_frame, textvariable=app.fav_usage_var, style="Italic.TLabel", wraplength=wrap, justify="left")
    app.fav_usage_label.grid(row=row, column=0, padx=10, pady=(0, 10), sticky="w")
    row += 1

    # Examples header
    app.fav_examples_header = ttk.Label(app.favorites_detail_frame, text="Examples:", style="Bold.TLabel")
    app.fav_examples_header.grid(row=row, column=0, padx=10, pady=(6, 2), sticky="w")
    row += 1

    app.fav_examples_label = ttk.Label(app.favorites_detail_frame, textvariable=app.fav_examples_var, style="Body.TLabel", wraplength=wrap, justify="left")
    app.fav_examples_label.grid(row=row, column=0, padx=10, pady=(0, 10), sticky="w")
    row += 1

    # Did you know header
    app.fav_dyk_header = ttk.Label(app.favorites_detail_frame, text="Did you know?", style="Bold.TLabel")
    app.fav_dyk_header.grid(row=row, column=0, padx=10, pady=(6, 2), sticky="w")
    row += 1

    app.fav_dyk_label = ttk.Label(app.favorites_detail_frame, textvariable=app.fav_dyk_var, style="Body.TLabel", wraplength=wrap, justify="left")
    app.fav_dyk_label.grid(row=row, column=0, padx=10, pady=(0, 16), sticky="w")


def on_favorites_scroll(app: App, event: tk.Event) -> None:
    """Handle mouse wheel scroll on favorites tab."""
    app.favorites_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


def load_favorites(app: App) -> None:
    """Load favorites data into the listbox."""
    app.favorites_data = get_favorites()
    app.favorites_listbox.delete(0, tk.END)
    for entry in app.favorites_data:
        app.favorites_listbox.insert(tk.END, entry.word)
    if not app.favorites_data:
        app.favorites_detail_var.set("No favorites yet.")


def on_favorites_select(app: App, event: tk.Event) -> None:
    """Handle selection of a word in favorites listbox."""
    if not app.favorites_listbox.curselection():
        return
    index = app.favorites_listbox.curselection()[0]
    entry = app.favorites_data[index]

    # Hide placeholder
    app.favorites_detail_var.set("")

    app.fav_word_var.set(entry.word)
    app.fav_meta_var.set(f"{entry.pronunciation}  •  {entry.part_of_speech}" if entry.pronunciation else entry.part_of_speech)
    app.fav_short_def_var.set(entry.short_definition)
    app.fav_def_var.set(entry.definition)
    app.fav_usage_var.set(f"{entry.usage_example}" if entry.usage_example else "")
    app.fav_examples_var.set(entry.examples)
    app.fav_dyk_var.set(entry.did_you_know)

    # Show/hide headers based on content
    if entry.examples:
        app.fav_examples_header.grid()
    else:
        app.fav_examples_header.grid_remove()
    if entry.did_you_know:
        app.fav_dyk_header.grid()
    else:
        app.fav_dyk_header.grid_remove()


def remove_selected_favorite(app: App) -> None:
    """Remove the selected favorite from the list."""
    if not app.favorites_listbox.curselection():
        return
    index = app.favorites_listbox.curselection()[0]
    entry = app.favorites_data[index]
    toggle_favorite(entry)
    load_favorites(app)
    
    app.fav_word_var.set("")
    app.fav_meta_var.set("")
    app.fav_short_def_var.set("")
    app.fav_def_var.set("")
    app.fav_usage_var.set("")
    app.fav_examples_var.set("")
    app.fav_dyk_var.set("")
    
    app.favorites_detail_var.set("Select word to display")