from random import sample
from db import DB

class Agent():
    def __init__(self):
        self.lottery_numbers = list(range(1, 19))
        self.menu_title = '券商'
        self.account = ''
        self.max_term_id = db.get_max_term()
        self.menu = {
            '1':'銷售統計 (依期別/人數/張數/收入/利潤排序)',
            '2':'單期銷售 (輸入期別或最新一期)',
            '3':'兌獎查詢 (輸入期別或最新一期)',
            '4':'本期開獎',
            'e':'離開'       
        }
        self.menu_func = {
            '1': lambda dbc: self.judgment_sales_statistics(dbc),
            '2': lambda dbc: self.judgment_single_sale(dbc),
            '3': lambda dbc: self.show_term_list(dbc),
            '4': lambda dbc: self.draw_win_numbers(dbc)
        }
        self.divider = '='*20


    def show_menu(self, db):
        divider = '+ '*25
        print(divider)
        for fid, fname in self.menu.items():
            print(' %s. %s' % (fid, fname))
        print(divider)
        opt = input('請選擇: ').lower()
        if opt in self.menu.keys():
            return opt, self.menu[opt]
        else:
            return '', 'O.O請重新輸入O.O'
  
    def judgment_sales_statistics(self, db):
        print('銷售統計')
        opt1 = int(input('1.期別 2.人數 3.張數 4.收入 5.利潤排序:'))
        opt2 = input('a.由高到低(DESC) b.由低到高(ASC):').lower()
        if opt1 in range(1, 6):
            db.update_term_data(self.max_term_id)
            self.lotteries_summary(db, opt1, opt2=='a')

    def judgment_single_sale(self, db):
        print('單期銷售')
        print('目前最新期別 :', self.max_term_id)
        qry_term_id = input('輸入期別 (0 表示全部，直接 Enter 可查最新一期):')
        # 設定查詢期別
        if qry_term_id.isdigit():
            qry_term_id = int(qry_term_id)
        else:
            qry_term_id = self.max_term_id
        # 處理查詢
        if self.max_term_id is None or qry_term_id not in range(0, self.max_term_id+1):
            print('期別錯誤')
        elif qry_term_id == 0:
            # 全部銷售明細
            self.show_lottery_list(db)
        else:
            # 單期銷售明細
            self.show_lottery_list(db, qry_term_id)

    def show_lottery_list(self, db, term_id=0):
        """ 顯示彩券清單 
        """
        lotteries = db.get_lottery_list(term_id)
        if len(lotteries) > 0:
            for t in lotteries:
                print(t)
            print()
        else:
            print('The table is empty.')

    def show_term_list(self, db):
        """ 開獎清單 
        """
        terms = db.get_term_list()
        if len(terms) > 0:
            for t in terms:
                print(t)
            print()
        else:
            print('The table is empty.')


    def lotteries_summary(self, db, sort_by, is_desc):
        """ 銷售統計 (依期別/人數/張數/收入/利潤排序)
        """
        term_stat = db.select()
        term_stat.sort(key=lambda ts: ts[sort_by-1], reverse=is_desc)
        for ts in term_stat:
            print(ts)
        print()    


    def get_prize_top_two(self, db, term_id):
        """ 計算頭獎及二獎獎金
        """
        revenues = db.select_revenues(term_id)
        if revenues == 0:
            print('The table is empty.')
        else:
            return (int(revenues*0.7), round(revenues*0.05))

    def draw_win_numbers(self, db):
        """ 本期開獎及計算獎金 
        """
        # 開獎及對獎
        self.max_term_id = db.get_max_term()
        db.update_term_data(self.max_term_id)
        win_num = set(sample(list(range(1, 19)), 6))
        print(win_num)
        prize_types = ('P4', 'P3', 'P2', 'P1')
        # 頭獎及二獎獎金
        p1_bonus, p2_bonus = self.get_prize_top_two(db, self.max_term_id)
        print(p1_bonus, p2_bonus)
        lotteries = [list(row) for row in db.get_lottery_list(self.max_term_id)]
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
                # 彩券兌獎結果
                # print(row, match_numbers, match_count)
                db.update_result_to_lottery((row[10], row[2]))
            # 計算頭獎及二獎平均分配獎金 
            p1_avg = 0
            p2_avg = 0
            if p1_count != 0:
                p1_avg = int(p1_bonus / p1_count)
            if p2_count != 0:
                p2_avg = int(p2_bonus / p2_count)
            # 分配獎金
            tup_bonus = (p1_avg, p2_avg, 100, 20)
            for row in lotteries:
                if row[10] != 'NO':
                    row[11] = tup_bonus[int(row[10][1])-1]
                win_num = list(win_num)
                db.update_bonus_to_lottery((row[11], row[2]))
                # 有中獎再顯示
                if row[10] != 'NO':
                    print(row)

            db.update_to_term(((win_num[0], win_num[1], win_num[2], win_num[3], win_num[4], win_num[5], self.max_term_id)))
        else:
            print('The table is empty.')
        db.update_winners_and_bonus(self.max_term_id)

with DB() as db:
    agent = Agent()        
    while True:
        func_id, func_name = agent.show_menu(db)
        if func_id == 'e':
            break
        elif func_id == '':
            print(func_name)
        else:
            agent.menu_func[func_id](db)
        print()