import os
import sqlite3
from random import randint, sample
#連接資料庫
conn = sqlite3.connect('lottery.db')
cur = conn.cursor()
lottery_numbers = list(range(1, 19))
def show_menu():
    pct = '◎' * 18
    print('''
    {}
    1. 購買大樂透
    2. 中獎查詢
    e. 離開       
    {}
    '''.format(pct, pct))
# 1. 買張大樂透吧!!
#     1. 自己選號
#     2. 電腦選號
# 2. 有沒有中獎呢... 
#     1. 開獎查詢(全部或單期)
#     2. 中獎查詢(全部或中獎)
# e. 離開 

def select_prize(db_cur):
    db_cur.execute("SELECT MAX(TERM) FROM TERM")
    new_term = db_cur.fetchone()[0]
    term = input('搜尋哪一期?(n表示最新一期)')
    if term == 'n':
        term = new_term
    db_cur.execute("""SELECT RESULT<>'NO' FROM LOTTERY WHERE CUSTOMER_ID = ?, TERM = ?"""(1, term))
    prize = db_cur.fatchall()
    print(prize)
    
def insert_random_lottery(db_cur, lottery, term, customer_id):
    for i in range(lottery):
       # 新增彩券
        db_cur.execute("SELECT COUNT(*) FROM LOTTERY WHERE TERM=?", (term,))
        lottery_id = db_cur.fetchone()[0] +1
        row_data = [term, customer_id, lottery_id]
        row_data.extend(sample(lottery_numbers, 6))
        row_data.extend(['R', '', 0])
        print(row_data)
        db_cur.execute("INSERT INTO LOTTERY VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", tuple(row_data))
        conn.commit()
    print()

def buy_lotteries(db_cur):
    # 查詢目前為止最新期別
    db_cur.execute("SELECT MAX(TERM) FROM TERM")
    term = db_cur.fetchone()[0]
    while True:
        lottery = input('How many lotteries (quit)? ').lower()
        if lottery == 'quit':
            break
        q1 = int(input('1.電腦選號 2.自己選號'))
        # 使用者購買彩券
        if q1 == 1:
            insert_random_lottery(db_cur, int(lottery), term, 1)
        elif q1 == 2:
            print('第 1 位顧客')
            for h in range(int(lottery)):
                lo_num = []
                for i in range(1, 7):
                    while True:
                        your_num = int(input('{}號數字'.format(i)))
                        if your_num in lo_num:
                            print('請重新輸入')
                            continue
                        if your_num not in lo_num:
                            lo_num.append(your_num)
                            break
                db_cur.execute("SELECT COUNT(*) FROM LOTTERY WHERE TERM=?", (term,))
                lottery_ID = db_cur.fetchone()[0] +1
                row_data = (term, 1, lottery_ID, lo_num[0], lo_num[1], lo_num[2], lo_num[3], lo_num[4], lo_num[5], 'C', '', 0)
                db_cur.execute("INSERT INTO LOTTERY VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", row_data)
                conn.commit()
                print(row_data)

        # 模擬其他顧客購買彩券
        # 其他顧客人數
        other_people = randint(5, 15)
        for i in range(other_people):
            other_lottery = randint(1, 5)
            # 模擬產生顧客編號
            customer_id = randint(2, 30)
            insert_random_lottery(db_cur, other_lottery, term, customer_id)

while True:
    show_menu()
    opt = input('>>').lower()
    if opt not in ('1', '2', 'e'):
        print('O.O請重新輸入O.O')
    if opt == '1':
        buy_lotteries(cur)
    elif opt == '2':
        select_prize(cur)
    elif opt == 'e':
        break