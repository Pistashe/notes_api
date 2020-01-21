from colorama import Fore, Back, Style

from .displayer import Displayer

class DisplayerAscii(Displayer):
    def _display_plain_note(self, note):
        msg = self._get_header(note)
        msg += note.content
        msg += Style.RESET_ALL + "\n"

        print(msg)

    def _display_tick_note(self, note):
        msg = self._get_header(note)
        for item in note.content:
            box = "[x] " if item["ticked"] else "[ ] "
            msg += box + item["text"] + "\n"
        msg += Style.RESET_ALL + "\n"

        print(msg)

    def _get_header(self, note):
        header = self._translate_color(note.color)
        header += note.title + "\n"
        header += "="*len(note.title) + "\n"
        header += "".join(["#{} ".format(tag) for tag in note.tags])
        header += "\n\n"
        return header

    def _translate_color(self, color_note):
        return getattr(Fore, color_note.upper())
