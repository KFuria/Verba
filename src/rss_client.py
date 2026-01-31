import html
import re
from dataclasses import dataclass
import feedparser

FEED_URL = "https://www.merriam-webster.com/wotd/feed/rss2"


@dataclass(frozen=True)
class WordEntry:
    word: str
    pronunciation: str
    part_of_speech: str
    definition: str
    short_definition: str
    usage_example: str
    examples: str
    did_you_know: str
    published: str
    link: str
    
def _strip_html(text:str) -> str:
    # remove anchor tags
    text = re.sub(r"<a[^>]*>([^<]*)</a>", r"\1", text)
    # HTML tags
    plain = re.sub(r"<[^>]+>", "", text)
    # URLs
    plain = re.sub(r"https?://\S+","", plain)
    
    return html.unescape(plain).strip()

def _extract_section(text:str, start_marker: str, end_markers:list[str]) -> str:
    start_idx = text.find(start_marker)
    if start_idx == -1:
        return ""
    start_idx += len(start_marker)
    end_idx = len(text)
    for marker in end_markers:
        idx = text.find(marker, start_idx)
        if idx != -1 and idx < end_idx:
            end_idx = idx
    return text[start_idx:end_idx].strip()

def _parse_description(raw:str) -> dict[str,str]:
    result = {
        "pronunication": "",
        "part_of_speech": "",
        "definition": "",
        "usage_example": "",
        "examples" : "",
        "did_you_know": ""
    }
    
    # pronunciation (\word\)
    pronunciation_match = re.search(r"\\([^\\]+)\\", raw)
    if pronunciation_match:
        result["pronunciation"] = pronunciation_match.group(1).strip()
    
    # part of speech (<em>part-of-speed-</em>)
    pos_match = re.search(r"\\[^\\]+\\[^<]*<em>([^<]+)</em>", raw)
    if pos_match:
        result["part_of_speech"] = pos_match.group(1).strip()
    
    # definition (<p> definition </p>\n<p>//USAGE</p>)
    def_match = re.search(r"</em><br\s*/?>.*?<p>(.+?)</p>", raw, re.DOTALL)
    if def_match:
        result["definition"] = _strip_html(def_match.group(1))
        
    # usage example
    usage_match = re.search(r"<p>\s*//\s*(.+?)</p>", raw, re.DOTALL)
    if usage_match:
        result["usage_example"] = _strip_html(usage_match.group(1))
        
    # Examples
    examples = _extract_section(raw, "<strong>Examples:</strong>", ["<strong>Did you know?"])
    if examples:
        result["examples"] = _strip_html(examples)
    
    # Did you know
    dyk = _extract_section(raw, "<strong>Did you know?</strong>", ["<br /><br />", "</font>"])
    if dyk:
        result["did_you_know"] = _strip_html(dyk)
        
    return result

def fetch_latest_word() -> WordEntry:
    feed = feedparser.parse(FEED_URL)
    
    # if feed is not valid
    if not feed.entries:
        return WordEntry(
            word = "(no data)",
            pronunciation="",
            part_of_speech="",
            definition="",
            short_definition="",
            usage_example="",
            examples="",
            did_you_know="",
            published="",
            link=FEED_URL
        )
    
    entry = feed.entries[0]
    raw_description = getattr(entry, "summary", "") or ""
    parsed = _parse_description(raw_description)
    
    # Get short definition from merriam namespace
    short_def = ""
    if hasattr(entry, "merriam_shortdef"):
        raw_short = entry.merriam_shortdef
        if isinstance(raw_short, str):
            short_def = _strip_html(raw_short)
        elif isinstance(raw_short, list) and raw_short:
            short_def = _strip_html(str(raw_short[0]))
    
    return WordEntry(
        word = getattr(entry, "title", "(unknown)") or "(unknown)",
        pronunciation=parsed["pronunciation"],
        part_of_speech=parsed["part_of_speech"],
        definition=parsed["definition"],
        short_definition=short_def,
        usage_example=parsed["usage_example"],
        examples=parsed["examples"],
        did_you_know=parsed["did_you_know"],
        published=getattr(entry, "published", "") or "",
        link=getattr(entry, "link", FEED_URL) or FEED_URL
    )

if __name__ == "__main__":   
    entry = fetch_latest_word()
    print(entry.word)
    print(entry.pronunciation)
    print(entry.part_of_speech)
    print(entry.definition)
    print(entry.short_definition)
    print(entry.usage_example)
    print(entry.examples)
    print(entry.did_you_know)
    print(entry.published)
    print(entry.link)
