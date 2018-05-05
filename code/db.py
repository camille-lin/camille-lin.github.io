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

# 期別開獎表
# 期別, 人數, 張數, 收入,
# 獎號1, 獎號2, 獎號3, 獎號4, 獎號5, 獎號6, 
# 頭獎人數, 頭獎獎金70%, 二獎人數, 二獎獎金5%, 三獎人數, 三獎獎金2000, 普獎人數, 普獎獎金200
cur.execute('''CREATE TABLE TERM
    (TERM int, CUSTOMERS int, TICKETS int, REVENUES int, 
     NUM1 int, NUM2 int, NUM3 int, NUM4 int, NUM5 int, NUM6 int, 
     P1_WS int, P1_BS int, P2_WS int, P2_BS int, P3_WS int, P3_BS int, P4_WS int, P4_BS int)''')

cur.execute("INSERT INTO TERM VALUES(1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)")

conn.commit()
conn.close()


