import json
import sys
from pathlib import Path
from typing import Any, Dict, List

from rss_client import WordEntry

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "wotd.json"


# Load data
def load_data() -> Dict[str, Any]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        return {"history": [], "favorites": []}
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"history": [], "favorites": []}

# Save data
def save_data(data: Dict[str, Any]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    
def add_history(entry:WordEntry) -> None:
    # Skip empty "word" obj
    if not entry.word or entry.word.strip() in {"(no data)", "(unknown)"}:
        return
    
    data = load_data()
    history = data.get("history", [])
    record = {
        "word": entry.word,
        "pronunciation": entry.pronunciation,
        "part_of_speech": entry.part_of_speech,
        "definition": entry.definition,
        "short_definition": entry.short_definition,
        "usage_example": entry.usage_example,
        "examples": entry.examples,
        "did_you_know": entry.did_you_know,
        "published": entry.published,
        "link": entry.link,
    }
    # Check words in history to avoid duplicates
    if not any(h.get("word") == entry.word for h in history):
        history.insert(0, record)
    data["history"] = history
    save_data(data)
    
    
def toggle_favorite(entry: WordEntry) -> bool:
    data = load_data()
    favorites = data.get("favorites", [])
    record = {
        "word": entry.word,
        "pronunciation": entry.pronunciation,
        "part_of_speech": entry.part_of_speech,
        "definition": entry.definition,
        "short_definition": entry.short_definition,
        "usage_example": entry.usage_example,
        "examples": entry.examples,
        "did_you_know": entry.did_you_know,
        "published": entry.published,
        "link": entry.link,
    }
    existing = next((f for f in favorites if f.get("word") == entry.word), None)
    if existing:
        favorites.remove(existing)
        is_favorite = False
    else:
        favorites.insert(0, record)
        is_favorite = True
    data["favorites"] = favorites
    save_data(data)
    return is_favorite

def _dict_to_entry(d: Dict[str, str]) -> WordEntry:
    """Convert a dictionary to a WordEntry dataclass."""
    return WordEntry(
        word=d.get("word", ""),
        pronunciation=d.get("pronunciation", ""),
        part_of_speech=d.get("part_of_speech", ""),
        definition=d.get("definition", ""),
        short_definition=d.get("short_definition", ""),
        usage_example=d.get("usage_example", ""),
        examples=d.get("examples", ""),
        did_you_know=d.get("did_you_know", ""),
        published=d.get("published", ""),
        link=d.get("link", ""),
    )


def get_history() -> List[WordEntry]:
    return [_dict_to_entry(d) for d in load_data().get("history", [])]


def get_favorites() -> List[WordEntry]:
    return [_dict_to_entry(d) for d in load_data().get("favorites", [])]


def is_favorite(word: str) -> bool:
    """Check if a word is in the favorites list."""
    favorites = load_data().get("favorites", [])
    return any(f.get("word") == word for f in favorites)