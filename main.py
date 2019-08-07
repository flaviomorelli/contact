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

setup_db(connector)

karl_marx = ("Karl", "Marx", "089123445", "karl.marx@gmx.de", None)

connector.execute("""
    INSERT INTO contacts
    VALUES (?, ?, ?, ?, ?)
    """, karl_marx)

# It is necessary to commit after each insert!
connector.commit()