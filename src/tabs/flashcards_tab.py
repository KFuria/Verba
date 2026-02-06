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
    # canvas
    app.flashcard_canvas = tk.Canvas(app.flashcards_tab, bg=SURFACE, highlightthickness=0)
    container = ttk.Frame(app.flashcard_canvas, style="Card.TFrame")
    app.flashcard_canvas.create_window((225, 100), window=container, anchor="n", width=450)
    app.flashcard_canvas.pack(side="left", fill="both", expand=True)

    container.columnconfigure(0, weight=1)
    title = ttk.Label(container, textvariable=app.flashcard_title_var, style="Flashcard.TLabel", wraplength=260)
    title.grid(row=0, column=0, pady=(16, 8), padx=10)
    app.flashcard_body_label = ttk.Label(container, textvariable=app.flashcard_body_var, style="FlashcardBody.TLabel", wraplength=260, justify="left")
    app.flashcard_body_label.grid(row=1, column=0, pady=(0, 16), padx=10)
    
    controls = ttk.Frame(app.flashcard_canvas, style="Card.TFrame")
    controls.pack(side="bottom", fill="x", padx=10, pady=10)
    shuffke_btn = ttk.Button(controls, text="Shuffle", style="Primary.TButton", command=lambda: start_flashcards(app))
    shuffke_btn.pack(side="left", fill="x", padx=10, pady=10)
    flip_btn = ttk.Button(controls, text="Flip", style="Secondary.TButton", command=lambda: flip_flashcard(app))
    flip_btn.pack(side="left", fill="x", padx=10, pady=10)
    next_btn = ttk.Button(controls, text="Next", style="Secondary.TButton", command=lambda: next_flashcard(app))
    next_btn.pack(side="left", fill="x", padx=10, pady=10)


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
