import sqlite3
import models

DB: str = "database.db"


def create_tables():
    with sqlite3.connect(DB) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""CREATE TABLE IF NOT EXISTS Auth (
                    id                  INTEGER PRIMARY KEY,
                    password            TEXT NOT NULL
                )""")
            cursor.execute("""CREATE TABLE IF NOT EXISTS Users (
                    id                  INTEGER PRIMARY KEY,
                    name                TEXT NOT NULL,
                    avatar              TEXT,
                    description         TEXT,
                    github_url          TEXT NOT NULL
                )""")
            cursor.execute("""CREATE TABLE IF NOT EXISTS Packages (
                    name            TEXT PRIMARY KEY,
                    author_id       INTEGER NOT NULL,
                    github_url      TEXT NOT NULL,
                    avatar          TEXT,
                    FOREIGN KEY (author_id) REFERENCES Users(id)
                )""")
            cursor.execute("""CREATE TABLE IF NOT EXISTS Releases (
                    package_name            TEXT,
                    version                 TEXT NOT NULL,
                    contributor_id          INTEGER NOT NULL,
                    description             TEXT,
                    date                    INTEGER,
                    downloads               INTEGER,
                    FOREIGN KEY (package_name) REFERENCES Packages(name),
                    FOREIGN KEY (contributor_id) REFERENCES Users(id)
                )""")
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")


def add_auth(password: str) -> int:
    try:
        with sqlite3.connect(DB) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO Auth (password) VALUES (?)",
                (password,)
            )
            connection.commit()
            return cursor.lastrowid
    except Exception as e:
        print(f"Error occurred while adding Auth: {e}")
    finally:
        connection.close()


def check_auth(_id: int, password: str) -> bool:
    try:
        with sqlite3.connect(DB) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM Auth WHERE id = ?, password = ?",
                (_id, password)
            )
            user_data = cursor.fetchone()
            if user_data:
                return True
            return False
    except sqlite3.Error as e:
        return False
    finally:
        connection.close()


def get_user(_id: int) -> models.User | models.Error:
    try:
        # gets user from sqlite3 database
        with sqlite3.connect(DB) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM Users WHERE id = ?",
                (_id,)
            )
            user_data = cursor.fetchone()
            if user_data:
                user = models.User(*user_data)
                return user
            return models.Error(404, "No such user in database")
    except sqlite3.Error as e:
        return models.Error(404, "Not expected error")
    finally:
        connection.close()


def get_package(name: str) -> models.Package | models.Error:
    try:
        # gets package from sqlite3 database
        with sqlite3.connect(DB) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM Packages WHERE name = ?",
                (name,)
            )
            package_data = cursor.fetchone()
            if package_data:
                package = models.Package(*package_data)
                return package
            return models.Error(404, "No such package in database")
    except sqlite3.Error as e:
        return models.Error(404, "Not expected error")
    finally:
        connection.close()


def get_release(package_name: str, version: str) -> models.Release | models.Error:
    try:
        # gets release from sqlite3 database
        with sqlite3.connect(DB) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM Releases WHERE package_name = ?, version = ?",
                (package_name, version)
            )
            release_data = cursor.fetchone()
            if release_data:
                release = models.Release(*release_data)
                return release
            return models.Error(404, "No such release in database")
    except sqlite3.Error as e:
        return models.Error(404, "Not expected error")
    finally:
        connection.close()


def get_last_release(package_name: str) -> models.Release | models.Error:
    try:
        # gets last release from sqlite3 database
        with sqlite3.connect(DB) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT *
                FROM Releases
                WHERE package_name = ?
                ORDER BY CAST(SUBSTR(version_text, 1, INSTR(version_text || '.', '.') - 1) AS INTEGER) DESC,
                         CAST(SUBSTR(version_text, INSTR(version_text || '.', '.') + 1, INSTR(SUBSTR(version_text || '.', INSTR(version_text || '.', '.') + 1) || '.', '.') - 1) AS INTEGER) DESC,
                         CAST(SUBSTR(version_text, INSTR(SUBSTR(version_text || '.', INSTR(version_text || '.', '.') + 1) || '.', INSTR(SUBSTR(version_text || '.', INSTR(version_text || '.', '.') + 1) || '.', '.') + 1)) AS INTEGER) DESC
                LIMIT 1
                """,
                (package_name,)
            )
            release_data = cursor.fetchone()
            if release_data:
                release = models.Release(*release_data)
                return release
            return models.Error(404, "No such release in database")
    except sqlite3.Error as e:
        return models.Error(404, "Not expected error")
    finally:
        connection.close()


def add_user(_id: int, name: str, avatar: str, description: str, github_url: str):
    try:
        with sqlite3.connect(DB) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO Users (id, name, avatar, description, github_url) VALUES (?, ?, ?, ?, ?)",
                (_id, name, avatar, description, github_url)
            )
            connection.commit()
    except Exception as e:
        print(f"Error occurred while adding user: {e}")
    finally:
        connection.close()


def add_package(name: str, author_id: int, github_url: str, avatar: str):
    try:
        # adds package to sqlite3 database
        with sqlite3.connect(DB) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO Packages (name, author_id, github_url, avatar) VALUES (?, ?, ?, ?)",
                (name, author_id, github_url, avatar)
            )
            connection.commit()
    except Exception as e:
        print(f"Error occurred while adding package: {e}")
    finally:
        connection.close()


def add_release(package_name: str, version: str, contributor_id: int, description: str, date: int):
    try:
        # adds release to sqlite3 database
        with sqlite3.connect(DB) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO Releases (package_name, version, contributor_id, description, date, downloads) VALUES (?, ?, ?, ?, ?, ?)",
                (package_name, version, contributor_id, description, date, 0)
            )
    except Exception as e:
        print(f"Error occurred while adding release: {e}")
    finally:
        if connection:
            connection.close()
