from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from datetime import datetime as dt
from PIL import Image, ImageTk
from WordC import WC
import db_sync
import scrapping
import urllib.request

class Window2():
    def __init__(self,get1):
        self.search_word = ''
        self.window = Tk()
        self.window.title('EncoreTeam 1')
        self.window.geometry('700x700')
        self.window.resizable(False, False)
        self.data = get1
        self.img = ''

    def show_error(self):
        msgbox.showerror('Error', '검색할 수 없는 기간을 선택하셨습니다.')
    # 기존 Window2 제거후 새로운 Window2 열기
        #self.window.destroy()
        #window2 = Window2(self.data)
        #window2.show_result_window2(self.search_word)
    # DB 타입 설정


    def con1(self):
        self.type = 'local'
        pp = self.selc_period.get()
        if pp == 'No':
            self.get_date = '{}-{}-{}~{}-{}-{}'.format(dt.now().year, dt.now().month, dt.now().day, dt.now().year,
                                                       dt.now().month, dt.now().day)
            msgbox.showinfo('알림', '기본설정 기간으로 갱신합니다')
        else:
            self.y1 = self.com_p_year1.get()
            self.m1 = self.com_p_month1.get()
            self.d1 = self.com_p_day1.get()
            self.y2 = self.com_p_year2.get()
            self.m2 = self.com_p_month2.get()
            self.d2 = self.com_p_day2.get()
            for i in (self.y1, self.m1, self.d1, self.y2, self.m2, self.d2):
                if i.isnumeric() != True:
                    self.show_error()
            self.m1, self.d1, self.m2, self.d2 = map(lambda x: '0' + x if len(x) == 1 else x, (self.m1, self.d1, self.m2, self.d2))

            self.nowyear, self.nowmonth, self.nowday = dt.now().year, dt.now().month, dt.now().day
            self.nowyear, self.nowmonth, self.nowday = map(lambda x: '0' + str(x) if len(str(x)) == 1 else str(x),
                                                           (self.nowyear, self.nowmonth, self.nowday))
            self.current_time = self.nowyear + self.nowmonth + self.nowday
            self.start_date = self.y1 + self.m1 + self.d1
            self.end_date = self.y2 + self.m2 + self.d2
            if self.start_date > self.current_time or self.end_date > self.current_time:
                self.show_error()
            if self.start_date > self.end_date:

                self.show_error()
            else:
                self.get_date = '{}-{}-{}~{}-{}-{}'.format(self.y1, self.m1, self.d1, self.y2, self.m2, self.d2)
        ora = db_sync.OraDb(self.search_word)
        ora.scrap = scrapping.Nav_scrap
        ran1 , ran2 = ora.scrap.get_range(self.get_date)
        img, text = ora.scrap.img_or_txt(self.search_word,ran1,ran2)

        for index, file in enumerate(img, 1):
            urllib.request.urlretrieve(file, 'c:/ENCORE1/' + str(index) + f'_{self.search_word}.jpg')  # url로 표시된 네트워크 객체를 로컬 파일로 복사.
        with open(f'c:/ENCORE1/{self.search_word}.txt', 'w', encoding='utf-8') as f:
            f.writelines(text)

    def con2(self):
        self.type = 'db'
        pp = self.selc_period.get()
        if pp == 'No':
            self.get_date = '{}-{}-{}~{}-{}-{}'.format(dt.now().year, dt.now().month, dt.now().day, dt.now().year,
                                                       dt.now().month, dt.now().day)
            msgbox.showinfo('알림', '기본설정 기간으로 갱신합니다')
        else:
            self.y1 = self.com_p_year1.get()
            self.m1 = self.com_p_month1.get()
            self.d1 = self.com_p_day1.get()
            self.y2 = self.com_p_year2.get()
            self.m2 = self.com_p_month2.get()
            self.d2 = self.com_p_day2.get()
            for i in (self.y1,self.m1,self.d1,self.y2,self.m2,self.d2):
                if i.isnumeric() != True :
                    self.show_error()
            self.m1, self.d1 , self.m2, self.d2 = map(lambda x:'0'+x if len(x) ==1 else x,(self.m1,self.d1,self.m2,self.d2))

            self.nowyear, self.nowmonth, self.nowday = dt.now().year, dt.now().month, dt.now().day
            self.nowyear, self.nowmonth, self.nowday = map(lambda x: '0' + str(x) if len(str(x)) == 1 else str(x),
                                                           (self.nowyear, self.nowmonth, self.nowday))
            self.current_time = self.nowyear + self.nowmonth + self.nowday

            self.start_date = self.y1 + self.m1 + self.d1
            self.end_date = self.y2 + self.m2 + self.d2


            if self.start_date > self.current_time or self.end_date > self.current_time:
                self.show_error()
            if self.start_date > self.end_date:
                self.show_error()
            else:
                self.get_date = '{}-{}-{}~{}-{}-{}'.format(self.y1, self.m1, self.d1, self.y2, self.m2, self.d2)
        ora = db_sync.OraDb(self.search_word)
        ora.scrap = scrapping.Nav_scrap
        ran1 , ran2 = ora.scrap.get_range(self.get_date)
        img, text = ora.scrap.img_or_txt(self.search_word,ran1,ran2)
        ora.Insert_m(ran1,ran2,img[:5],text[:5])
    def con3(self):
        self.type = 'both'
        pp = self.selc_period.get()
        if pp == 'No':
            self.get_date = '{}-{}-{}~{}-{}-{}'.format(dt.now().year, dt.now().month, dt.now().day, dt.now().year,
                                                       dt.now().month, dt.now().day)
            msgbox.showinfo('알림', '기본설정 기간으로 갱신합니다')
        else:
            self.y1 = self.com_p_year1.get()
            self.m1 = self.com_p_month1.get()
            self.d1 = self.com_p_day1.get()
            self.y2 = self.com_p_year2.get()
            self.m2 = self.com_p_month2.get()
            self.d2 = self.com_p_day2.get()

            for i in (self.y1, self.m1, self.d1, self.y2, self.m2, self.d2):
                if i.isnumeric() != True:
                    self.show_error()
            self.m1, self.d1, self.m2, self.d2 = map(lambda x: '0' + x if len(x) == 1 else x,
                                                     (self.m1, self.d1, self.m2, self.d2))

            self.nowyear,self.nowmonth,self.nowday = dt.now().year,  dt.now().month ,dt.now().day
            self.nowyear,self.nowmonth,self.nowday = map(lambda x : '0' +str(x) if len(str(x)) ==1 else str(x), (self.nowyear,self.nowmonth,self.nowday))
            self.current_time = self.nowyear +self.nowmonth +self.nowday

            self.start_date = self.y1 + self.m1 + self.d1
            self.end_date = self.y2 + self.m2 + self.d2
            if self.start_date > self.current_time or self.end_date > self.current_time:
                self.show_error()
            if self.start_date > self.end_date:

                self.show_error()
            else:
                self.get_date = '{}-{}-{}~{}-{}-{}'.format(self.y1, self.m1, self.d1, self.y2, self.m2, self.d2)
        ora = db_sync.OraDb(self.search_word)
        ora.scrap = scrapping.Nav_scrap
        ran1 , ran2 = ora.scrap.get_range(self.get_date)
        img, text = ora.scrap.img_or_txt(self.search_word,ran1,ran2)
        ora.Insert_m(ran1,ran2,img[:5],text[:5])
        for index, file in enumerate(img, 1):
            urllib.request.urlretrieve(file, 'c:/ENCORE1/' + str(index) + f'_{self.search_word}.jpg')
        with open(f'c:/ENCORE1/{self.search_word}.txt', 'w', encoding='utf-8') as f:
            f.writelines(text)

    # 닫기 버튼 (DB 옆)
    def con4(self):
        msgbox.showinfo('알림', '종료합니다')
        self.window.destroy()





    # 확인버튼 입력할 때 결과바디
    def search_btn(self):
        self.search_word = self.search_result.get()
        second_from_GUI = self.search_word
        ora = db_sync.OraDb(second_from_GUI)
        second_from_GUI = ora.Create_table()
        self.window.destroy()
        window2 = Window2(second_from_GUI)

        window2.show_result_window2(self.search_word)


    def show_result_window2(self, search):
        self.search_word = search


        # 데이터 입력받는다고 가정
        data = self.data
        rows = data[1:]



        photo1 = PhotoImage(file='bgw.png', master=self.window)
        label1 = Label(self.window, image=photo1)
        label1.place(x=0, y=0)

        photo2 = PhotoImage(file='pic1.png', master=self.window)
        label2 = Label(self.window, image=photo2, borderwidth=0)
        label2.place(x=0, y=1.5)

        # 검색어 입력받기
        self.search_result = Entry(self.window, width=100, font=('나눔고딕', 10), bg='white', borderwidth=1)
        self.search_result.place(x=190, y=20, width=370, height=33)

        # 검색 버튼 띄우기 (작동안함) -> DB로 테이블 ID 보내기 (뒤에)
        btn_search1 = Button(self.window, font=('나눔고딕', 9), text='검색', command=self.search_btn)
        btn_search1.place(x=570, y=20, width=50, height=34)

        # 되돌리기 버튼 띄우기
        btn_search2 = Button(self.window, font=('나눔고딕', 9), text='첫페이지', command=self.window.destroy)
        btn_search2.place(x=630, y=20, width=50, height=34)

        # 현재 검색어 표시
        sw1 = Label(self.window, text='검색어', width=5, bg='white', font=('나눔고딕', 13))
        sw1.place(x=20, y=70)
        sw2 = Label(self.window, text=self.search_word, width=10, fg='blue', bg='white' , font=('나눔고딕', 13))
        sw2.place(x=80, y=70)

        # ------------------------------DB 설정------------------------------------------------
        # 프레임 생성
        top_frame = Frame(self.window)
        top_frame.place(x=25, y=105)  # 표 위치 임의로 설정

        s = ttk.Style()
        s.configure('Treeview', rowheight=30)

        # 컬럼 설정
        tree = ttk.Treeview(top_frame, columns=(0, 1, 2, 3, 4 ,5), show='headings')
        tree.pack(side='left')

        # 컬럼명
        tree.heading(0, text='인덱스')
        tree.heading(1, text='PK')
        tree.heading(2, text='시작범위')
        tree.heading(3, text='종료범위')
        tree.heading(4, text='텍스트 조회')
        tree.heading(5, text='이미지 조회')

        # 컬럼 높이, 너비 설정
        tree.column(0, width=30)
        tree.column(1, width=100)
        tree.column(2, width=100)
        tree.column(3, width=100)
        tree.column(4, width=100)
        tree.column(5, width=200)

        # 스크롤바 설정 (https://myinbox.tistory.com/154)
        scroll1 = ttk.Scrollbar(top_frame, orient='vertical', command=tree.yview)
        scroll1.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scroll1.set)

        words =[]
        for i in rows:
            for j in i:
                tree.insert('', 'end', values=(j[0], j[1], j[2], j[3], j[4], j[5]))
                words.append(j[4])

        # 워드클라우드
        font_path = 'C:/Windows/Fonts/NGULIM.TTF'  # 사용자별 변경
        w1 = WC(font_path)
        w1.save_word_cloud(words, self.search_word)
        self.img = f'{self.search_word}.jpeg'



        # ------------------------------이미지 설정------------------------------------------------
        # 워드클라우드 사진 올리기(resize 자유롭게 하기 위해 PIL-ImageTK사용)
        try:
            load = Image.open(self.img).resize((650, 190)) ####
            image = ImageTk.PhotoImage(load, master=self.window)
            img = Label(self.window, image=image, borderwidth=5)
            img.image = image
            img.place(x=24, y=350)

        except Exception as E:
            load = Image.open('boundary.png').resize((650, 190))
            image = ImageTk.PhotoImage(load, master=self.window)

            img = Label(self.window, image=image, borderwidth=5)
            img.image = image
            img.place(x=24, y=350)

        # ----------------- 기간 설정 --------------------------------------------

        photo3 = PhotoImage(file='boundary.png', master=self.window)
        label3 = Label(self.window, image=photo3, borderwidth=0)
        label3.place(x=24, y=565)

        frame_option = Label(self.window, text='[추가 정보 갱신을 원하시면 정보를 입력해주세요]', width=33, bg='white', font=('나눔고딕', 10))
        frame_option.place(x=40, y=555)

        # 기간 선택 여부
        period_yesno = Label(self.window, text='기간 선택 여부', width=10, bg='white', font=('나눔고딕', 8))
        period_yesno.place(x=45, y=580)

        # yes or no 선택
        self.sp = ['No', 'Yes']
        self.selc_period = ttk.Combobox(self.window, state='readonly', values=self.sp, width=7)
        self.selc_period.current(0)
        self.selc_period.place(x=50, y=600)

        # year선택, month선택, day선택
        select_year = list(range(1990, dt.now().year + 1))
        select_month = list(range(1, 13))
        select_day = list(range(1, 32))
        #select_month2 = list(range(1, 13))
        #select_day2 = list(range(1,32))


        # 시작 기간 선택
        start_period = Label(self.window, text='기간 시작', width=7, bg='white', font=('나눔고딕', 8))
        start_period.place(x=135, y=580)
        self.com_p_year1 = ttk.Combobox(self.window, state='readonly', values=select_year, width=7)
        self.com_p_year1.current(0)
        self.com_p_year1.place(x=140, y=600)
        self.com_p_year1.set('년')
        self.com_p_month1 = ttk.Combobox(self.window, state='readonly', values=select_month, width=7)
        self.com_p_month1.current(0)
        self.com_p_month1.place(x=220, y=600)
        self.com_p_month1.set('월')
        self.com_p_day1 = ttk.Combobox(self.window, state='readonly', values=select_day, width=7)
        self.com_p_day1.current(0)
        self.com_p_day1.place(x=300, y=600)
        self.com_p_day1.set('일')

        # 시작과 끝 기간 구분자
        seperator2 = Label(self.window, text='-', width=1, bg='white')
        seperator2.place(x=390, y=600)

        # 끝 기간 선택
        start_period = Label(self.window, text='기간 끝', width=5, bg='white', font=('나눔고딕', 8))
        start_period.place(x=415, y=580)
        self.com_p_year2 = ttk.Combobox(self.window, state='readonly', values=select_year, width=7)
        self.com_p_year2.current(0)
        self.com_p_year2.place(x=420, y=600)
        self.com_p_year2.set('년')
        self.com_p_month2 = ttk.Combobox(self.window, state='readonly', values=select_month, width=7)
        self.com_p_month2.current(0)
        self.com_p_month2.place(x=500, y=600)
        self.com_p_month2.set('월')
        self.com_p_day2 = ttk.Combobox(self.window, state='readonly', values=select_day, width=7)
        self.com_p_day2.current(0)
        self.com_p_day2.place(x=580, y=600)
        self.com_p_day2.set('일')



        # ----------------- DB 저장 타입 설정 --------------------------------------------
        DB1 = Button(self.window, text='로컬 저장', bg='white', width=20, borderwidth=0.5, command=self.con1)
        DB1.place(x=50, y=640)


        DB2 = Button(self.window, text='DB 저장', bg='white', width=20, borderwidth=0.5, command=self.con2)
        DB2.place(x=202, y=640)


        DB3 = Button(self.window, text='둘 다 저장', bg='white', width=20, borderwidth=0.5, command=self.con3)
        DB3.place(x=354, y=640)

        DB4 = Button(self.window, text='닫기', bg='white', width=20, borderwidth=0.5, command=self.con4)
        DB4.place(x=506, y=640)


        self.window.mainloop()
