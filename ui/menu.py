"""
Generic terminal menu navigation.

A :class:`Menu` pairs a display function (which draws a screen and returns the
user's raw choice) with a table of ``(aliases, action)`` entries. It runs the
same navigation loop every submenu used to hand-code: dispatch the chosen
action, or handle back / exit / invalid input identically. This removes the
duplicated ``handle_*_menu`` boilerplate without changing any on-screen output.
"""

import time

from ui.console import wprint


class Menu:
    """A submenu screen plus its choice-to-action dispatch table."""

    def __init__(self, display, entries):
        """
        Args:
            display: Callable that renders the menu and returns the raw choice.
            entries: List of ``(aliases, action)`` pairs, where ``aliases`` is a
                tuple of accepted strings and ``action`` is a zero-arg callable.
        """
        self.display = display
        self.entries = entries

    def run(self, app):
        """Loop until the user goes back, or exits (which stops the whole app)."""
        while app.running:
            choice = self.display()
            choice = choice.lower().strip()

            for aliases, action in self.entries:
                if choice in aliases:
                    action()
                    break
            else:
                if choice in ("b", "back"):
                    break
                elif choice in ("e", "exit", "q", "quit"):
                    app.running = False
                    break
                else:
                    wprint(f"Invalid option: {choice}")
                    time.sleep(1)
