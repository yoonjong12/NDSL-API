# 파일 정리할 때 사용
import pandas as pd
import glob
import os
from pathlib import Path

# 특허, 논문 데이터를 개인적으로 정리하고자 만든 함수들입니다.

#### IPC, 연도별 특허 데이터 정리 ####

# matrix를 만들기 위한 빈 csv파일을 만드는 함수입니다.
def saveEmpty(query, save, ipc, years):
    # matrix index용 모든 섹션
    index_dir = save + query + '/' + query + '_sort.csv'
    index_df = pd.DataFrame(0, index=ipc, columns=years)
    index_df.to_csv(index_dir, sep=',', mode='w', encoding='utf-8')


# 연도별, ipc 분류별 특허 데이터를 정리하는 함수입니다.
# query는 리스트 형태로 원소는 query를 string으로 넣어줍니다.
# load는 쉽게 말해서 NDSL API쓸 때 저장하기로한 directory입니다.
# save는 분류를 저장할 디렉토리입니다.
def sortPatent(query, load, save):  # 특허 rawdata -> query의 모든 섹션 검색 후 빈 index csv 생성-> 토대로 matrix 생성
    years = []
    totalSort = []
    dir_li = []
    for i in query:
        fileDir = load + i + '.csv'
        read = pd.read_csv(fileDir, index_col=0, engine='python', encoding='utf-8')
        ipc_info = read['ipcInfo'].values
        title = read['patentTitle'].values
        abstract = read['abstract'].values
        year = read['issueDate'].values

        years = []
        ipc_li = []

        try:
            os.mkdir(save + i)
        except:
            pass

        # 기존 파일 제거
        files = glob.glob(save + i + '/*')
        for f in files:
            os.remove(f)

        # ipc별, 연도별 특허 정리
        for a, b, c, d in zip(year, ipc_info, title, abstract):  # [21090906, [A61,A60], 특허, 초록]
            year_slc = str(a)[:4]  # 2019
            years.append(year_slc)
            ipc_splt = b.split(',')
            ipc = [i[:3] for i in ipc_splt]
            ipc = list(set(ipc))
            for b_ in ipc:
                saveDir = Path(save + i + '/' + year_slc + i + b_ + '.csv')  # 빅데이터/2019빅데이터A61.csv
                df = pd.DataFrame({'year': [a], 'ipc': [b_], 'title': [c], 'abstract': [d]})
                df.to_csv(saveDir, sep=',', mode='a', encoding='utf-8', header=False)
                ipc_li.append(b_)
        years = sorted(list(set(years)))
        ipc_li = sorted(list(set(ipc_li)))  # 중복 제거 후 보기 좋게 정렬
        saveEmpty(i, save, ipc_li, years)


#### 초록만 받아오기 ####
# 기존 특허데이터에서 제목, 초록, ipc번호만 정리합니다.
# 각 인자는 위 sortPatent와 동일합니다.
def getAb(query, load, save):
    fileName = load + query + '.csv'
    fileDir = save + query + 'Ab.csv'
    empty = pd.DataFrame({'patentNumber': [], 'patentTitle': [], 'abstract': [], 'ipcInfo': []})
    empty.to_csv(fileDir)
    read = pd.read_csv(fileName, index_col=0, engine='python', encoding='utf-8')
    a = read['patentNumber'].values  # 특허번호
    b = read['patentTitle'].values  # 특허명
    c = read['abstract'].values  # 초록가져오기
    d = read['ipcInfo'].values
    arrayA = []
    arrayB = []
    arrayC = []
    arrayD = []

    for m, n, o, p in zip(a, b, c, d):
        arrayA.append(m)
        arrayB.append(n)
        arrayC.append(o)
        arrayD.append(p)
    df = pd.DataFrame({'number': arrayA, 'name': arrayB, 'abstract': arrayC, 'ipcInfo': arrayD})
    print(df)
    df.to_csv(fileDir, sep=',', mode='a', encoding='utf-8', header=False)