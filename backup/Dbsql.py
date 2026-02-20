"""
SQLite with archived file metadata
"""

import sqlite3

class Dbsql:

    def __init__(self, dbpath):
        """
        Initialize sql database
        """
        self.dbpath = dbpath
        self.conn = sqlite3.connect(
            dbpath,
            detect_types=sqlite3.PARSE_DECLTYPES |
            sqlite3.PARSE_COLNAMES)
        cursor = self.conn.cursor()
        try:
            # Create table
            cursor.executescript("""
                CREATE TABLE IF NOT EXISTS metadata(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filePath TEXT NOT NULL,
                    fileName TEXT NOT NULL,
                    fileSize INTEGER NOT NULL,
                    fileModified TIMESTAMP NOT NULL, 
                    fileHash,
                    occurrence
                ); 
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error: in SQL CREATE TABLE" + e.args[0])
        pass

    # context manager ========

    def __enter__(self):
        """
        context manager: begin session
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        context manager: end of session
        """
        # close connection
        self.conn.close()

    # common functions ========

    def get_row(self, row_id):
        """
        Select record from database table metadata
        """
        sql = "SELECT id, filePath, fileName, fileSize, fileModified, fileHash, occurrence FROM metadata WHERE id = ?;"
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (row_id,))
            return cursor.fetchall() # success
        except sqlite3.Error as e:
            print("SQLite SELECT TABLE metadata error occurred:" + e.args[0])
        return [] # failed

    def set_row(self, file_path, file_name, file_size, file_modified, file_hash=None, occurrence=None):
        """
        Insert record into database table metadata
        """
        sql = "INSERT INTO metadata(filePath, fileName, fileSize, fileModified, fileHash, occurrence) VALUES (?, ?, ?, ?, ?, ?);"
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (file_path, file_name, file_size, file_modified, file_hash, occurrence))
            self.conn.commit()
            return cursor.lastrowid # success
        except sqlite3.Error as e:
            print("SQLite INSERT TABLE metadata error occurred:" + e.args[0])
        return None # failed

    def update_hash_plus(self, id, hash, occurrence):
        """
        Update the hash in row with id=id
        """
        sql = "UPDATE metadata SET fileHash=?, occurrence=? WHERE id=?;"
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (hash, occurrence, id))
            self.conn.commit()
            return cursor.rowcount
        except sqlite3.Error as e:
            print("SQLite UPDATE TABLE metadata error occurred:" + e.args[0])
            raise Exception("Fatal SQLite error occurred")

    def del_rows(self):
        """
        Delete all records in table metadata
        """
        sql = "DELETE FROM metadata;"
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            return cursor.rowcount # success
        except sqlite3.Error as e:
            print("SQLite DELETE TABLE metadata error occurred:" + e.args[0])
        return None

    def get_duplicate_files(self):
        """
        Get all duplicate filenames in database table metadata
        """
        sql = "SELECT fileName, fileSize, COUNT(*) c FROM metadata GROUP BY fileName, fileSize HAVING c > 1;"
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print("SQLite SELECT duplicate_filenames error occurred:" + e.args[0])
        return []

    def get_duplicate_rows(self, file_name):
        """
        Get duplicate rows from database table metadata with same 'filename'
        """
        sql = "SELECT * FROM metadata WHERE fileName=? ORDER BY fileModified ASC;"
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (file_name,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print("SQLite SELECT duplicate_rows error occurred:" + e.args[0])
        return []

# main ========

if __name__ == '__main__':
    print("The SQL class module shall not be invoked on it's own.")
