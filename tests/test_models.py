import os
import pytest
from datetime import datetime
from pathlib import Path
from lexicard.models import Lexicard, Deck, User, save_deck_to_json_file, load_deck_from_json_file

@pytest.fixture
def sample_card():
    return Lexicard(
        tid=1,
        sound="test_sound",
        check_for_correction=False,
        phonetic="test",
        target_word="test",
        explain="test explanation"
    )

@pytest.fixture
def sample_deck(sample_card):
    return Deck(
        author="test author",
        name="test deck",
        description="test description",
        target_language="en",
        _last_id_used=1,
        cards=[sample_card]
    )

def test_lexicard_creation(sample_card):
    assert sample_card.tid == 1
    assert sample_card.target_word == "test"

def test_deck_creation(sample_deck, sample_card):
    assert sample_deck.name == "test deck"
    assert len(sample_deck.cards) == 1
    assert sample_deck.cards[0] == sample_card

def test_user_creation():
    user_data = {
        "tid": 123,
        "name": "test_user",
        "signup_tstamp": datetime.now(),
        "highest_score_ever": 100,
        "highest_score_30d": 50,
        "streak": 5
    }
    user = User.model_validate(user_data)
    assert user.name == "test_user"
    assert user.streak == 5

def test_deck_serialization(sample_deck, tmp_path):
    file_path = tmp_path / "test_deck.json"
    save_deck_to_json_file(sample_deck, file_path)
    assert file_path.exists()
    
    loaded_deck = load_deck_from_json_file(file_path)
    assert loaded_deck.name == sample_deck.name
    assert loaded_deck.author == sample_deck.author
    assert len(loaded_deck.cards) == len(sample_deck.cards)
    assert loaded_deck.cards[0].tid == sample_deck.cards[0].tid
