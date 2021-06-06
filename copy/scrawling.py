from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import urllib.request
import datetime
import time
from collections import Counter

class Nav_scrap:

    class InvalidValue(Exception):
        def __init__(self,string):
            self.string = string
        def __str__(self):
            return self.string



    @staticmethod
    def get_range(third_input):
        now = datetime.datetime.now() #현재 시간 기준으로 추천할 것임.
        current_time = str(now.year) +'-'+ str(now.month)+'-'+ str(now.day)
        while 1:
            #문제가 되는 것 1) 날짜 형식이 맞지 않은 경우, 2)기간 구분자를 너무 많이 쓴 경우, 3)년,월,일 구분을 다른 문자를 사용해서 넣는 경우, 4)그냥 엔터친 경우   -> 잡는다
            try :
                my_input = list(third_input.split('~'))   #두개로 나눠져야.
                if len(my_input) !=2:  #두개가 아니면 -> 구분 똑바로해
                    raise Nav_scrap.InvalidValue("기간 구분을 제대로 해주세요")

                from_check = list(filter(lambda x: x.isnumeric() == False, my_input[0])) #check list -> from_에서 숫자가 아닌 경우를 걸러줌
                to_check = list(filter(lambda x: x.isnumeric() == False, my_input[1])) #check list   -> to_에서 숫자가 아닌 경우를 걸러줌

                if from_check.count('-') != 2 or len(from_check) !=2:
                    raise Nav_scrap.InvalidValue("년-월-일 구분자는 (-)을 사용해주세요.")   #사용자 지정 exception을 만들어 인풋값을 입력함으로, 특정 에러 발생시 원하는 아웃풋을 얻는다.
                if to_check.count('-') != 2 or len(to_check) !=2:
                    raise Nav_scrap.InvalidValue("년-월-일 구분자는 (-)을 사용해주세요.")


                y1,m1,d1 = my_input[0].split('-')
                y2, m2, d2 = my_input[1].split('-')
                if (int(y1) not in range(1990,now.year+1)) or (int(m1) not in range(1,13)) or (int(d1) not in range(1,32)):
                    raise Nav_scrap.InvalidValue("검색할 수 없는 기간을 선택하셨습니다.")

                if (int(y2) not in range(1990,now.year+1)) or (int(m2) not in range(1,13)) or (int(d2) not in range(1,32)):
                    raise Nav_scrap.InvalidValue("검색할 수 없는 기간을 선택하셨습니다.")

                if my_input[0] > current_time or my_input[1] > current_time :
                    raise Nav_scrap.InvalidValue("나는 미래를 예측할 순 없어요")
                from_ =(y1,m1,d1)
                to_ = (y2,m2,d2)
                # finally,
                # 1)문제 없으면 검색 시작시점을 from_ 변수에 넣어준다.
                # 2) 마찬가지로 to_에는 종료시점을 넣어준다.

            except ValueError as e:
                print("기간 구분은 (~)을 사용해 주세요")
            except Nav_scrap.InvalidValue as i:
                print(i)
            else:
                break
        return from_,to_

    @staticmethod
    def get_url(search,ran1,ran2): # get_range()[0],get_range()[1]
        #range_ = Nav_scrap.get_range()
        y1, m1, d1 = ran1
        y2, m2, d2 = ran2
        #-------------------------------------


        binary = "C:\chromedriver_win32\chromedriver.exe" #<< 구글 가동
        webbrowser = webdriver.Chrome(binary)
        webbrowser.get("https://www.naver.com/") #시작 페이지  #저희는 정말 '시작부터' 했슴

        mouse = webbrowser.find_element_by_class_name("input_text") #<<마우스 갖다 댐
        mouse.send_keys(search)
        mouse.submit()

        #get the current url
        #print(webbrowser.current_url) #this's enabling us to tell where we are right now.

        webbrowser.find_element_by_link_text('이미지').click() #지정한 텍스트가 있는 곳을 클릭한다.
        time.sleep(2) #화면 넘어가주는 겸 쉬어주고
        webbrowser.find_element_by_xpath('//*[@id="snb"]/div[1]/div/div[3]/a').click()#옵션 -> 직접입력
        webbrowser.find_element_by_xpath('//*[@id="snb"]/div[2]/ul/li[2]/div/div[1]/a[8]').click()#직접입력 -> 펼치기

        time.sleep(1)

        #from
        webbrowser.find_element_by_xpath(f'//*[@id="snb"]/div[2]/ul/li[2]/div/div[2]/div[2]/div[1]/div/div/div/ul/li[{eval(y1)-1989}]').click() #1990년 =1  2021 -1990
        webbrowser.find_element_by_xpath(f'//*[@id="snb"]/div[2]/ul/li[2]/div/div[2]/div[2]/div[2]/div/div/div/ul/li[{m1}]').click() #4월 1~12
        time.sleep(2)
        webbrowser.find_element_by_xpath(f'//*[@id="snb"]/div[2]/ul/li[2]/div/div[2]/div[2]/div[3]/div/div/div/ul/li[{d1}]/a').click() #11일
        time.sleep(2)

        #to
        webbrowser.find_element_by_xpath('//*[@id="snb"]/div[2]/ul/li[2]/div/div[2]/div[1]/span[3]/a').click() #가고싶은 월 정하기 전
        time.sleep(1)
        webbrowser.find_element_by_xpath(f'//*[@id="snb"]/div[2]/ul/li[2]/div/div[2]/div[2]/div[1]/div/div/div/ul/li[{eval(y2)-1989}]').click()  # 2009년
        webbrowser.find_element_by_xpath(f'//*[@id="snb"]/div[2]/ul/li[2]/div/div[2]/div[2]/div[2]/div/div/div/ul/li[{m2}]').click()  # 7월 1~12
        webbrowser.find_element_by_xpath(f'//*[@id="snb"]/div[2]/ul/li[2]/div/div[2]/div[2]/div[3]/div/div/div/ul/li[{d2}]/a').click()  # 25일
        time.sleep(2)

        #선택
        webbrowser.find_element_by_xpath('//*[@id="snb"]/div[2]/ul/li[2]/div/div[2]/div[3]/button').click() #이동!
        time.sleep(1)


        #extraction!
        for i in range(2):
            webbrowser.find_element_by_xpath("//body").send_keys(Keys.END) #드래그를 내리겠다.
            time.sleep(1)
        time.sleep(2)
        source = webbrowser.page_source #소스페이지 얻기 Ctrl + U
        soup = BeautifulSoup(source,'lxml') #파싱한다.
        # #'lxml' <-when things get less organized
        # #html.parser
        # #html5lib   < - Extremely lenient, Parses pages the same way a web browser does, Creates valid HTML5

        return soup

    @staticmethod
    def html_img(search,ran1,ran2):
        soup = Nav_scrap.get_url(search,ran1,ran2) #해당 페이지 소스를 저장
        list_img = soup.find_all('img') #그러나 img 태그 안에는 링크도있고, 텍스트도 있고 'src'가 있는데도 링크가 없는 것도 있고.
        #print(list_img)
        images = [ i.get("src") for i in list_img if i.get("src") != None and "http" in i.get("src")]   #2 img.   #src중에서 http가 있어서 링크 연결할 수 있는 놈만 뺀다.
        txt = [i.get("alt") for i in list_img if i.get('alt')!=None and search in i.get('alt')]  # 2alt         # alt 이용해 텍스트 분리시키겠다.

        return images,txt #분류 끝

    @staticmethod
    def img_or_txt(search,ran1,ran2):

        images, txt = Nav_scrap.html_img(search, ran1, ran2) #스크래핑 먼저.
        txt = [i[0] for i in Counter(txt).most_common(30)]

        return images,txt
        #사용자 GUI 인풋