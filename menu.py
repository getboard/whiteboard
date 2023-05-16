import tkinter


class Menu:
    _menubar: tkinter.Menu  # field to add menu items
    _current_state: str

    MENU_ROOT_STATE = 'select'

    def __init__(self, root: tkinter.Tk):
        self._menubar = tkinter.Menu(root)
        # by default, we add select
        self._menubar.add_command(
            label=self.MENU_ROOT_STATE,
            command=lambda: self.set_selected_state(self.MENU_ROOT_STATE),
        )
        self.set_root_state()
        root.config(menu=self._menubar)

    @property
    def current_state(self):
        return self._current_state

    def set_root_state(self):
        self._current_state = self.MENU_ROOT_STATE

    def add_command_to_menu(self, name: str):
        self._menubar.add_command(label=name, command=lambda: self.set_selected_state(name))

    def set_selected_state(self, name: str):
        if self._current_state == name:
            self.set_root_state()
        else:
            self._current_state = name
