from colorama import Fore, Style

from .displayer import Displayer

class DisplayerAscii(Displayer):
    def display(self, note):
        msg = self._translate_color(note.color)
        msg += note.title + "\n"
        msg += "="*len(note.title) + "\n"
        msg += "".join(["#{} ".format(tag) for tag in note.tags])
        msg += "\n\n"
        msg += note.content
        msg += Style.RESET_ALL + "\n"

        print(msg)

    def _translate_color(self, color_note):
        return getattr(Fore, color_note.upper())
