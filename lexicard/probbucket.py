"""Module for managing word learning probability buckets.

This module provides the ProbBucket class which tracks words in different stages of learning
and selects them based on weighted probabilities.
"""

import random
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .models import Deck, Lexicard


class ProbBucket:
    """A weighted probability system for selecting flashcards.

    Cards are organized into three buckets: known, review, and learn.
    Selection is weighted to favor cards that are still being learned or need review.
    """

    LIMIT = 3000  # memory is limited, older known words might be removed to make space

    def __init__(self, cards_list: list["Lexicard"] | None = None) -> None:
        """Initialize the probability bucket with an optional list of cards.

        Args:
                cards_list: Initial cards to put into the 'learn' bucket.
        """
        self._known: list[Lexicard] = []
        self._review: list[Lexicard] = []
        if cards_list:
            self._learn: list[Lexicard] = cards_list.copy()
        else:
            self._learn: list[Lexicard] = []

        self.print_sizes()
        self._current_card: Lexicard | None = None

    def get_current_card(self) -> Optional["Lexicard"]:
        """Retrieve the current card or pick a new one if none exists.

        Returns:
                The current Lexicard object or None if no cards are available.
        """
        if not self._current_card:
            self._current_card = self.pick_card()
        return self._current_card

    def print_sizes(self) -> None:
        """Print the current count of cards in each bucket to the console."""
        print(f"known {len(self._known)} ——— review {len(self._review)} ——— learn {len(self._learn)}")

    def add_cards(self, cards_list: list["Lexicard"]) -> "ProbBucket":
        """Add new cards to the 'learn' bucket.

        Args:
                cards_list: List of Lexicard objects to add.

        Returns:
                The current ProbBucket instance.
        """
        self._learn.extend(cards_list)
        self.print_sizes()
        return self

    def pick_card(self, exclude: list["Lexicard"] | None = None) -> Optional["Lexicard"]:
        """Pick a single card based on the current learning state probabilities.

        Args:
                exclude: Optional list of cards to ignore during selection.

        Returns:
                A randomly selected Lexicard or None if empty.
        """
        if not self._learn:
            if not self._review:
                if not self._known:
                    print("ERROR no cards")
                    return None
                else:
                    probs = [100, 0, 0]
            else:  # have review
                if not self._known:
                    probs = [0, 100, 0]
                else:
                    probs = [30, 70, 0]
        else:  # have learn
            if not self._review:
                if not self._known:
                    probs = [0, 0, 100]
                else:
                    probs = [30, 0, 70]
            else:  # have review
                if not self._known:
                    probs = [0, 30, 70]
                else:
                    probs = [10, 20, 70]
        print(probs)
        return self._pick(probs, exclude)

    def _pick(self, probs: list[int], exclude: list["Lexicard"] | None = None) -> Optional["Lexicard"]:
        """Internal method for weighted selection with safety retries and fallbacks.

        Args:
                probs: A list of 3 integers representing weights for [known, review, learn].
                exclude: Optional list of cards to exclude from selection.

        Returns:
                A selected Lexicard or None.
        """
        exclude_ids = {c.tid for c in exclude} if exclude else set()

        # Try random weighted selection first (max 50 retries for efficiency)
        for _ in range(50):
            chosen_collection = random.choices([self._known, self._review, self._learn], weights=probs, k=1)[
                0
            ]
            if not chosen_collection:
                continue

            picked = random.choice(chosen_collection)
            if picked.tid not in exclude_ids:
                print(picked)
                self._current_card = picked
                return picked

        # Fallback: if random picking fails (e.g., small buckets), look at all available cards
        all_possible = self._known + self._review + self._learn
        # Use a dict for de-duplication by tid to simulate set behavior
        unique_cards = {c.tid: c for c in all_possible}.values()
        available = [c for c in unique_cards if c.tid not in exclude_ids]

        if not available:
            print("ERROR: Not enough unique cards available to pick with current exclusion list.")
            return None

        picked = random.choice(available)
        print(f"Fallback selection used: {picked}")
        self._current_card = picked
        return picked

    def pick_3_cards(self) -> tuple[Optional["Lexicard"], Optional["Lexicard"], Optional["Lexicard"]]:
        """Pick one question card and two incorrect answer cards.

        Returns:
                A tuple of (question_card, incorrect_1, incorrect_2).
        """
        q = self.pick_card()
        a1 = self.pick_card([q]) if q else None
        a2 = self.pick_card([q, a1]) if q and a1 else None
        return q, a1, a2

    def _forget(self) -> None:
        """Internal method to remove a 'known' card when the memory limit is reached."""
        if len(self._known) == 0:
            print("ERROR: memory full, cannot add new word(s)")
            return
        to_forget = self._pick([100, 0, 0])  # select from words that have been mastered
        if to_forget:
            self._known.remove(to_forget)

    def forget_known(self) -> None:
        """Clear the 'known' bucket completely."""
        self._known = []

    def forget_all(self) -> None:
        """Clear all buckets (known, review, and learn)."""
        self._known = []
        self._review = []
        self._learn = []

    def x_add_cards(self, cards: list["Lexicard"]) -> None:
        """Add a large set of cards, potentially purging old 'known' cards if over limit.

        Args:
                cards: List of Lexicard objects to add.
        """
        lk = len(self._known)
        lr = len(self._review)
        ll = len(self._learn)
        ln = len(cards)
        if lk + lr + ll + ln >= self.LIMIT:  # need more space
            if ln > lk:
                print("ERROR: too many new words")
                return
            if lk <= (lk + lr + ll + ln - self.LIMIT):
                print("ERROR: too many new words")
                return
            for _ in range(lk + lr + ll + ln - self.LIMIT):
                self._forget()
        self._learn.extend(cards)

    def promote(self, card: "Lexicard", high_priority: bool = False) -> None:
        """Move a card to the next higher learning stage.

        Args:
                card: The card to promote.
                high_priority: If True, moves directly to 'known' from 'learn'.
        """
        self.print_sizes()
        if card in self._known:
            pass  # nothing to do, already at top
        elif card in self._review:
            self._review.remove(card)
            self._known.append(card)
        else:  # assume! card in _learn
            if card in self._learn:
                self._learn.remove(card)
                if high_priority:
                    self._known.append(card)
                else:
                    self._review.append(card)
        self.print_sizes()

    def demote(self, card: "Lexicard") -> None:
        """Move a card back to a lower learning stage.

        Args:
                card: The card to demote.
        """
        self.print_sizes()
        if card in self._known:
            self._known.remove(card)
            self._review.append(card)
        elif card in self._review:
            self._review.remove(card)
            self._learn.append(card)
        else:  # assume! card in _learn
            pass  # already at the bottom
        self.print_sizes()


def test_picks(deck: "Deck") -> None:
    """Run basic selection tests with a given deck.

    Args:
            deck: The Deck object to test with.
    """
    pb = ProbBucket(deck.cards)
    print("\n1 question only")
    print(pb.pick_card())
    print("\n1 question and two answers")
    a, b, c = pb.pick_3_cards()
    print(f"Question: {a}")
    print("then two wrong answers: ")
    print(b)
    print(c)


if __name__ == "__main__":
    from .models import load_deck_from_json_file

    dk = load_deck_from_json_file("deck_data.json")
    if dk:
        test_picks(dk)
