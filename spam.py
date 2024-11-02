import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import urllib.request
import json
import csv
import os

directory_path = './Sample/Sample/02.라벨링데이터/2. 유해질의 데이터/스팸및광고'


# 헤더작성
with open('test.csv', 'w', newline='', encoding='utf-8') as output_file:
    f = csv.writer(output_file)
    f.writerow(["스팸및광고", "내용"])
    
# JSON 파일의 개수를 저장할 변수
json_file_count = 0

# 디렉토리 내 모든 파일을 순회
for filename in os.listdir(directory_path):
    # 파일 확장자가 .json인 파일만 선택
    if filename.endswith('.json'):
        file_path = os.path.join(directory_path, filename) # 파일경로 결합

        # JSON 파일을 열고 내용 확인
        with open(file_path, 'r', encoding='utf-8') as input_file, open('test.csv', 'a', newline="", encoding='utf-8') as output_file :
            data = json.load(input_file)

            f = csv.writer(output_file)

            for line in data["data"]:
                f.writerow([line["instruct_id"], line["instruct_text"]])

        json_file_count += 1

print(f"디렉토리 내 원본 JSON 파일의 수: {json_file_count}")

p_data = pd.read_csv("./test.csv", encoding='utf-8')
print(p_data.head())