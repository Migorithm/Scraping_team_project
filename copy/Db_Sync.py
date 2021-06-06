import cx_Oracle
import scrapping
import json
import undetected_chromedriver.v2 as cv2


class OraDb:
    def __init__(self,table_name): # 연결
        self.dsn = cx_Oracle.makedsn("localhost", 1521, 'xe')
        self.db = cx_Oracle.connect('SCOTT', 'TIGER', self.dsn)
        self.cur = self.db.cursor()
        self.table_name = table_name

    def Create_table(self):
        try :
            self.cur.callproc('creta',[self.table_name])      #프로시져로 테이블생성
            self.cur.callproc("SEQS",[f'{self.table_name}'])  #시퀀스 생성
            return self.Select_all()
        except Exception as E:                    #이미 테이블이 존재하는 경우 조회하도록.
            try:
                self.cur.callproc("SEQS", [self.table_name])
            except:
                pass
        return self.Select_all()


    def Insert_m(self,ran1,ran2,img,text):
        # try:
            self.__init__(self.table_name)
            in_val2 = self.cur.execute(f"select {self.table_name}_seq.nextval from dual").fetchone()[0]
            out_val = self.cur.var(str)
            print(in_val2,type(in_val2))
            self.cur.callproc('numbering', [in_val2, self.table_name, out_val])
            self.cur.execute(f"insert into {self.table_name} values(:IDX, :검색PK ,:검색시작범위, :검색종료범위,  :텍스트조회, :이미지조회 )",
                {"IDX":in_val2, "검색PK": out_val.getvalue(), "검색시작범위": json.dumps(ran1), "검색종료범위": json.dumps(ran2), "텍스트조회": json.dumps(text), "이미지조회": json.dumps(img)})
            self.db.commit()
            self.db.close()

        # except Exception as E:
        #     self.__init__(self.table_name)
        #     in_val2 = self.cur.execute(f"select {self.table_name}_seq.nextval from dual").fetchone()[0]
        #     out_val = self.cur.var(str)
        #     self.cur.callproc('numbering', [in_val2, self.table_name, out_val])
        #     self.cur.execute(f"insert into {self.table_name} values('{out_val.getvalue()}' ,:검색시작범위, :검색종료범위,  :텍스트조회, :이미지조회 )",
        #         {"검색시작범위": json.dumps(ran1), "검색종료범위": json.dumps(ran2), "텍스트조회": json.dumps(text), "이미지조회": json.dumps(img)})
        #     self.db.commit()
        # finally:
        #     self.cur.close()
        #     self.db.close()

    def Select_all(self):
        try:
            self.cur.execute(f"select * from {self.table_name} order by 1 desc")
            result = []
            for i in self.cur.fetchall():
                result.append((i[0],i[1],"-".join(json.loads(i[2])),"-".join(json.loads(i[3])),json.loads(i[4]),json.loads(i[5])))
            cols =[i[0] for i in self.cur.description] #column
            return cols, result
        except Exception as E:
            self.__init__(self.table_name)
            self.cur.execute(f"select * from {self.table_name} order by 1 desc")
            result = []
            for i in self.cur.fetchall():
                result.append((i[0],i[1],"-".join(json.loads(i[2])),"-".join(json.loads(i[3])),json.loads(i[4]),json.loads(i[5])))
            cols = [i[0] for i in self.cur.description]  # column
            return cols, result
        finally:
            self.cur.close()
            self.db.close()

    def __del__(self):
        pass




if __name__ == '__main__':
    pass