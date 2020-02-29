import numpy as np
import pandas as pd
import re

class Preprocess:
    def __init__(self, analyzer):
        # 기호에 따라 Kkma, mecab, Komoran 등 자유롭게 넣어주세요
        self.analyzer = analyzer
        self.hangul = re.compile('[^ ㄱ-ㅎㅣ가-힣 ]+$')

    # etc py파일에서 getAbstract로 처리한 파일에 이 함수를 적용하는 것을 추천합니다.
    # 특허 데이터에서 초록을 Konlpy로 Tokenizing 하는 함수입니다.
    # load_ab는 초록 데이터가 포함된 csv의 디렉토리입니다.
    # save는 Tokenizing된 데이터를 저장할 디렉토리입니다.
    def getToken(self, query, load_ab, save):
        for i in query:
            fileName = load_ab + i + 'Ab.csv'
            fileDir1 = save + i + 'Konlpy.csv'
            empty = pd.DataFrame({'num': [], 'patentNumber': [], 'patentTitle': [], 'nouns': [], 'ipcInfo': []})
            empty.to_csv(fileDir1)
            read = pd.read_csv(fileName, index_col=0, engine='python', encoding='utf-8')
            a = read['patentNumber'].values  # 번호
            b = read['patentTitle'].values  # 번호
            c = read['abstract'].values  # 초록
            d = read['ipcInfo'].values
            li = [x for x in range(len(a))]
            for m, n, o, p, z in zip(a, b, c, d, li):
                aa = m
                bb = n
                cc = o
                dd = p
                temp = self.hangul.sub(' ', cc)
                temps = self.analyzer.nouns(temp)
                li.append([temps])
                string = " ".join([k for k in temps if not k.isdigit() and len(k) >= 2])  # 명사만 한 단어로 정리
                df1 = pd.DataFrame(data=np.array([[z, aa, bb, string, dd]])
                                   , columns=['num', 'patentNumber', 'patentTitle', 'nouns', 'ipcInfo'])
                df1.to_csv(fileDir1, sep=',', mode='a', encoding='utf-8', index=False, header=False)  # 한 특허의 초록이 하나의 string으로
