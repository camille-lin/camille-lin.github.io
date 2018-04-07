import os
import sqlite3
from random import sample
#連接資料庫
conn = sqlite3.connect('lottery.db')
cur = conn.cursor()

def show_menu():
    divider = '+ '*25
    menu = '''1. 銷售統計 (依期別/人數/張數/收入/利潤排序)
2. 單期銷售 (輸入期別或最新一期) ***已完整    
3. 兌獎查詢 (輸入期別或最新一期)
4. 本期開獎
e. 離開'''

    print(divider) 
    print(menu)
    print(divider)   

def get_max_term_id(db_cur):
    """ 取得最新期別編號 
    """
    db_cur.execute("SELECT MAX(TERM) FROM LOTTERY")
    return db_cur.fetchone()[0]
    
def get_lottery_list(db_cur, term_id=0):
    """ 擷取彩券清單資料
    """
    if term_id == 0:
        db_cur.execute("SELECT * FROM LOTTERY")
    else:
        db_cur.execute("SELECT * FROM LOTTERY WHERE TERM=?", (term_id,))
    return db_cur.fetchall()

def show_lottery_list(db_cur, term_id=0):
    """ 顯示彩券清單 
    """
    lotteries = get_lottery_list(db_cur, term_id)
    if len(lotteries) > 0:
        for t in lotteries:
            print(t)
        print()
    else:
        print('The table is empty.')

def show_term_list(db_cur):
    """ 開獎清單 
    """
    db_cur.execute("SELECT * FROM TERM")
    terms = db_cur.fetchall()
    if len(terms) > 0:
        for t in terms:
            print(t)
        print()
    else:
        print('The table is empty.')

def lotteries_summary(db_cur, sort_by):
    """ 銷售統計 (依期別/人數/張數/收入/利潤排序)
    """
    # GROUP BY TERM, CUSTOMER_ID 以期別、顧客編號為群組區分計算張數
    # TODO 針對使用 list or tuple 排序的範例請在教材中搜尋 pairs
    db_cur.execute("SELECT * FROM TERM")   
    count_tickets = db_cur.fetchall()
    if sort_by == 1:
        # 將資料以 tuple 儲存並放在 list
        print(count_tickets)
        for t in count_tickets:
            print(t)
        print()

def update_term_data(db_cur, term_id):
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

def get_prize_top_two(db_cur, term_id):
    """ 計算頭獎及二獎獎金
    """
    db_cur.execute("SELECT REVENUES FROM TERM WHERE TERM=?", (term_id, ))
    revenues = db_cur.fetchone()[0]
    return (int(revenues*0.7), round(revenues*0.05))

def draw_win_numbers(db_cur, term_id):
    """ 本期開獎及計算獎金 
    """
    # 開獎及對獎
    win_num = set(sample(list(range(1, 50)), 6))
    print(win_num)
    # win_num = {24, 40, 14, 47, 26, 46}
    prize_types = ('P4', 'P3', 'P2', 'P1')
    # 頭獎及二獎獎金
    p1_bonus, p2_bonus = get_prize_top_two(db_cur, term_id)
    print(p1_bonus, p2_bonus)
    lotteries = [list(row) for row in get_lottery_list(db_cur, term_id)]
    if len(lotteries) > 0:
        # 對獎
        p1_count = 0
        p2_count = 0
        for row in lotteries:
            match_numbers = set(row[3:9]).intersection(win_num)
            match_count = len(match_numbers)
            if match_count >= 3:
                row[10] = prize_types[match_count-3]
                if row[10] == 'P1':
                    p1_count += 1
                elif row[10] == 'P2':
                    p2_count += 1
            else:
                row[10] = 'NO'
            num = row[2], row[3], row[4], row[5], row[6], row[7]
            db_cur.execute("UPDATE LOTTERY SET RESULT=?, BONUS=? WHERE LOTTERY_ID=?", (row[10], row[11], lotteries[2]))
            print(row, match_numbers, match_count)
        # 計算頭獎及二獎平均分配獎金 
        p1_avg = 0
        p2_avg = 0
        if p1_count != 0:
            p1_avg = int(p1_bonus / p1_count)
        if p2_count != 0:
            p2_avg = int(p2_bonus / p2_count)
        # 分配獎金
        tup_bonus = (p1_avg, p2_avg, 2000, 200)
        for row in lotteries:
            if row[10] != 'NO':
                row[11] = tup_bonus[int(row[10][1])-1]
            win_num = list(win_num)
            # 執行有問題
            db_cur.execute("UPDATE TERM SET NUM1=?, NUM2=?, NUM3=?, NUM4=?, NUM5=?, NUM6=? WHERE TERM=?", (win_num[0], win_num[1], win_num[2], win_num[3], win_num[4], win_num[5], term_id))
            # TODO 更新到資料庫 => UPDATE SQL
            print(row)
    else:
        print('The table is empty.')

    # 更新本期中獎人數及獎金
    db_cur.execute("SELECT RESULT, COUNT(*), SUM(BONUS) FROM LOTTERY WHERE TERM=? AND RESULT<>'NO' GROUP BY RESULT", (1, ))
    terms = db_cur.fetchall()
    if len(terms) > 0:
        for t in terms:
            t = list(t)
            print(t)
            if t[0] == 'P1':
                db_cur.execute("UPDATE TERM SET P1_WS=?, P1_BS=? WHERE TERM = ?", (t[1], t[2], 1))
            elif t[0] == 'P2':
                db_cur.execute("UPDATE TERM SET P2_WS=?, P2_BS=? WHERE TERM = ?", (t[1], t[2], 1))
            elif t[0] == 'P3':
                db_cur.execute("UPDATE TERM SET P3_WS=?, P3_BS=? WHERE TERM = ?", (t[1], t[2], 1))
            elif t[0] == 'P4':
                db_cur.execute("UPDATE TERM SET P4_WS=?, P4_BS=? WHERE TERM = ?", (t[1], t[2], 1))

    # 新增下期預設資料
    # cur.execute("INSERT INTO TERM VALUES(term_id+1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)")
    conn.commit()
while True:
    show_menu() 
    main_opt = input('>> ').lower()
    max_term_id = get_max_term_id(cur)
    if main_opt == '1':
        # 銷售統計
        # 期別 人數 張數 收入 利潤
        #    1    4    7  350  150
        #    2    7    7  350  150
        print('銷售統計')
        opt = int(input('1.期別 2.人數 3.張數 4.收入 5.利潤排序'))
        if opt in range(1, 6):
            update_term_data(cur, max_term_id)
            lotteries_summary(cur, opt)

    elif main_opt == '2':
        print('單期銷售')
        print('目前最新期別:', max_term_id)
        qry_term_id = input('輸入期別 (0 表示全部，直接 Enter 可查最新一期):')
        # 設定查詢期別
        if qry_term_id.isdigit():
            qry_term_id = int(qry_term_id)
        else:
            qry_term_id = max_term_id
        # 處理查詢
        if qry_term_id not in range(0, max_term_id+1):
            print('期別錯誤')
        elif qry_term_id == 0:
            # 全部銷售明細
            show_lottery_list(cur)
        else:
            # 單期銷售明細
            show_lottery_list(cur, qry_term_id)

    elif main_opt == '3':
        print('兌獎查詢')
        show_term_list(cur)
    elif main_opt == '4':
        print('本期開獎')
        update_term_data(cur, max_term_id)
        draw_win_numbers(cur, max_term_id)
    elif main_opt == 'e':
        break
    elif main_opt not in '12345':
        print('◎.◎請重新輸入◎.◎')

# 關閉資料庫
conn.close()
