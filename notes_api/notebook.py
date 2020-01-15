class Notebook():
    def __init__(self, notes=[]):
        self._notes = notes
        self.tags = {}
        self._update_tags()

    def __eq__(self, notebook):
        try:
            is_eq = True
            for i, _ in enumerate(self._notes):
                is_eq = is_eq and (self._notes[i] == notebook._notes[i])
        except IndexError:
            is_eq = False

        return is_eq

    def __ne__(self, notebook):
        return not self.__eq__(notebook)

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, notes):
        self._notes = notes
        self._update_tags()

    def _update_tags(self):
        tags = set()
        for note in self._notes:
            tags = tags.union(note.tags)

        self.tags = tags

    def sync(self, synchronizer):
        synchronizer.sync(self)

    def reorder(self, swap_indexes):
        try:
            note_0 = self._notes[swap_indexes[0]].duplicate()
            note_1 = self._notes[swap_indexes[1]].duplicate()
            self._notes[swap_indexes[0]] = note_1
            self._notes[swap_indexes[1]] = note_0
        except IndexError as e:
            raise IndexError("The indexes are out of bound") from e

    def add_notes(self, notes):
        if isinstance(notes, list):
            self._notes += notes
        else:
            self._notes.append(notes)

        self._update_tags()

    def remove_notes(self, indexes_note):
        if isinstance(indexes_note, list):
            self._notes = [self._notes[i] for i in range(len(self._notes)) \
                           if i not in indexes_note]
        else:
            self._notes.pop(indexes_note)

        self._update_tags()

    def display(self, displayer):
        for note in self._notes:
            note.display(displayer)
