from collections import Counter

import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image # 이미지를 픽셀값으로 변환
import numpy as np
from functools import reduce


class WC:

    def __init__(self, font):
        self.data = []
        self.search = ''
        self.font_path = font

    def save_word_cloud(self, data, search):
        self.data = data
        self.search = search
        words1 = []
        for i in self.data:
            for j in i:
                for k in j.split():
                    a = reduce(lambda x, y: x + y if y not in '(}-[])/\~.!|@#$%^&*' else x, k)
                    words1.append(a)
        words2 = []
        for i in words1:
            if i[0] in '(}-[])/~.!|@#$%^&*':
                i = i[1:]
            words2.append(i)
        res1 = [i for i in words2 if i != None and self.search not in i]

        res2 = Counter(res1)
        # 만들고자 하는 이미지 불러오기
        image = Image.open('./background.jpeg')
        mask = np.array(image)
        # WordCloud 생성
        wc = WordCloud(font_path = self.font_path,
                       mask = mask,
                       height = mask.shape[0],
                       width = mask.shape[1],
                       background_color='white')
        try :
            cloud = wc.generate_from_frequencies(dict(res2))
            cloud.to_file(f'{self.search}.jpeg')
        except ValueError as E:
            pass
        # 파일에 저장

