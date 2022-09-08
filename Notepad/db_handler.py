import sqlite3


class NotepadDB:
    def __init__(self, path):
        self.con = sqlite3.connect(path)

    def init_db(self):
        print("initialising")
        query = "CREATE TABLE IF NOT EXISTS Notes(" \
                "id INTEGER PRIMARY KEY, " \
                "title TEXT NOT NULL, " \
                "content TEXT NOT NULL, " \
                "timestamp DATE NOT NULL DEFAULT CURRENT_TIMESTAMP);"
        self.con.execute(query)

    def add_note(self, title, content):
        query = "INSERT INTO Notes(title, content) VALUES(?, ?)"
        self.con.execute(query, (title, content))

    def delete_note(self, title):
        query = "DELETE FROM Notes WHERE title =  ?"
        self.con.execute(query, (title,))

    def get_notes(self):
        query = f"SELECT * FROM Notes"
        results = self.con.execute(query).fetchall()
        return results

    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        if isinstance(exc_value, Exception):
            self.con.rollback()
        else:
            self.con.commit()

        self.con.close()
