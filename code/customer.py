from db import DB
from random import randint, sample

class Customer():
    def __init__(self):
        self.lottery_numbers = list(range(1, 19))
        self.menu_title = '顧客'
        self.account = ''
        self.menu = {
            '1':'購買大樂透',
            '2':'中獎查詢',
            'e':'離開'       
        }
        self.menu_func = {
            '1': lambda dbc: self.buy_lotteries(dbc),
            '2': lambda dbc: self.select_winning_list(dbc),
        }
        self.divider = '='*20
    def show_menu(self):
        pct = '◎' * 18
        print(pct)
        for fid, fname in self.menu.items():
            print(' %s. %s' % (fid, fname))
        print(pct)
        opt = input('請選擇: ').lower()
        if opt in self.menu.keys():
            return opt, self.menu[opt]
        else:
            return '', 'O.O請重新輸入O.O'

    def select_winning_list(self, db):
        new_term = db.get_max_term()
        term = input('搜尋哪一期 (n 表示最新開獎期別)?')
        if term == 'n':
            # 最新開獎期別與目前期別差一期
            term = new_term-1
        winning_list = db.get_winning_list(term, 1)
        for row in winning_list:
            print(row)
        
    def insert_random_lottery(self, db, lottery, term, customer_id):
        for i in range(lottery):
            # 新增彩券
            lottery_id = db.select_lottery_id(term) + 1
            row_data = [term, customer_id, lottery_id]
            row_data.extend(sample(self.lottery_numbers, 6))
            row_data.extend(['R', '', 0])
            print(row_data)
            db.insert_lottery_row(tuple(row_data))
        print()

    def buy_lotteries(self, db):
        while True:
            lottery = input('How many lotteries (quit)? ').lower()

            # 查詢目前為止最新期別
            term = db.get_max_term()
            if lottery == 'quit':
                break
            q1 = int(input('1.電腦選號 2.自己選號'))
            # 使用者購買彩券
            if q1 == 1:
                self.insert_random_lottery(db, int(lottery), term, 1)
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
                    lottery_id = db.select_lottery_id(term) + 1
                    row_data = (term, 1, lottery_id) + tuple(lo_num) + ('C', '', 0)
                    db.insert_lottery_row(row_data)
                    print(row_data)

            # 模擬其他顧客購買彩券
            # 其他顧客人數
            other_people = randint(5, 15)
            for i in range(other_people):
                other_lottery = randint(1, 5)
                # 模擬產生顧客編號
                customer_id = randint(2, 30)
                self.insert_random_lottery(db, other_lottery, term, customer_id)


with DB() as db:
    csm = Customer()
    while True:
        func_id, func_name = csm.show_menu()
        if func_id == 'e':
            break
        elif func_id == '':
            print(func_name)
        else:
            csm.menu_func[func_id](db)
        print()
