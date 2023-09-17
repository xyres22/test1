import sqlite3

class Base():
    def __init__(self,db):
        self.conn=sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS store (title TEXT PRIMARY KEY,details TEXT,day DATE,hour TIME)")
        self.conn.commit()

    def add_entry(self,text,second_text,date,time):
        self.cur.execute("INSERT INTO store(title,details,day,hour) VALUES(?,?,?,?)",(text,second_text,date,time))
        self.conn.commit()

    def view_all(self):
        self.cur.execute('SELECT * FROM store')
        rows = self.cur.fetchall()
        self.conn.commit()
        return rows
    
    def exist(self,text):
        self.cur.execute('SELECT COUNT() FROM store WHERE title = ?',(text,))
        rows = self.cur.fetchall()
        self.conn.commit()
        return rows
    
    def delete(self,text):
        self.cur.execute('DELETE FROM store WHERE title = ?',(text,))
        self.conn.commit()

    def search(self,text):
        self.cur.execute('SELECT * FROM store WHERE title = ?',(text,))
        rows = self.cur.fetchall()
        self.conn.commit()
        return rows
    
    def update(self,second_text,date,time,text):
        self.cur.execute('UPDATE store SET details = ?, day= ? , hour = ? WHERE title = ?',(second_text,date,time,text))
        self.conn.commit()