from API import NDSL
import etc
import os
import preprocessing
# Konlpy tokenizer
from konlpy.tag import Okt, Komoran, Kkma
okt = Okt()
komoran = Komoran()
kkma = Kkma()

# ex) 'keyValue=12341234' 부여받은 숫자로 교체하세요
ndsl = NDSL('keyValue=12341234')
# ex) input: '드론 증강현실 드론 자율주행' -> query = ['드론','증강현실','드론','자율주행']
query = input().split()
load = 'patent_'

#특허 받아오기
ndsl.getPatent(query, load)

#특허 정리
etc.sortPatent([query[0]], load, 'temp')

#특허 초록만 정리
try:
    os.mkdir('abstract')
except:
    pass
etc.getAb(query[0], load, 'abstract/patent_')

# 토크나이징
pre = preprocessing.Preprocess(okt)
pre.getToken([query[0]], 'abstract/patent_', 'abstract/patent_')