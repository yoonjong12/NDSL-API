# NDSL-API
NDSL API를 활용한 논문, 특허 데이터 분석

## 1. API를 사용하여 데이터 받기
먼저 https://nos.ndsl.kr 에서 API 키를 발급받으세요\
발급 받은 키로 API py의 NDSL 클래스 객체를 생성합니다.

```python
from API import NDSL
ndsl = NDSL('keyValue=12341234')
```

그리고 원하는 검색 키워드를 list형태로 만들어주세요\
ex) input: '드론 증강현실 드론 자율주행' -> query = ['드론','증강현실','드론','자율주행']\
load 변수는 제공받은 데이터를 저장할 디렉토리입니다. 저는 개인적으로 키워드 앞에 'patent_'를 붙여서 저장했습니다.\
NDSL 클래스에는 getArticle, getPatent 함수 2가지가 있습니다. 각각 논문, 특허를 받아오는 함수입니다.\
함수의 자세한 부분은 코드를 참조하시면 됩니다.
```python
query = input().split()
load = 'patent_'
ndsl.getPatent(query, load)
```
## 2. 데이터 분류
etc에는 제가 개인적으로 분석의 용이성을 위해서 만든 함수 몇 가지가 있습니다.

> ipc별, 연도별 데이터 정리
```python
import etc
etc.sortPatent([query[0]], load, 'temp')
```

> #특허 초록만 정리
```python
import etc
etc.getAb(query[0], load, 'abstract/patent_')
```
## 3. 전처리
데이터를 전처리하고, Konlpy를 사용하여 토크나이징을 할 수 있습니다.
Konlpy는 https://konlpy.org/ 를 참고해주세요. 

```python
import preprocessing
from konlpy.tag import Okt

pre = preprocessing.Preprocess(okt)
pre.getToken([query[0]], 'abstract/patent_', 'abstract/patent_')
```

## 4. 토픽모델링
지금까지 진행한 과정을 거쳐서 얻은 데이터로 토픽모델링을 진행했습니다.
자세한 내용은 ipynb 파일을 확인해주세요
