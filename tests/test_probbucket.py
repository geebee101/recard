import pytest
from lexicard.models import Lexicard
from lexicard.probbucket import ProbBucket

@pytest.fixture
def sample_cards():
    return [
        Lexicard(tid=i, sound="0", check_for_correction=False, phonetic=f"p{i}", target_word=f"t{i}", explain=f"e{i}")
        for i in range(1, 11)
    ]

def test_probbucket_init(sample_cards):
    pb = ProbBucket(sample_cards)
    assert len(pb._learn) == 10
    assert len(pb._known) == 0
    assert len(pb._review) == 0

def test_pick_card(sample_cards):
    pb = ProbBucket(sample_cards)
    card = pb.pick_card()
    assert card in sample_cards
    # The picked card is also stored in _current_card
    assert pb._current_card == card

def test_promote_demote(sample_cards):
    pb = ProbBucket(sample_cards[:1])
    card = sample_cards[0]
    
    # Initial state: in learn
    assert card in pb._learn
    
    # Promote to review
    pb.promote(card)
    assert card not in pb._learn
    assert card in pb._review
    
    # Promote to known
    pb.promote(card)
    assert card not in pb._review
    assert card in pb._known
    
    # Demote to review
    pb.demote(card)
    assert card not in pb._known
    assert card in pb._review
    
    # Demote to learn
    pb.demote(card)
    assert card not in pb._review
    assert card in pb._learn

def test_promote_high_priority(sample_cards):
    pb = ProbBucket(sample_cards[:1])
    card = sample_cards[0]
    pb.promote(card, high_priority=True)
    assert card in pb._known
    assert card not in pb._learn

def test_pick_3_cards(sample_cards):
    pb = ProbBucket(sample_cards)
    q, a1, a2 = pb.pick_3_cards()
    assert q is not None
    assert a1 is not None
    assert a2 is not None
    assert q != a1
    assert q != a2
    assert a1 != a2

def test_forget_all(sample_cards):
    pb = ProbBucket(sample_cards)
    pb.promote(sample_cards[0], high_priority=True)
    pb.forget_all()
    assert len(pb._learn) == 0
    assert len(pb._known) == 0
    assert len(pb._review) == 0

def test_get_current_card(sample_cards):
    pb = ProbBucket(sample_cards)
    assert pb._current_card is None
    card = pb.get_current_card()
    assert card is not None
    assert pb._current_card == card
    
    # Subsequent call returns the same card
    assert pb.get_current_card() == card

def test_add_cards(sample_cards):
    pb = ProbBucket()
    pb.add_cards(sample_cards)
    assert len(pb._learn) == len(sample_cards)

def test_promote_missing_card(sample_cards):
    pb = ProbBucket(sample_cards[:1])
    missing_card = sample_cards[5]
    # Should not raise error, just stay the same
    pb.promote(missing_card)
    assert len(pb._learn) == 1
    assert len(pb._review) == 0
    assert len(pb._known) == 0

def test_x_add_cards_under_limit(sample_cards):
    pb = ProbBucket()
    pb.x_add_cards(sample_cards)
    assert len(pb._learn) == len(sample_cards)

