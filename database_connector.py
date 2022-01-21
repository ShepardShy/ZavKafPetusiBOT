import sqlite3
import logging
import os

format_log = "%(asctime)s: %(message)s"
logging.basicConfig(format=format_log, level=logging.INFO,
                    datefmt="%H:%M:%S")


class DbConnector:
    connection = None
    cursor = None

    def connect(self):
        try:
            path = './db'
            if not os.path.exists(path):
                os.mkdir(path)
            self.connection = sqlite3.connect('./db/apps_base.db')
            self.cursor = self.connection.cursor()
            logging.info("Connecting to db")
        except sqlite3.Error as err:
            logging.error(f'Error connect to db: {err}')

    def create_table(self):
        check_table_query = "SELECT name FROM sqlite_master WHERE type='table' AND name='govno_coders';"
        self.cursor.execute(check_table_query)
        result_check = self.cursor.fetchone()
        if result_check is None:
            create_table_query = """CREATE TABLE govno_coders(
                                    id INTEGER primary key autoincrement unique,
	                                user_name TEXT not null unique,
	                                msg_text TEXT not null);"""
            self.cursor.execute(create_table_query)
            self.connection.commit()
            logging.info("Create table apps on database")

    def start_init(self):
        self.connect()
        self.create_table()

    def select_all_coders(self):
        self.cursor.execute("SELECT * FROM govno_coders;")
        res = self.cursor.fetchall()
        return res

    def close_connect(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            
    def answer_fail(coder):
        answers = ['был замечен господином З. и выгнан из аудитории.',
                  'не смог доставить груз и пошел изучать cisco.', 'попался на взятке.',
                  'не смог угадать число 2 и проиграл.', 'съел все конфеты Зацепина, чем его расстроил.',
                  'врезался в отбойник чем привлек внимание З.', 'пошел в преподаватели УрТИСИ.']
        i = random.randint(0, len(answers) - 1)
        res = f'{coder} {answers[i]} \n'
        return res

    def answer_success(coder):
        answers = ['обучался у шаолиньских монахов, которые научили его скрытности.',
                  'доставил успешно груз.', 'убедил Фарносова вернутся в УрТИСИ.',
                  'не убедил Фарносова вернутся в УрТИСИ, но зато пошел с ним пить пиво.', 'доказал, что он не связист.',
                  'переиграл и уничтожид З.']
        i = random.randint(0, len(answers) - 1)
        res = f'{coder} {answers[i]} \n'
        return res

def test():
    conn = DbConnector()
    conn.start_init()


if __name__ == "__main__":
    test()
