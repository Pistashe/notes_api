class Displayer():
    """
    Interface that must be implemented to correctly handle the display of a
    note.
    """

    def display(self, note):
        """
        Handles the way a note is displayed to the user.
        """
        if note._type == "tick":
            self._display_tick_note(note)
        elif note._type == "plain":
            self._display_plain_note(note)

    def _display_plain_note(self, note):
        """
        Handles the way a plain note is displayed to the user.
        """
        raise NotImplementedError("The function display_plain_note has not "\
                                  "been implemented.")

    def _display_tick_note(self, note):
        """
        Handles the way a tick note is displayed to the user.
        """
        raise NotImplementedError("The function display_tick_note has not "\
                                  "been implemented.")
