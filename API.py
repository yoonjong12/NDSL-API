# API 사용
import requests
import urllib
import json
import numpy as np
import pandas as pd

# NDSL API로 특허와 논문 데이터를 받을 수 있는 모듈
# default로 제 개인 key를 넣어놨지만, 직접 객체를 선언할 때 인자로 넣어주시면 따로 설정하실 수 있습니다.
# key는 'keyValue=발급받은 키' 형태로 넣어야합니다. ex) 'keyValue=12341234'

class NDSL:
    def __init__(self, key):
        self.key = key

    # 논문를 받아오는 함수입니다
    # 인자 query는 리스트로 넣어주셔야 하며 리스트 안에는 원하는 검색어를 넣으시면 됩니다. ex) ['빅데이터','IoT']
    # 인자 directory는 csv파일의 저장 위치와 저장 형식입니다. string으로 넣어주세요 밑에서 형식을 자유롭게 바꾸셔도 됩니다. ex) './NDSL/article_'
    def getArticle(self, query, directory):
        for i in query:
            save_dir = directory + i + '.csv'
            empty = pd.DataFrame({'year': [], 'title': [], 'abstract': [], 'author': [], 'keyword': []})
            # 기존 저장된 파일은 삭제
            empty.to_csv(save_dir)

            urlFront = "http://openapi.ndsl.kr/itemsearch.do?"
            # 인증키
            key = self.key
            # 검색어
            query = "&query=" + urllib.parse.quote(i)
            # 검색대상 컨텐츠 ( ARTI=논문전체, NART=국내학위논문제외, JAKO=국내학술지, JAFO=해외학술지, CFKO=국내회의자료, CFFO=해외회의자료, DIKO=국내학위논문)
            target = "&target=JAKO"
            # 검색대상 항목 ( BI=전체, TI=제목, AB=초록, PB=발행기관, AU=저자, SN=ISSN, BN=ISBN, KW=키워드, PY=발행년도)
            searchField = "&searchField=BI"
            # 검색결과 출력건수 ( Default=10, Max=100)
            displayCount = "&displayCount="
            # 검색시작위치 ( 출력건수*페이지번호, Default=1, Max=100 displayCount가 10인 경우)
            startPos = "&startPosition="
            # 정렬항목 ( Default=정확도, pubyear=발행일(Default:내림차순), title=논문명, jtitle=저널명, NULL=정확도)
            sortBy = "&sortby="
            # 검색결과 출력형식 ( xml,json)
            returnType = "&returnType=json"
            # 검색결과 출력범위 ( simple=라이선스 미체크, advance=라이선스 체크후 url제공)
            resGroup = "&responseGroup=advance"
            # 콜백함수 ( returnType이 json경우 필수)
            callback = "&callback=true"
            url = urlFront + key + query + target + searchField + returnType + displayCount + startPos + sortBy + resGroup + callback
            parser = requests.get(url)
            res = parser.text
            #     json받아오면서 앞의 true와 괄호 생략
            parser2 = res[5:-1]
            dic = json.loads(parser2)
            #     건수
            summary = dic['resultSummary']
            totalCount = summary['totalCount']

            print(totalCount)
            start = 0
            count = int(totalCount)
            displaycount = 10
            num = int(float(count / displaycount))
            if count % displaycount != 0:
                num += 1
            for i in range(0, num):
                print("page num =" + str(i))
                start = (i * displaycount) + 1
                url = urlFront + key + query + target + searchField + returnType + displayCount + startPos + str(
                    start) + sortBy + resGroup + callback
                print(url)
                parser = requests.get(url)
                res = parser.text
                try:
                    dic = json.loads(parser2)
                except ValueError:
                    print('-----종료-----')
                    break
                parser2 = res[5:-1]
                #         print(dic['outputData'])
                for h in dic['outputData']:
                    #       발행년도
                    journalInfo = h['journalInfo']
                    year = journalInfo['year']
                    #             print(year)

                    #       논문정보
                    articleInfo = h['articleInfo']

                    #       제목
                    titleTemp = articleInfo['articleTitleInfo']
                    title = titleTemp['articleTitle']
                    print(title)

                    #       초록
                    abstractTemp = articleInfo['abstractInfo']
                    abstract = abstractTemp[0]
                    if isinstance(abstract, list):
                        abstract = 'Null'

                    #       저자
                    authorInfo = articleInfo['authorInfo']
                    #             print(type(authorInfo))
                    name = ''
                    for h in authorInfo:
                        if isinstance(h, str):
                            author = h
                        else:
                            try:
                                a = h['#text']
                            except TypeError:
                                continue
                            if name is '':
                                name += a
                            else:
                                name += ',' + a
                    author = name

                    #     키워드
                    keyword = articleInfo['keyword']
                    keywordType = type(keyword)
                    if keywordType == list:
                        keyword = "Null"
                    print('------------')
                    df = pd.DataFrame(data=np.array([[year, title, abstract, author, keyword]]))
                    df.to_csv(save_dir, sep=',', mode='a', encoding='utf-8', header=False)

    # 특허를 받아오는 함수입니다.
    # 논문함수와 크게 다른 부분은 없습니다.
    def getPatent(self, query, directory):
        for i in query:
            save_dir = directory + i + '.csv'
            empty = pd.DataFrame(
                {'issueDate': [], 'patentTitle': [], 'abstract': [], 'patentNumber': [], 'applicants': [], 'ipcInfo': []})
            empty.to_csv(save_dir)

            urlFront = "http://openapi.ndsl.kr/itemsearch.do?"
            # 인증키
            key = self.key
            # 검색어
            query = "&query=" + urllib.parse.quote(i)
            # 검색대상 컨텐츠 ( PATENT=특허전체, KPAT=한국특허전체, KUPA=한국공개특허, KPTN=한국등록특허, KUUM=한국공개실용신안, KUMO=한국등록실용실안,
            #     KODE=한국의장등록, UPAT=미국특허전체, USPA=미국등록특허, USAP=미국공개특허, JEPA=일본특허, WOPA=국제특허, EUPA=유럽특허
            target = "&target=KPTN"
            # 검색대상 항목 ( BI=전체, TI=명칭, PA=출원인, AN=출원번호, AD=출원일자, UN=공개번호, UD=공개일자, RN=등록번호, RD=등록일자, PRAN=우선권번호
            #  PRAD=우선권일자, IPN=국제출원번호, IPD=국제출원일자, IUN=국제공개번호, IUD=국제공개일자, AB=초록, IN=발명자, AG=대리인, IC=IPC분류, UC=USC분류, ID=대표IPC, MC=디자인분류, NULL=쿼리에직접작성
            searchField = "&searchField=BI"
            # 검색결과 출력건수 ( Default=10, Max=100)
            displayCount = "&displayCount=10"
            # 검색시작위치 ( 출력건수*페이지번호, Default=1, Max=100 displayCount가 10인 경우), 숫자는 공란으로 두어야함!
            startPos = "&startPosition="
            # 정렬항목 ( Default=정확도, adate=출원일자, title=명칭, aname=출원인, iname=발명자, anum=출원번호, unum=공개번호, udate=공개일자, mum=등록번호, rdate=등록일자, country=국가, ic=IPC
            sortBy = "&sortby=Default"
            # 검색결과 출력형식 ( xml,json)
            returnType = "&returnType=json"
            # 콜백함수 ( returnType이 json경우 필수)
            callback = "&callback=true"
            url = urlFront + key + query + target + searchField + returnType + displayCount + startPos + sortBy + callback
            parser = requests.get(url)
            res = parser.text
            # json받아오면서 앞의 true와 괄호 지우기
            parser2 = res[5:-1]
            dic = json.loads(parser2)
            # 건수
            summary = dic['resultSummary']
            totalCount = summary['totalCount']
            start = 0
            count = int(totalCount)
            displaycount = 10
            num = int(float(count / displaycount))
            print(num)

            if count % displaycount != 0:
                num += 1
            for i in range(0, num):  # i를 조작하여 페이지 수 조작
                print("page num =" + str(i))
                start = (i * displaycount) + 1
                url = urlFront + key + query + target + searchField + returnType + displayCount + startPos + str(
                    start) + sortBy + callback
                print(url)
                parser = requests.get(url)
                res = parser.text
                parser2 = res[5:-1]
                try:
                    dic = json.loads(parser2)
                except ValueError:
                    print('-----종료-----')
                    break
                for h in dic['outputData']:
                    # 특허정보
                    patentInfo = h['patentInfo']
                    # 등록일자
                    issueDate = patentInfo['issueDate']
                    # 특허명
                    patentTitle = patentInfo['patentTitle']
                    # 초록
                    abstract = patentInfo['abstract']
                    if isinstance(abstract, list):
                        abstract = 'Null'
                    # 특허번호
                    patentNumber = patentInfo['applicationNumber']
                    # 출원인
                    applicantsInfo = patentInfo['applicantsInfo']
                    name = ''
                    for h in applicantsInfo:
                        if isinstance(h, str):
                            name = h
                        else:
                            try:
                                a = h['#text']
                            except TypeError:
                                continue
                            if name is '':
                                name += a
                            else:
                                name += ',' + a
                    applicants = name
                    # 분류코드
                    ipc_list = patentInfo['ipcInfo']
                    name = ''
                    for h in ipc_list:
                        if isinstance(h, str):
                            ipc = h
                        else:
                            try:
                                a = h['#text']
                            except TypeError:
                                continue
                            if name is '':
                                name += a
                            else:
                                name += ',' + a
                            ipc = name
                    df = pd.DataFrame(data=np.array([[issueDate, patentTitle, abstract, patentNumber, applicants, ipc]])
                                      , columns=['issueDate', 'patentTitle', 'abstract', 'patentNumber', 'applicants',
                                                 'ipcInfo'])
                    df.to_csv(save_dir, sep=',', mode='a', encoding='utf-8', header=False)