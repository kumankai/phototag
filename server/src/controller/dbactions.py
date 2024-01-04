"""
MODULE contains functions for database queries
"""

import sqlite3

connection = sqlite3.connect("database.db", check_same_thread=False)
cursor = connection.cursor()


def checktable(table):
    """
    Checks if a table exists in database
    table: string
    return: List || None
    """
    cursor.execute(
        f"SELECT name FROM SQLITE_MASTER WHERE TYPE='table' AND NAME='{table}'"
    )
    result = cursor.fetchone()
    return result is not None


def createtable():
    """
    Initialize tables
    return: None
    """
    if not checktable("images"):
        cursor.execute(
            """
            CREATE TABLE images (
            imageID INTEGER PRIMARY KEY,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            filename)
            """
        )
        print("\nimages table created")

    if not checktable("tags"):
        cursor.execute(
            """
            CREATE TABLE tags (
            imageID INTEGER,
            tag,
            FOREIGN KEY(imageID) REFERENCES IMAGES(imageID))
            """
        )
        print("\ntags table created")

    connection.commit()


def saveimage(file, tags):
    """
    Saves image in database
    file: string
    tags: List
    return: None
    """
    cursor.execute(f"INSERT INTO images (filename) VALUES ('{file}')")

    id = cursor.execute(
        f"SELECT imageID FROM IMAGES WHERE FILENAME='{file}'"
    ).fetchall()[0][0]

    for tag in tags:
        cursor.execute(f"INSERT INTO tags VALUES ('{id}', '{tag}')")

    connection.commit()


def getTags(from_date, to_date):
    """
    Grabs tags between a period of time
    from_date: string
    to_date: string
    return: List
    """
    data = cursor.execute(
        f"""
        SELECT t.tag
        FROM tags t
        JOIN images i ON t.imageID = i.imageID
        WHERE i.timestamp BETWEEN '{from_date}' AND '{to_date}
        '"""
    ).fetchall()

    res = [tag[0] for tag in data]
    return res


def detectppl(from_date, to_date):
    """
    Grabs any human presence tag in database
    from_date: string
    to_date: string
    return: Bool
    """
    total_detectedppl_tag = cursor.execute(
        f"""
        SELECT COUNT(*)
        FROM tags t
        JOIN images i ON t.imageID = i.imageID
        WHERE t.tag IN (
            'person',
            'human',
            'people'
        )
        AND i.timestamp BETWEEN '{from_date}' AND '{to_date}'
        """
    ).fetchone()[0]

    return True if total_detectedppl_tag > 0 else False


def getpopular():
    """
    Gets five most popular tags in database
    return: List
    """
    topfive = cursor.execute(
        f"""
        SELECT tag, COUNT(*) AS tag_count
        FROM tags
        GROUP BY tag
        ORDER BY tag_count DESC
        LIMIT 5
        """
    ).fetchall()

    return topfive
