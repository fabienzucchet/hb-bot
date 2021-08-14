"""Manage connection with sqlite3 database."""
from sqlalchemy import create_engine
from sqlalchemy import Table, MetaData, Column, String, Integer, ForeignKey

from config import database_path

SQLITE = "sqlite"

PEOPLE = "people"
SUBSCRIPTIONS = "subscriptions"


class HBDatabase:
    # http://docs.sqlalchemy.org/en/latest/core/engines.html
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}'
    }

    # Main DB Connection Ref Obj
    db_engine = None

    def __init__(self, dbtype, username='', password='', dbname=''):
        dbtype = dbtype.lower()
        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
            self.db_engine = create_engine(engine_url)
            print(self.db_engine)
        else:
            print("DBType is not found in DB_ENGINE")

    def create_db_tables(self):
        metadata = MetaData()
        people = Table(
            PEOPLE,
            metadata,
            Column("login", String, primary_key=True),
            Column("first_name", String),
            Column("last_name", String),
            Column("birth_year", Integer),
            Column("birth_month", Integer),
            Column("birth_day", Integer)
        )
        subscriptions = Table(
            SUBSCRIPTIONS,
            metadata,
            Column("chan_id", String, primary_key=True),
            Column("login", String, ForeignKey("people.login"))
        )
        try:
            metadata.create_all(self.db_engine)
            print("Tables created")
        except Exception as e:
            print("Error occurred during Table creation!")
            print(e)

    # Insert, Update, Delete
    def execute_query(self, query=''):
        if query == '':
            return
        print(query)
        with self.db_engine.connect() as connection:
            try:
                connection.execute(query)
            except Exception as e:
                print(e)

    # Select
    def execute_select_query(self, query=None):
        if query == '':
            return
        print(query)
        with self.db_engine.connect() as connection:
            try:
                cursor = connection.execute(query)

            except Exception as e:
                print(e)

            else:
                results = [row for row in cursor]
                cursor.close()

                return results


if __name__ == '__main__':

    db = HBDatabase(SQLITE, dbname=database_path)

    # Table creation
    db.create_db_tables()

    # Insert query
    query = "INSERT INTO people (login, first_name, last_name, birth_year, birth_month, birth_day) VALUES ('login', 'FirstName', 'LastName', 1999, 1, 1);"
    db.execute_query(query)

    # Select query
    select_query = "SELECT * FROM people;"
    res = db.execute_select_query(select_query)
    print(res)
