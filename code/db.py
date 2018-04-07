import os
import sqlite3

dbname = 'lottery.db'
os.unlink(dbname)

conn = sqlite3.connect(dbname)
if os.path.exists(dbname):
    cur = conn.cursor()

# 彩券對獎表
# 期別, 顧客編號, 彩券編號,
# 選號1, 選號2, 選號3, 選號4, 選號5, 選號6, 
# 選法(Custom/Random), 對獎結果(P1, P2, P3, P4, NO), 獎金
cur.execute('''CREATE TABLE LOTTERY 
    (TERM int, CUSTOMER_ID int, LOTTERY_ID int, 
     NUM1 int, NUM2 int, NUM3 int, NUM4 int, NUM5 int, NUM6 int,
     METHOD text, RESULT text, BONUS int)''')
# cur.execute("INSERT INTO LOTTERY VALUES(1, 1, 1, 11, 12, 13, 14, 15, 16, 'C', 'NO', 0)")
# cur.execute("INSERT INTO LOTTERY VALUES(1, 2, 2, 21, 22, 23, 24, 25, 26, 'C', 'P2', 16888)")
# cur.execute("INSERT INTO LOTTERY VALUES(1, 3, 3, 31, 32, 33, 34, 35, 36, 'C', 'P3', 2000)")
# cur.execute("INSERT INTO LOTTERY VALUES(1, 4, 4, 13, 15, 24, 29, 35, 47, 'R', 'P4', 200)")
# cur.execute("INSERT INTO LOTTERY VALUES(1, 1, 5, 11, 12, 13, 24, 25, 26, 'C', 'NO', 0)")
# cur.execute("INSERT INTO LOTTERY VALUES(1, 2, 6, 21, 22, 23, 34, 35, 36, 'C', 'P2', 16888)")
# cur.execute("INSERT INTO LOTTERY VALUES(1, 3, 7, 31, 32, 33, 44, 45, 46, 'C', 'NO', 0)")

# cur.execute("INSERT INTO LOTTERY VALUES(2, 1, 1, 11, 12, 13, 14, 15, 16, 'C', 'NO', 0)")
# cur.execute("INSERT INTO LOTTERY VALUES(2, 2, 2, 21, 22, 23, 24, 25, 26, 'C', 'NO', 0)")
# cur.execute("INSERT INTO LOTTERY VALUES(2, 3, 3, 31, 32, 33, 34, 35, 36, 'C', 'NO', 0)")
# cur.execute("INSERT INTO LOTTERY VALUES(2, 4, 4, 11, 17, 23, 26, 36, 42, 'R', 'P4', 200)")
# cur.execute("INSERT INTO LOTTERY VALUES(2, 5, 5, 11, 12, 13, 24, 25, 26, 'C', 'NO', 0)")
# cur.execute("INSERT INTO LOTTERY VALUES(2, 6, 6, 21, 22, 23, 34, 35, 36, 'C', 'NO', 0)")
# cur.execute("INSERT INTO LOTTERY VALUES(2, 7, 7, 31, 32, 33, 44, 45, 46, 'C', 'NO', 0)")

# 查詢目前為止最新期別
# max_term = SELECT MAX(TERM) FROM LOTTERY
# 查詢指定期別目前為止最大彩券編號
# SELECT MAX(LOTTERY_ID) FROM LOTTERY WEHRE TERM=max_term
# 查詢指定期別目前為止的彩券數
# SELECT COUNT(*) FROM LOTTERY WEHRE TERM=max_term

# 期別開獎表
# 期別, 人數, 張數, 收入,
# 獎號1, 獎號2, 獎號3, 獎號4, 獎號5, 獎號6, 
# 頭獎人數, 頭獎獎金70%, 二獎人數, 二獎獎金5%, 三獎人數, 三獎獎金2000, 普獎人數, 普獎獎金200
cur.execute('''CREATE TABLE TERM
    (TERM int, CUSTOMERS int, TICKETS int, REVENUES int, 
     NUM1 int, NUM2 int, NUM3 int, NUM4 int, NUM5 int, NUM6 int, 
     P1_WS int, P1_BS int, P2_WS int, P2_BS int, P3_WS int, P3_BS int, P4_WS int, P4_BS int)''')

# (1) 人數、張數、收入可一併算
# (2) 亂數產生獎號
# (3) 開獎要另外計算之後累加
cur.execute("INSERT INTO TERM VALUES(1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)")
# cur.execute("INSERT INTO TERM VALUES(2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)")

# 本期開獎 draw_winning_numbers()
# (1) 開出獎號
# (2) 核對所有彩券 <= LOTTERY
# (3) 更新人數、彩券數、收入、各種獎項中獎人數及發出獎金 UPDATE SQL
# (4) 新增下一期的 TERM

# (1) cur.execute("UPDATE TERM SET CUSTOMERS=?, TICKETS=?, REVENUES=? WHERE TERM=?", (1, 4, 7, 7*50))
# cur.execute("INSERT INTO TERM VALUES(1, 4, 7, 350, 13, 15, 22, 27, 31, 47, 0, 0, 0, 0, 0, 0, 1, 200)")
# cur.execute("INSERT INTO TERM VALUES(2, 7, 7, 350, 11, 12, 23, 31, 37, 42, 0, 0, 0, 0, 0, 0, 1, 200)")
conn.commit()

conn.close()


