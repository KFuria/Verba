from __future__ import annotations

import random
import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import App

from config import SURFACE


def build_flashcards_tab(app: App) -> None:
    """Build the flashcards tab UI."""
    # Scrollable canvas
    app.flashcard_canvas = tk.Canvas(app.flashcards_tab, bg=SURFACE, highlightthickness=0)
    scrollbar = ttk.Scrollbar(app.flashcards_tab, orient="vertical", command=app.flashcard_canvas.yview)
    container = ttk.Frame(app.flashcard_canvas, style="Card.TFrame")

    container.bind("<Configure>", lambda e: app.flashcard_canvas.configure(scrollregion=app.flashcard_canvas.bbox("all")))
    app.flashcard_canvas.create_window((0, 0), window=container, anchor="nw", width=280)
    app.flashcard_canvas.configure(yscrollcommand=scrollbar.set)

    app.flashcard_canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    app.flashcard_canvas.bind("<Enter>", lambda e: app.flashcard_canvas.bind_all("<MouseWheel>", lambda evt: on_flashcard_scroll(app, evt)))
    app.flashcard_canvas.bind("<Leave>", lambda e: app.flashcard_canvas.unbind_all("<MouseWheel>"))

    container.columnconfigure(0, weight=1)

    title = ttk.Label(container, textvariable=app.flashcard_title_var, style="Flashcard.TLabel", wraplength=260)
    title.grid(row=0, column=0, pady=(16, 8), padx=10, sticky="w")

    app.flashcard_body_label = ttk.Label(container, textvariable=app.flashcard_body_var, style="FlashcardBody.TLabel", wraplength=260, justify="left")
    app.flashcard_body_label.grid(row=1, column=0, pady=(0, 16), padx=10, sticky="w")

    controls = ttk.Frame(container, style="Card.TFrame")
    controls.grid(row=2, column=0, pady=8)

    ttk.Button(controls, text="Shuffle", style="Primary.TButton", command=lambda: start_flashcards(app)).grid(row=0, column=0, padx=3)
    ttk.Button(controls, text="Flip", style="Secondary.TButton", command=lambda: flip_flashcard(app)).grid(row=0, column=1, padx=3)
    ttk.Button(controls, text="Next", style="Secondary.TButton", command=lambda: next_flashcard(app)).grid(row=0, column=2, padx=3)


def on_flashcard_scroll(app: App, event: tk.Event) -> None:
    """Handle mouse wheel scroll on flashcards tab."""
    app.flashcard_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


def load_flashcards(app: App) -> None:
    """Load flashcards from history data."""
    app.flashcards = list(app.history_data)
    if not app.flashcards:
        app.flashcard_title_var.set("No cards yet")
        app.flashcard_body_var.set("Add words to history to start.")
        app.flashcard_index = 0
        app.flashcard_flipped = False


def start_flashcards(app: App) -> None:
    """Start a new flashcard session with shuffled cards."""
    app.flashcards = list(app.history_data)
    if not app.flashcards:
        app.flashcard_title_var.set("No cards yet")
        app.flashcard_body_var.set("Add words to history to start.")
        return
    random.shuffle(app.flashcards)
    app.flashcard_index = 0
    app.flashcard_flipped = False
    show_flashcard(app)


def flip_flashcard(app: App) -> None:
    """Flip the current flashcard to show/hide definition."""
    if not app.flashcards:
        return
    app.flashcard_flipped = not app.flashcard_flipped
    show_flashcard(app)


def next_flashcard(app: App) -> None:
    """Move to the next flashcard."""
    if not app.flashcards:
        return
    app.flashcard_index = (app.flashcard_index + 1) % len(app.flashcards)
    app.flashcard_flipped = False
    show_flashcard(app)


def show_flashcard(app: App) -> None:
    """Display the current flashcard."""
    entry = app.flashcards[app.flashcard_index]
    app.flashcard_title_var.set(entry.word)
    app.flashcard_body_var.set(entry.definition if app.flashcard_flipped else "(Click Flip to reveal definition)")
