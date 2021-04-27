import sqlite3
import time

class db_interface:
    base = None

    def __init__(self, dbname):
        self.base = sqlite3.connect(dbname)
        if not self.base:
            print("An error occured while connecting to database")

        
    def new_cash_entry(self, userid, init):
        self.base.execute(f"INSERT INTO BALANCE (USERID,CASH)\
                            VALUES ({userid},{init});")
        self.base.commit()
        
    def update_cash_entry(self, userid, new):
        exists = self.base.execute(f"SELECT EXISTS(\
                                     SELECT USERID\
                                     FROM BALANCE\
                                     WHERE USERID = {userid}\
                                     );")
                                    


        if exists.fetchone()[0] == 0:
            self.new_cash_entry(userid, new)
            return
        exists.close()
        self.base.execute(f"UPDATE BALANCE SET CASH = {new}\
                            WHERE USERID = {userid};")
        self.base.commit()

    def get_cash_entry(self, userid):
        exists = self.base.execute(f"SELECT EXISTS(\
                                     SELECT USERID\
                                     FROM BALANCE\
                                     WHERE USERID = {userid}\
                                     );")


        if exists.fetchone()[0] == 0:
            self.new_cash_entry(userid, 0)
            return 0
        exists.close()
        cursor = self.base.execute(f"SELECT CASH\
                                    FROM BALANCE\
                                    WHERE USERID = {userid};")
        cash = cursor.fetchone()[0]
        cursor.close()
        return cash
            

        

    def get_leaderboard(self):
        leaderboard_cursor = self.base.execute(f"SELECT USERID, CASH\
                                                     FROM BALANCE\
                                                     ORDER BY CASH DESC \
                                                     LIMIT 100;")
        return leaderboard_cursor

    def close(self):
        self.base.close()

        



    
        
        