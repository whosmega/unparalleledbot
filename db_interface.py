import sqlite3
import time

class db_interface:
    base = None

    def __init__(self, dbname):
        self.base = sqlite3.connect(dbname)
        if not self.base:
            print("An error occured while connecting to database")

        
    def new_entry(self, table=None, key=None, keyfield=None, value=None, valuefield=None):
        self.base.execute(f"INSERT INTO {table} ({keyfield},{valuefield})\
                            VALUES ({key},{value});")
        self.base.commit()
        
    def update_entry(self, table=None, update=None, key=None, keyfield=None, updatefield=None):
        exists = self.base.execute(f"SELECT EXISTS(\
                                     SELECT {keyfield}\
                                     FROM {table}\
                                     WHERE {keyfield} = {key}\
                                     );")
                                    


        if exists.fetchone()[0] == 0:
            self.new_entry(table=table, key=key, value=update, keyfield=keyfield, valuefield=updatefield)
            return
        exists.close()
        self.base.execute(f"UPDATE {table} SET {updatefield} = {update}\
                            WHERE {keyfield} = {key};")
        self.base.commit()

    def get_entry(self, table=None, key=None, keyfield=None, value=None, valuefield=None):
        exists = self.base.execute(f"SELECT EXISTS(\
                                     SELECT {keyfield}\
                                     FROM {table}\
                                     WHERE {keyfield} = {key}\
                                     );")


        if exists.fetchone()[0] == 0:
            self.new_entry(table=table, key=key, keyfield=keyfield, value=value, valuefield=valuefield)
            return 0
        exists.close()
        cursor = self.base.execute(f"SELECT {valuefield}\
                                    FROM {table}\
                                    WHERE {keyfield} = {key};")
        cash = cursor.fetchone()[0]
        cursor.close()
        return cash
            

        

    def get_leaderboard(self, getfields=None, sortfields=None, table=None, limit=1):
        leaderboard_cursor = self.base.execute(f"SELECT {getfields}\
                                                     FROM {table}\
                                                     ORDER BY {sortfields} DESC \
                                                     LIMIT {limit};")
        return leaderboard_cursor.fetchall()

    def close(self):
        self.base.close()

        



    
        
        