from menu import ConsoleMenu
from db_handler import NotepadDB


class NotepadManager:
    SELECTIONS = ["add", "delete", "display", "exit"]
    DB_PATH = 'notepad.db'

    def __init__(self) -> None:
        self.menu = ConsoleMenu()
        self.is_running = True
        with NotepadDB(NotepadManager.DB_PATH) as db:
            db.init_db()
        self.main_menu()

    def main_menu(self) -> None:
        while self.is_running:
            selection = self.menu.select(description="What would you like to do?", selections=NotepadManager.SELECTIONS)
            self.__call_selection(selection)

    def __call_selection(self, selection: int) -> None:
        sel_methods = [self.__add, self.__delete, self.__display, self.__exit]
        sel_methods[selection]()

    def __add(self) -> None:
        title = self.menu.get_text("note title:")
        content = self.menu.get_text("note content:")
        with NotepadDB(NotepadManager.DB_PATH) as db:
            db.add_note(title, content)

    def __delete(self) -> None:
        title = self.menu.get_text("note to delete title:")
        with NotepadDB(NotepadManager.DB_PATH) as db:
            db.delete_note(title)

    @staticmethod
    def __display() -> None:  # TEST
        with NotepadDB(NotepadManager.DB_PATH) as db:
            notes = db.get_notes()
        print("title | content | created")

        for note in notes:
            print(f"{note[1]}| {note[2]} | {note[3]}")

        if not notes:
            print("-- table empty --")

    def __exit(self) -> None:
        print("exiting")
        self.is_running = False
