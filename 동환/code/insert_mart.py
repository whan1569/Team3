import pandas as pd
from sqlalchemy import create_engine
import re
import numpy as np

# MySQL 연결 설정
user = "root"
password = "1234"
host = "localhost"
database = "lg_hellovisionvod"
table_name = "vod_mart"

# MySQL 연결 문자열 생성
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

# CSV 파일 경로
file_path = r"C:\Users\USER\Desktop\data\vod_mart_data.csv"

# 특수기호 삭제 및 예외값 처리 함수
def clean_data(value):
    if pd.isnull(value):  # NaN 값 대처
        return ""  # 빈 문자열로 대처
    if isinstance(value, str):  # 문자열인 경우 특수기호 제거
        value = re.sub(r'[^\w\s]', '', value)  # 특수기호 제거
        return value.strip()  # 공백 제거
    try:
        # 값이 숫자로 변환 가능한 경우 반환
        return float(value)
    except ValueError:
        # 변환 불가능한 경우 빈 문자열로 대처
        return ""

# 에러 카운터 초기화
error_count = 0

# CSV 파일 읽기
try:
    df = pd.read_csv(
        file_path,
        sep=',',  # 쉼표 구분자
        on_bad_lines='skip',  # 문제 발생 행 건너뛰기
        encoding='utf-8',  # UTF-8 인코딩 사용
        quotechar='"'  # 따옴표 처리
    )
except Exception:
    error_count += 1

# 데이터 전처리: 특수기호 삭제 및 예외값 대처
try:
    df = df.applymap(clean_data)
except Exception:
    error_count += 1

# 모든 값을 문자열로 변환
df = df.astype(str)

# 데이터베이스에 청크 단위 삽입
chunk_size = 300  # 청크 크기 300으로 설정
try:
    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i+chunk_size]
        chunk.to_sql(name=table_name, con=engine, if_exists="append", index=False)  # method='multi' 제거
except Exception:
    error_count += 1

# 최종 에러 개수 출력
print(f"Total errors encountered: {error_count}")
