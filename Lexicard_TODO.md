---
title: Lexicard_TODO.md
---

### LIST.TODO
1. Correct login    DONE
2. loader + save json (inc. mod Card+Deck   DONE
3. create random funcs  DONE
4. pip/poetry to uv? DONE
5. ruff DONE
6. revamp UI / cleanup / remove unused & examples DONE (scrapping old altogether rough_ONE)
7. create template DONE
8. create all pages DONE
9. backup copy >> gh commit + tag 0.1
10. rework w gem: review / doc / tests

deck capability

TODO set min w/h
TODO on mobile > doesn't appear, spaces are too big! SOLVED
TODO on mobile if items in a column are too large, they are no longer justified

what about menu disabled options?

### STYLES
# tailwind styles accross the app
header
heading
text
target_text
phonetic_text
# do we need en_text?


### NICEGUI
props are component properties (Quasar) while
classes are tailwind


NICEGUI.useful
ui.add_css
ui.add_head_html('<link 
ui.run_javascript()
ui.html()

### Marius
some rough and dirty code at XYZ
This is my first py project using uv, and I haven't finished the docs, so there is no package, yet.
It is not a proper layered web app, but a local desktop utility.
Goals were:
1- I needed a tool to practice a specific lexicon in THai (which I don't own).
2- I wanted to explore some UI-flows for recards.
3. I wanted a safe testbed for a number of new tools: uv, Antigravity, pydantic, nicegui, vue, quasar, etc.


modes
audio only th->en (reveal will reveall th/roman/en all)
audio+th->en
en->th
w or wo roman


next explore multi-choice
for now with same set
this will need an additional 'feedback' 'overlay'

next next explore multi-choice w more than one valid response

next next next
example sentences >> missing word

make deck
create or edit
edit: Editable AG Grid https://github.com/zauberzeug/nicegui/tree/main/examples/editable_ag_grid

### STATE
class State:
    def __init__(self):
        self.user_status = "Logged Out"
        self.visit_count = 0

# Create a single instance of the state to be used globally
shared_state = State()