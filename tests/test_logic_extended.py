import os
import pytest
from lexicard.models import Deck, Lexicard, load_deck_from_json_file, save_deck_to_json_file, load_deck_from_excel_file

def test_deck_json_roundtrip(tmp_path):
    card = Lexicard(tid=1, sound="s1", check_for_correction=False, phonetic="p1", target_word="t1", explain="e1")
    deck = Deck(author="a1", name="n1", description="d1", target_language="en", cards=[card])
    
    file_path = tmp_path / "test_deck.json"
    save_deck_to_json_file(deck, str(file_path))
    
    loaded_deck = load_deck_from_json_file(str(file_path))
    assert loaded_deck.name == "n1"
    assert len(loaded_deck.cards) == 1
    assert loaded_deck.cards[0].target_word == "t1"

def test_deck_from_dict():
    data = {
        "author": "a2",
        "name": "n2",
        "description": "d2",
        "target_language": "th",
        "cards": [
            {"tid": 2, "sound": "s2", "check_for_correction": True, "phonetic": "p2", "target_word": "t2", "explain": "e2"}
        ]
    }
    deck = Deck.model_validate(data)
    assert deck.author == "a2"
    assert deck.cards[0].tid == 2

def test_excel_loading_error():
    # Test with non-existent file
    with pytest.raises(Exception):
        load_deck_from_excel_file("non_existent.xlsx")

def test_save_deck_no_cards(tmp_path):
    deck = Deck(author="a3", name="n3", description="d3", target_language="en", cards=[])
    file_path = tmp_path / "empty_deck.json"
    save_deck_to_json_file(deck, str(file_path))
    assert os.path.exists(file_path)
