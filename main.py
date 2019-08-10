import sqlite3

connector = sqlite3.connect("address_book.db")


def setup_db(connector):
    connector.executescript(
        """
        DROP TABLE IF EXISTS contacts;

        CREATE TABLE contacts(
        NAME         TEXT            NOT NULL,
        SURNAME      TEXT            NOT NULL,
        PHONE        TEXT            NOT NULL,
        EMAIL        TEXT,       
        AGE          INT
        );
        """
    )


def add_contact(connector, name, surname, phone, email=None, age=None):
    query = """
        INSERT INTO contacts
        VALUES (?, ?, ?, ?, ?)
        """

    data = (name, surname, phone, email, age)    

    connector.execute(query, data)
    connector.commit()
    print(f"You added {data} to your contacts")


setup_db(connector)

add_contact(connector, "Karl", "Marx", "089123445", "karl.marx@posteo.de", 40)

# connector.execute(
#     """
#     INSERT INTO contacts
#     VALUES (?, ?, ?, ?, ?)
#     """,
#     karl_marx,
# )
# It is necessary to commit after each insert!
# connector.commit()
