import mysql.connector
from mysql.connector import errorcode

class Database():
    def __init__(self):
        self.current_fname = ""

    def connect(self):
        try:
            cnx = mysql.connector.connect(
                host="localhost",
                user="root",
                password="password"
            )
            return cnx
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                return False
            else:
                return False
            
    def create_database(self): # Create
        """creates database and table"""
        cnx = self.connect()

        if cnx:
            cursor = cnx.cursor()

            cursor.execute("CREATE DATABASE IF NOT EXISTS text_editor")
            cursor.execute("USE text_editor")
            cursor.execute("CREATE TABLE IF NOT EXISTS Text_Data(filename varchar(255), content text(65535))")
            
            cursor.close()
            cnx.close()
        else:
            pass

    def get_fnames(self) -> list:
        """Get 'filenames' from database"""
        cnx = self.connect()

        if cnx:
            cursor = cnx.cursor()
            cursor.execute("USE text_editor")

            # create list of filenames to access specific file
            cursor.execute("SELECT filename FROM Text_Data")
            results = cursor.fetchall()
            values = [row[0] for row in results]

            if values:
                return values
            
            cursor.close()
            cnx.close()
        else:
            pass

    def get_val_from_fname(self, fname) -> str: # Read
        """Get content of filename in database

        Args:
            fname (str): File name from option menu

        Returns:
            str: content of the file
        """
        cnx = self.connect()
        if cnx:
            cursor = cnx.cursor()
            cursor.execute("USE text_editor")

            # select content using filename
            query = "SELECT t1.content FROM Text_Data t1 WHERE t1.filename = %s"
            self.current_fname = fname

            cursor.execute(query, (fname,))

            result = cursor.fetchone()

            if result:
                # iterate over tuple to return string
                for content in result:
                    return content
            
            cursor.close()
            cnx.close()
        else:
            pass

    def save_to_db(self, filename, text): # Update
        """saves the filename and content to database"""
        cnx = self.connect()

        if cnx:
            cursor = cnx.cursor()
            cursor.execute("USE text_editor")
            
            query = "INSERT INTO Text_Data (filename, content) VALUES (%s, %s)"
            values = (filename, text)

            cursor.execute(query, values)

            cnx.commit()

            cursor.close()
            cnx.close()
        else:
            pass

    def del_from_tbl(self, fname): # Delete
        """Delete column using filename"""
        cnx = self.connect()
        if cnx:
            cursor = cnx.cursor()
            cursor.execute("USE text_editor")
            
            query = "DELETE FROM Text_Data WHERE filename = %s"
            cursor.execute(query, (fname,))

            cnx.commit()

            cursor.close()
            cnx.close()
        else:
            pass