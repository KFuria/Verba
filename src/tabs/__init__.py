from tabs.home_tab import build_home_tab, on_home_scroll
from tabs.history_tab import build_history_tab, on_history_scroll, on_history_select, load_history
from tabs.favorites_tab import build_favorites_tab, on_favorites_scroll, on_favorites_select, load_favorites, remove_selected_favorite
from tabs.flashcards_tab import build_flashcards_tab, on_flashcard_scroll, load_flashcards, start_flashcards, flip_flashcard, next_flashcard, show_flashcard

__all__ = [
    "build_home_tab",
    "on_home_scroll",
    "build_history_tab",
    "on_history_scroll",
    "on_history_select",
    "load_history",
    "build_favorites_tab",
    "on_favorites_scroll",
    "on_favorites_select",
    "load_favorites",
    "remove_selected_favorite",
    "build_flashcards_tab",
    "on_flashcard_scroll",
    "load_flashcards",
    "start_flashcards",
    "flip_flashcard",
    "next_flashcard",
    "show_flashcard",
]