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

    def update_term_data(self, term_id):
        """ 更新本期人數、張數、收入
        """
        self.cur.execute("SELECT CUSTOMER_ID, COUNT(*) FROM LOTTERY WHERE TERM=? GROUP BY CUSTOMER_ID ", (term_id, ))
        terms = self.cur.fetchall()
        customers = len(terms)
        tickets = 0
        if customers > 0:
            for t in terms:
                tickets = tickets + t[1]
                # print(t)
            revenues = tickets * 50
            self.cur.execute("UPDATE TERM SET CUSTOMERS=?, TICKETS=?, REVENUES=? WHERE TERM=?", 
                (customers, tickets, revenues, term_id))
            self.conn.commit()
    ##名稱
    def select(self):
        self.cur.execute("""SELECT TERM, CUSTOMERS, TICKETS, REVENUES, (REVENUES-P1_BS-P2_BS-P3_BS-P4_BS) AS PROFIT,
            P1_WS, P1_BS, P2_WS, P2_BS, P3_WS, P3_BS, P4_WS, P4_BS FROM TERM """)
        return self.cur.fetchall()[:-1]

    def select_revenues(self, term_id):
        self.cur.execute("SELECT REVENUES FROM TERM WHERE TERM=?", (term_id, ))
        return self.cur.fetchone()[0]

    def update_result_to_lottery(self, bindings):
        self.cur.execute("UPDATE LOTTERY SET RESULT=? WHERE LOTTERY_ID=?", bindings)
        self.conn.commit()

    def update_bonus_to_lottery(self, bindings):
        self.cur.execute("UPDATE LOTTERY SET BONUS=? WHERE LOTTERY_ID=?", bindings)
        self.conn.commit()

    def update_to_term(self, bindings):
        self.cur.execute("UPDATE TERM SET NUM1=?, NUM2=?, NUM3=?, NUM4=?, NUM5=?, NUM6=? WHERE TERM=?", bindings)
        self.conn.commit()

    def update_winners_and_bonus(self, term_id):
        ''' 更新本期中獎人數及獎金 '''
        self.cur.execute("SELECT RESULT, COUNT(*), SUM(BONUS) FROM LOTTERY WHERE TERM=? AND RESULT<>'NO' GROUP BY RESULT", (term_id, ))
        terms = self.cur.fetchall()
        if len(terms) > 0:
            for t in terms:
                t = list(t)
                print(t)
                term_bonus = (t[1], t[2], term_id)
                if t[0] == 'P1':
                    self.cur.execute("UPDATE TERM SET P1_WS=?, P1_BS=? WHERE TERM=?", term_bonus)
                elif t[0] == 'P2':
                    self.cur.execute("UPDATE TERM SET P2_WS=?, P2_BS=? WHERE TERM=?", term_bonus)
                elif t[0] == 'P3':
                    self.cur.execute("UPDATE TERM SET P3_WS=?, P3_BS=? WHERE TERM=?", term_bonus)
                elif t[0] == 'P4':
                    self.cur.execute("UPDATE TERM SET P4_WS=?, P4_BS=? WHERE TERM=?", term_bonus)

        # 新增下期預設資料
        self.cur.execute("INSERT INTO TERM VALUES(?, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)", (term_id+1, ))
        self.conn.commit()


    def get_lottery_list(self, term_id=0):
        """ 擷取彩券清單資料
        """
        if term_id == 0:
            self.cur.execute("SELECT * FROM LOTTERY")
        else:
            self.cur.execute("SELECT * FROM LOTTERY WHERE TERM=?", (term_id,))
        return self.cur.fetchall()

    def get_term_list(self):
        self.cur.execute("SELECT * FROM TERM")
        return self.cur.fetchall()
