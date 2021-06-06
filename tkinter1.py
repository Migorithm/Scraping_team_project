from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from datetime import datetime as dt
from PIL import Image, ImageTk
from tkinter2 import Window2
import db_sync
import scrapping

class Window1():
    def __init__(self):
        self.search_word = ''
        self.type = '' # DB 타입
        self.window = Tk()
        self.window.title('EncoreTeam 1')
        self.window.geometry('600x250')
        self.window.resizable(False, False)
    # DB 타입 설정

# ------------------------------------------------------------------------------------------------------------#
    def search_btn(self):
        self.search_word = self.search_result.get()

        first_from_GUI = self.search_word
        ora = db_sync.OraDb(first_from_GUI) #인스턴스 선언.  아이유

        first_from_DB = ora.Create_table()


        window2 = Window2(first_from_DB)
        window2.show_result_window2(self.search_word)
        return self.search_word

    def get_search_window1(self):
        # 배경화면 설정
        photo1 = PhotoImage(file='bgw.png', master=self.window)
        label1 = Label(self.window, image=photo1)
        label1.place(x=-2, y=0)
        photo2 = PhotoImage(file='teamwork2.png', master=self.window)
        label2 = Label(self.window, image=photo2, borderwidth=0)
        label2.place(x=-200, y=-200)
        #-------- 검색어 입력받기 -----------------------------------------------
        self.search_result = Entry(self.window, width=100, font=('나눔고딕', 10), bg='white', borderwidth=1)
        self.search_result.place(x=40, y=150, width=480, height=40)
        # 검색 버튼 띄우기
        btn_search = Button(self.window, font=('나눔고딕', 10), text='검색', command=self.search_btn)

        # command=lambda: [search_btn(), start_window2()])
        btn_search.place(x=520, y=150, width=50, height=41)

        self.window.mainloop()

