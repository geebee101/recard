#
from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel, ValidationError

class Lexicard(BaseModel):
    """Model for a single flashcard.
    
    Structure for prototype only, not final.
    """
    tid: int
    sound: str # 0 or fname no ext
    check_for_correction: bool
    phonetic: str
    target_word: str
    explain: str

class Deck(BaseModel):
    """For now simple collection of cards."""
    author: str
    name: str
    description: str
    target_language: str # e.g. en, th
    _last_id_used: int
    cards: List[Lexicard] = []

class User(BaseModel):
    tid: int
    name: str
    signup_tstamp: datetime
    highest_score_ever: int
    highest_score_30d:int
    streak: int
    # cached as well, pds, etc.

toto = {
    'tid': 1234567890,
    'name': 'toto',
    'signup_tstamp': datetime.now(),
    'highest_score_ever': 302,
    'highest_score_30d':101,
    'streak': 21
    }

toto_user = User.model_validate(toto)

file_path = 'deck_data.json'

def save_deck_to_json_file(aDeck, file_path: str):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(aDeck.model_dump_json(indent=2))
    print(f"Model successfully saved to {file_path}")

def load_deck_from_json_file(file_path: str) -> Deck:
    with open(file_path, "r") as f:
        # Read the entire file content as a string
        json_raw = f.read()
    
    # Use model_validate_json to create and validate the model instance
    deck = Deck.model_validate_json(json_raw)
    print(f"Model successfully loaded from {file_path}")
    return deck

# convert initial excel

import openpyxl

def load_deck_from_excel():
    file_path = 'decxample.xlsx'
    wb = openpyxl.load_workbook(file_path, data_only=True)
    sheet = wb['lexicon']
    cards = []

    # Iterate over rows, assuming first row is header.
    for row_idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
        if not row or row[0] is None:
            continue

        try:
            card_data = {
                'tid': int(row[0]),
                'sound': row[1],
                'check_for_correction': bool(row[2]),
                'phonetic': row[3],
                'target_word': row[4],
                'explain': row[5]
                }

            lexicard = Lexicard(**card_data)
            cards.append(lexicard)
        except (ValueError, TypeError, IndexError, ValidationError) as e:
            print(f"Error processing row {row_idx}: {e}")
            continue

    print(f'ABOUT TO CONVERT {len(cards)} cards')

    deckdict = {
        'author': 'แรช',
        'name': 'demodeck',
        'description': 'a deck targeting Thai to demo the app.',
        'target_language': 'th',
        '_last_id_used': 1538,
        'cards': cards
        }

    return Deck(**deckdict)

# initial conversion and validation
def proto_load_save():
    theDeck = load_deck_from_excel()
    #print(theDeck)
    print(f'The deck {theDeck.name} has {len(theDeck.cards)} cards')
    save_deck_to_json_file(theDeck, file_path)
    aDeck = load_deck_from_json_file(file_path)
    print(aDeck == theDeck)
    print(f'The rehydrated deck {aDeck.name} has {len(aDeck.cards)} cards')

if __name__ == '__main__':
    proto_load_save()


# .end