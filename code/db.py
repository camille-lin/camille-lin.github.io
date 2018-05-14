class DB:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.title_side = '-'*12

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        return False

    def open(self):
        """ 開啟資料庫連線
        """
        if self.conn is None:
            import sqlite3
            self.conn = sqlite3.connect('lottery.db')
            self.cur = self.conn.cursor()
        return True

    def close(self):
        """ 關閉資料庫連線
        """
        if self.conn is not None:
            self.conn.close()
            self.conn = None
        return True

    def insert_lottery_row(self, row_data):
        """ 新增彩券
        """
        self.cur.execute("INSERT INTO LOTTERY VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", row_data)
        self.conn.commit()

    def get_max_term(self):
        """ 查詢最新期別
        """
        self.cur.execute("SELECT MAX(TERM) FROM TERM")
        return self.cur.fetchone()[0]

    def get_winning_list(self, term, customer_id):
        """查詢是否中獎
        """
        self.cur.execute("SELECT * FROM LOTTERY WHERE TERM=? AND CUSTOMER_ID=? AND RESULT<>'NO' ", (term, customer_id))
        return self.cur.fetchall()

    def select_lottery_id(self, term):
        self.cur.execute("SELECT COUNT(*) FROM LOTTERY WHERE TERM=?", (term, ))
        return self.cur.fetchone()[0]

    def update_term_data(self, db_cur, term_id):
        """ 更新本期人數、張數、收入
        """
        db_cur.execute("SELECT CUSTOMER_ID, COUNT(*) FROM LOTTERY WHERE TERM=? GROUP BY CUSTOMER_ID ", (term_id, ))
        terms = db_cur.fetchall()
        customers = len(terms)
        tickets = 0
        if customers > 0:
            for t in terms:
                tickets = tickets + t[1]
                # print(t)
            revenues = tickets * 50
            db_cur.execute("UPDATE TERM SET CUSTOMERS=?, TICKETS=?, REVENUES=? WHERE TERM=?", 
                (customers, tickets, revenues, term_id))
            conn.commit()
