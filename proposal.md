### 프로젝트 주제
 - 스팸메일 및 문자분류 모델 개발계획

<br>

# 팀원 / 역할
| 학번/ 이름 | 역할 |
|:---:|:---:|
| 2026065 장성훈 | 데이터셋 탐색, 프로잭트 관리, 설계 및 구현 |
| 2026112 최종호 | 학습최적 모델탐색, 데이터 전처리, 설계 및 구현 |
| 2026003 곽계영 | 테스트환경 구축, 문서화 작업, 설계 및 구현 |

<br>

### 서론
 1. 스팸메일 및 문자 차단을 위한 순환신경망 모델 개발
 2. 평소 불필요한 광고수신 문자와 스팸메일의 바이러스 및 웜에 의한 컴퓨터 보안안전을 위해 효과적인 대응 모델 개발
 3. 뉴스나 위키, 공식문서에 등장하는 정제된 데이터가 아닌 신조어, 오탈자등 공식적인 글쓰기에서 나타나지않는 표현또한 학습

<br>

### 과정
 1. spam, ham 말뭉치 데이터셋을 통해 순환신경망 학습
 2. 수집된 새로운 스팸 말뭉치 데이터를 통해 예측 수행
 3. 최신 NLP 처리 모델 (BERT, ELECTRA) 모델들을 파인튜닝하여 수집한 데이터셋을 학습
 4. 순환신경망 (LSTM, GRU, Bi-LSTM) 트랜스포머(KcELECTRA) 모델의 하이퍼 파라미터를 튜닝하며 실험
 5. 실험 결과를 버전에따라 시각화하여 저장, 가장좋은 모델구성을 선정
 6. 시각화 자료와 결과를 토대로 문서화 및 발표

<br>

### 데이터셋

 - [kaggle sms-spam-collection-dataset] (https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset?resource=download)
 - [korean-collection-dataset] https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=71788
 - 유튜브 댓글 크롤링

<br>
 
