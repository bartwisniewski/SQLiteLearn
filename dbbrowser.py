import sqlite3


class Database:
    def __init__(self, path):
        self.con = sqlite3.connect(path)

    def create_table(self):
        query = "CREATE TABLE IF NOT EXISTS Customers(id INTEGER PRIMARY KEY, " \
                "name TEXT NOT NULL, surname TEXT NOT NULL, date_joined DATE NOT NULL);"
        self.con.execute(query)

    def add_to_customers(self, name, surname, date_joined):
        query = "INSERT INTO Customers(name, surname, date_joined) VALUES(?, ?, ?)"
        self.con.execute(query, (name, surname, date_joined))

    def delete_from_customers(self, customer_id):
        query = "DELETE FROM Customers WHERE ID =  ?"
        self.con.execute(query, (customer_id,))

    def clear(self):
        query = "DELETE FROM Customers"
        self.con.execute(query)

    def update_customer(self, customer_id, **kwargs):

        if len(kwargs) == 0:
            return

        query_params = list(kwargs.values())
        query_params.append(customer_id)

        update_fields = ""
        for key in kwargs:
            update_fields += f" {key} = ?,"
        update_fields = update_fields[:-1]

        query = f"UPDATE Customers SET{update_fields} WHERE ID = ?"

        self.con.execute(query, tuple(query_params))

    def preview_table(self, table_name):
        query = f"SELECT * FROM {table_name}"
        results = self.con.execute(query).fetchall()
        print(results)

    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        if isinstance(exc_value, Exception):
            self.con.rollback()
        else:
            self.con.commit()

        self.con.close()


with Database('example2-data') as db:
    db.create_table()
    db.add_to_customers('John', 'Wick', '2000-09-02')
    db.add_to_customers('James', 'Bond', '2002-05-16')
    db.preview_table('Customers')

    db.update_customer(1, date_joined='2008-10-11')
    db.update_customer(2, name="Winnie", surname="The Pooh")
    db.preview_table('Customers')

    db.delete_from_customers(1)
    db.preview_table('Customers')

    db.clear()
