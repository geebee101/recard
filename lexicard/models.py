"""Data models and serialization for the Lexicard application.

This module defines Pydantic models for Lexicards, Decks, and Users,
and provides utility functions for loading and saving data from JSON and Excel.
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import openpyxl
from pydantic import BaseModel, ValidationError


class Lexicard(BaseModel):
    """Model for a single flashcard.

    Attributes:
            tid: Unique identifier for the card.
            sound: Filename of the audio file (without extension) or '0' if none.
            check_for_correction: Flag indicating if the card needs review for errors.
            phonetic: Phonetic transcription of the target word.
            target_word: The word or phrase in the target language.
            explain: English translation or explanation of the word.
    """

    tid: int
    sound: str
    check_for_correction: bool
    phonetic: str
    target_word: str
    explain: str


class Deck(BaseModel):
    """Model for a collection of flashcards.

    Attributes:
            author: Name of the deck creator.
            name: Name of the deck.
            description: Brief description of the deck's content.
            target_language: ISO language code (e.g., 'th', 'en').
            cards: List of Lexicard objects included in the deck.
    """

    author: str
    name: str
    description: str
    target_language: str
    _last_id_used: int  # Internal field for ID management
    cards: list[Lexicard] = []


class User(BaseModel):
    """Model for a user profile and learning progress.

    Attributes:
            tid: Unique identifier for the user.
            name: Username.
            signup_tstamp: Timestamp of account creation.
            highest_score_ever: All-time high score.
            highest_score_30d: High score within the last 30 days.
            streak: Current consecutive days of activity.
    """

    tid: int
    name: str
    signup_tstamp: datetime
    highest_score_ever: int
    highest_score_30d: int
    streak: int


# Default configuration and initial testing data
FILE_PATH = Path(__file__).parent / "deck_data.json"

TOTO_DATA = {
    "tid": 1234567890,
    "name": "toto",
    "signup_tstamp": datetime.now(),
    "highest_score_ever": 302,
    "highest_score_30d": 101,
    "streak": 21,
}

toto_user = User.model_validate(TOTO_DATA)


def save_deck_to_json_file(deck: Deck, file_path: str | Path) -> None:
    """Serialize a Deck object to a JSON file.

    Args:
            deck: The Deck instance to save.
            file_path: Destination path on the filesystem.
    """
    path = Path(file_path)
    with path.open("w", encoding="utf-8") as f:
        f.write(deck.model_dump_json(indent=2))
    print(f"Model successfully saved to {path}")


def load_deck_from_json_file(file_path: str | Path) -> Deck:
    """Deserialize a Deck object from a JSON file.

    Args:
            file_path: Path to the JSON file.

    Returns:
            A validated Deck instance.
    """
    path = Path(file_path)
    with path.open("r", encoding="utf-8") as f:
        json_raw = f.read()

    deck = Deck.model_validate_json(json_raw)
    print(f"Model successfully loaded from {path}")
    return deck


def load_deck_from_excel(file_path: str | Path = "decxample.xlsx") -> Deck:
    """Load flashcard data from an Excel workbook and convert to a Deck.

    Args:
            file_path: Path to the .xlsx file.

    Returns:
            A Deck object containing cards from the 'lexicon' sheet.
    """
    path = Path(file_path)
    wb = openpyxl.load_workbook(path, data_only=True)
    sheet = wb["lexicon"]
    cards: list[Lexicard] = []

    # Iterate over rows, assuming first row is header.
    for row_idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
        if not row or row[0] is None:
            continue

        try:
            card_data = {
                "tid": int(row[0]),
                "sound": str(row[1]) if row[1] is not None else "0",
                "check_for_correction": bool(row[2]),
                "phonetic": str(row[3]) if row[3] is not None else "",
                "target_word": str(row[4]) if row[4] is not None else "",
                "explain": str(row[5]) if row[5] is not None else "",
            }

            lexicard = Lexicard(**card_data)
            cards.append(lexicard)
        except (ValueError, TypeError, IndexError, ValidationError) as e:
            print(f"Error processing row {row_idx}: {e}")
            continue

    print(f"ABOUT TO CONVERT {len(cards)} cards")

    deck_dict: dict[str, Any] = {
        "author": "แรช",
        "name": "demodeck",
        "description": "a deck targeting Thai to demo the app.",
        "target_language": "th",
        "_last_id_used": 1538,
        "cards": cards,
    }

    return Deck(**deck_dict)


def proto_load_save() -> None:
    """Run a prototype load-and-save cycle for testing purposes."""
    test_deck = load_deck_from_excel()
    print(f"The deck {test_deck.name} has {len(test_deck.cards)} cards")

    save_deck_to_json_file(test_deck, FILE_PATH)
    rehydrated_deck = load_deck_from_json_file(FILE_PATH)

    print(rehydrated_deck == test_deck)
    print(f"The rehydrated deck {rehydrated_deck.name} has {len(rehydrated_deck.cards)} cards")


if __name__ == "__main__":
    proto_load_save()
