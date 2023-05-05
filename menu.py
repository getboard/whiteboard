import tkinter


class Menu:
    _menubar: tkinter.Menu  # field to add menu items
    _current_state: str

    def __init__(self, root: tkinter.Tk):
        self._menubar = tkinter.Menu(root)
        # by default, we add select
        self._menubar.add_command(label='select')
        self.make_root_state()
        root.config(menu=self._menubar)

    @property
    def current_state(self):
        return self._current_state

    def make_root_state(self):
        self._current_state = 'select'

    def add_command_to_menu(self, name: str):
        self._menubar.add_command(label=name, command=lambda: self.make_selected_state(name))

    def make_selected_state(self, name: str):
        if self._current_state == name:
            self.make_root_state()
        else:
            self._current_state = name
