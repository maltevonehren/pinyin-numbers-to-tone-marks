from anki.notes import Note
from anki.collection import SearchNode
from aqt import gui_hooks, mw
from aqt.utils import showInfo, qconnect
from aqt.qt import *

from .pinyin_util import *


def transform_all() -> None:
    current = mw.col.decks.current()
    ids = mw.col.find_notes(mw.col.build_search_string(SearchNode(deck=current['name'])))
    num_changed = 0
    for id in ids:
        note: Note = mw.col.get_note(id)
        for (field, value) in note.items():
            if 'pinyin' in field.lower():
                new_value = pinyin_numbers_to_marks(value)
                if new_value != value:
                    note[field] = new_value
                    num_changed += 1
                    mw.col.update_note(note)
    showInfo(f"Updated {num_changed} entries")


def on_editor_did_unfocus_field(changed: bool, note: Note, current_field: int):
    (field, value) = note.items()[current_field]
    if 'pinyin' in field.lower():
        new_value = pinyin_numbers_to_marks(value)
        if new_value != value:
            note[field] = new_value
            changed = True
    return changed


gui_hooks.editor_did_unfocus_field.append(on_editor_did_unfocus_field)
action = QAction("pin1yin1 → pīnyīn: apply to active deck", mw)
qconnect(action.triggered, transform_all)
mw.form.menuTools.addAction(action)
