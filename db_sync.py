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
            self.cur.callproc('creta',[self.table_name])      #프로시져로, 파일처리, 장점? 내가 일해도 어떤 논리로 하는지 상대가 모름  - 보안성
            self.cur.callproc("SEQS",[f'{self.table_name}'])  #시퀀스 생성
            return self.Select_all()
        except Exception as E:                    #이미 테이블이 존재하는 경우 조회하도록.
            try:
                self.cur.callproc("SEQS", [self.table_name])
            except:
                pass
        return self.Select_all()


    def Insert_m(self,ran1,ran2,img,text):
        try:
            self.__init__(self.table_name)
            in_val2 = self.cur.execute(f"select {self.table_name}_seq.nextval from dual").fetchone()[0]
            out_val = self.cur.var(str)
            self.cur.callproc('numbering', [in_val2, self.table_name, out_val])
            self.cur.execute(f"insert into {self.table_name} values(:IDX, :검색PK ,:검색시작범위, :검색종료범위,  :텍스트조회, :이미지조회 )",
                {"IDX":in_val2, "검색PK": out_val.getvalue(), "검색시작범위": json.dumps(ran1), "검색종료범위": json.dumps(ran2), "텍스트조회": json.dumps(text[:5]), "이미지조회": json.dumps(img[:5])})
            self.db.commit()
            self.db.close()

        except Exception as E:
            print(E)

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
    a = input('검색이름 ')
    ora = OraDb(a)
    ora.Create_table()

    year = '2020'
    for i in range(1,13):
        if i in (1,3,5,7,8):
            year_month = year +'-0'+ str(i)
            d = 1
            while d < 32:
                day = str(d)
                year_month_day = year_month + '-'+ day + '~' + year_month +'-'+ day
                ora.scrap = scrapping.Nav_scrap
                ran1, ran2 = ora.scrap.get_range(year_month_day)
                img, txt = ora.scrap.img_or_txt(a,ran1,ran2)
                ora.Insert_m(ran1,ran2,img,txt)
                d +=1
        elif i in (10,12):
            year_month = year +'-'+str(i)
            d=1
            while d < 32:
                day = str(d)
                year_month_day = year_month + '-'+ day + '~' + year_month +'-'+ day
                ora.scrap = scrapping.Nav_scrap
                ran1, ran2 = ora.scrap.get_range(year_month_day)
                img, txt = ora.scrap.img_or_txt(a,ran1, ran2)
                ora.Insert_m(ran1, ran2, img, txt)
                d += 1
        elif i in (4,6,9,11):
            year_month = year +'-'+str(i)
            d = 1
            while d < 31:
                day = str(d)
                year_month_day = year_month + '-'+ day + '~' + year_month +'-'+ day
                ora.scrap = scrapping.Nav_scrap
                ran1, ran2 = ora.scrap.get_range(year_month_day)
                img, txt = ora.scrap.img_or_txt(a, ran1, ran2)
                ora.Insert_m(ran1, ran2, img, txt)
                d += 1
        else:
            year_month = year + '-0' + str(i)
            d = 1
            while d < 29:
                day = str(d)
                year_month_day = year_month + '-'+ day + '~' + year_month +'-'+ day
                ora.scrap = scrapping.Nav_scrap
                ran1, ran2 = ora.scrap.get_range(year_month_day)
                img, txt = ora.scrap.img_or_txt(a, ran1, ran2)
                ora.Insert_m(ran1, ran2, img, txt)
                d += 1

