import os
import json
import shutil

from notes_api.exceptions import DecryptionError
from notes_api.note import Note

CWD = os.getcwd()

class Notebook():
    def __init__(self, notes=[]):
        self._notes = notes
        self.tags = {}
        self._update_tags()

    def __eq__(self, notebook):
        if len(self._notes) != len(notebook._notes):
            return False

        for i, _ in enumerate(self._notes):
            if self._notes[i] != notebook._notes[i]:
                return False

        return True

    def __ne__(self, notebook):
        return not self.__eq__(notebook)

    @classmethod
    def from_archive(self, archive_path, encrypter=None):
        try:
            shutil.unpack_archive(archive_path, "tmp_archive/")
            os.chdir("tmp_archive")
            with open("notebook_infos.json") as file_:
                notebook_infos = json.load(file_)

            notes = [Note.from_file(id_, encrypter) \
                     for id_ in notebook_infos["order"]]
        except (shutil.ReadError, FileNotFoundError):
            raise FileNotFoundError("Archive not found.")
        finally:
            os.chdir("../")
            shutil.rmtree("tmp_archive", ignore_errors=True)

        return Notebook(notes)

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

    def save(self, encrypter=None):
        os.mkdir("tmp_archive")
        os.chdir("tmp_archive")

        notebook_infos = {"order": [note._id for note in self._notes]}
        with open("notebook_infos.json", "w") as file_:
            json.dump(notebook_infos, file_)

        for note in self._notes:
            note.save(encrypter=encrypter)

        os.chdir("../")
        shutil.make_archive("notebook_archive", "tar", "tmp_archive")
        print("ok")
        shutil.rmtree("tmp_archive")
