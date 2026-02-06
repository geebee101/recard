import random

class ProbBucket:
    LIMIT = 3000 # memory is limited, older known words might be removed to make space
    def __init__(self, aList = None):
        self._known = list()
        self._review = list()
        if aList:
            self._learn = aList.copy()
        else:
            self._learn = list()
        self.print_sizes()
        self._current_card = None

    def get_current_card(self):
        if not self._current_card: 
            self._current_card = self.pick_card()
        return self._current_card

    def print_sizes(self):
        #print('known (leftside) size:', len(self._known))
        #print('to review (middle) size:', len(self._review))
        #print('to learn (rightside) size:', len(self._learn))
        print(f'known {len(self._known)} ——— review {len(self._review)} ——— learn {len(self._learn)}')

    def add_cards(self, aList): # PB exists already, simplified method for demo
        self._learn.extend(aList)
        self.print_sizes()
        return self

    def pick_card(self, exclude=None):
        if not self._learn:
            if not self._review:
                if not self._known:
                    print('ERROR no cards')
                    return None
                else:
                    probs = [100, 0, 0]
            else: # have review
                if not self._known:
                    probs = [0, 100, 0]
                else:
                    probs = [30, 70, 0]
        else: # have learn
            if not self._review:
                if not self._known:
                    probs = [0, 0, 100]
                else:
                    probs = [30, 0, 70]
            else: # have review
                if not self._known:
                    probs = [0, 30, 70]
                else:
                    probs = [10, 20, 70]
        print(probs)
        return self._pick(probs)

    def _pick(self, probs, exclude = None):
        # Choose one collection based on weights
        chosen_collection = random.choices([self._known , self._review, self._learn], weights=probs, k=1)[0]
        print('Chosen collection size: ', len(chosen_collection))
        # Choose an item from the chosen collection
        picked = random.choice(chosen_collection)

        if exclude and picked in exclude:
            return self._pick(probs, exclude) # TODO edge case if we don't have enough cards (prevents deck save if less than 3???)
        print(picked)
        self._current_card = picked
        return picked

    def pick_3_cards(self): # question + 2 incorrect answers
        q = self.pick_card()
        a1 = self.pick_card([q])
        a2 = self.pick_card([q, a1])
        return q, a1, a2

    def _forget(self):
        if len(self._known()) == 0:
            print('ERROR: memory full, cannot add new word(s)')
            return
        to_forget = self._pick([100,0,0]) # select from words that have been mastered
        self._known.remove(to_forget)
        return

    def forget_known(self):
        " confirmations are the UI job"
        self._known = list()

    def forget_all(self):
        " confirmations are the UI job"
        self._known = list()
        self._review = list()
        self._learn = list()

    def x_add_cards(self, cards):
        """We could be more efficient adding one by one, but we want an all or nothing here.
        Because from a user viewpoint it is 'adding a new deck.'
        """
        lk = len(self._known)
        lr = len(self._review)
        ll = len(self._learn)
        ln = len(cards)
        if lk+lr+ll+ln >= LIMIT: # need more space
            if ln > lk:
                print('ERROR: too many new words')
                return
            if lk <= (lk+lr+ll+ln - LIMIT):
                print('ERROR: too many new words')
                return
            for i in range(lk+lr+ll+ln - LIMIT):
                self._forget()
        self._learn.extend(cards)

    def promote(self, aCard, high = False):
        self.print_sizes()
        if aCard in self._known:
            pass # nothing to do, already at top
        elif aCard in self._review:
            self._review.remove(aCard)
            self._known.append(aCard)
        else: # assume! card in _learn
            self._learn.remove(aCard)
            if high:
                self._known.append(aCard)
            else:
                self._review.append(aCard)
        self.print_sizes()

    def demote(self, aCard):
        self.print_sizes()
        if aCard in self._known:
            self._known.remove(aCard)
            self._review.append(aCard)
        elif aCard in self._review:
            self._review.remove(aCard)
            self._learn.append(aCard)
        else: # assume! card in _learn
            pass # already at the bottom
        self.print_sizes()


# end class


#########################################
# self tests
def test_picks(aDeck):
    pb = ProbBucket(aDeck.cards)
    print()
    print('1 question only')
    print(pb.pick_card())
    print()
    print('1 question and two answers')
    a, b, c = pb.pick_3_cards()
    print('Question: ', b, c)
    print('then two wrong answers: ')
    print(b)
    print(c)

if __name__ == '__main__':
    from models2 import Deck, Lexicard, load_deck_from_json_file
    dk = load_deck_from_json_file('deck_data.json')
    test_picks(dk)

"""
BEST PRACTICES FOR DECK MAKERS
While there is no technical limitation on deck size we recommend that you do not create a deck of more than a few hundred cards.
e.g. do not publish: 'The 5,000 most common words'. Prefer instead the following style: 'Frequency list XYZ: words 251-500.' Or '100 words for business,' 'Sport in the news: 200 words.'
Do not publish decks where only some entries have audio.
Do not publish decks with audio generated by an LLM, which has not been reviewed by a native speaker.
With scripts that differ from latin, use only transcription systems that are widely accepted by the community. Do not invent a new one. Do not generate transcription with an LLM, as they don't stick correctly to one system.
TODO add varirable to deck: transcription_system
"""

# end file