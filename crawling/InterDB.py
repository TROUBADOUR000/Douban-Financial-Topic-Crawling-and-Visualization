import sqlite3

import pandas as pd


class InterDB:
    __name__ = None
    # 打开
    def __init__(self, name):
        self.__name__ = name
        self.connect = sqlite3.connect(name)
        self.cursor = self.connect.cursor()

    def open_db(self):
        try:
            self.cursor.execute("create table if not exists Article ("
                                "a_title text,"
                                "a_text text,"
                                "a_time text,"# not chinese
                                "a_address text,"
                                "a_keywords text,"
                                "a_shared integer,"
                                "a_sentiment float,"
                                "primary key(a_text))")
            self.cursor.execute("create table if not exists Topic ("
                                "t_name nvarchar(20),"
                                "t_no text,"# not chinese
                                "primary key(t_name))")
            self.cursor.execute("create table if not exists Note ("
                                "n_name nvarchar(100),"
                                "n_no text,"  # not chinese
                                "primary key(n_name))")
        except Exception as err:
            print(err)

    # 关闭
    def close_db(self):
        self.connect.commit()
        self.connect.close()

    # 插入问题
    def insert_db_artical(self,a_title:str,a_text:str,a_time:str,a_address:str,a_keywords:str,a_shared:int,a_sentiment:float):
        try:
            self.cursor.execute("insert into Article(a_title,a_text,a_time,a_address,a_keywords,a_shared,a_sentiment)"
                                "values(?,?,?,?,?,?,?)", (a_title,a_text,a_time,a_address,a_keywords,a_shared,a_sentiment))
            self.connect.commit()
        except Exception as err:
            print(err)


    # 插入话题链接
    def insert_db_href(self, name, url):
        try:
            self.cursor.execute("insert into Topic(t_name,t_no)"
                                " values (?,?)", (name, url))
            self.connect.commit()
        except Exception as err:
            print(err)

    # 插入note链接
    def insert_db_note(self, name, url):
        try:
            self.cursor.execute("insert into Note(n_name,n_no)"
                                " values (?,?)", (name, url))
            self.connect.commit()
        except Exception as err:
            print(err)


    def read_db(self,command:str):
        import os.path
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, self.__name__)
        connect = sqlite3.connect(db_path)
        cursor = connect.cursor()
        frame1 = pd.read_sql(command, connect)
        cursor.close()
        connect.commit()
        connect.close()
        return frame1


    def to_excel(self):
        connect = sqlite3.connect(self.__name__)
        cursor = connect.cursor()
        frame1 = pd.read_sql('SELECT * FROM Question', connect)
        frame2 = pd.read_sql('SELECT * FROM Answer', connect)
        frame3 = pd.read_sql('SELECT * FROM Topic', connect)
        cursor.close()
        connect.commit()
        connect.close()
        writer = pd.ExcelWriter('all.xlsx', engine='openpyxl')
        '''
        book=load_workbook('all.xlsx')
        writer.book=book
        '''
        frame1.to_excel(writer, index=False, header=True, sheet_name='Question')
        frame2.to_excel(writer, index=False, header=True, sheet_name='Answer')
        frame3.to_excel(writer, index=False, header=True, sheet_name='Topic')
        writer.save()


if __name__ == "__main__":
    ib = InterDB('t.db')
    ib.open_db()
    test_flag = 1
    if test_flag == 1:
        ib.insert_db_artical("你是谁？", "123456", "20020809", "http:\\zhihu.com\\question\\123456", "数学，计算机",
                              1252, 123)
        ib.insert_db_note("123456", "我是人")
        ib.insert_db_href("夸奖", "http:\\zhihu.com\\topic\\123456")
    ib.close_db()
