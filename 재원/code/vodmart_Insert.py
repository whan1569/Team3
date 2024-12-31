import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import logging

# CSV 파일 경로
file_path = r"C:\Users\USER\Desktop\Project\Data\3기데이터\data\vod_mart_data\vod_mart_data.csv"

# MySQL 연결 문자열
host = "localhost"
database = "lg_hellovisionvod"
user = "root"
password = "1234"
port = "3306"

# SQLAlchemy 엔진 생성
engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}')

# 로그 설정
logging.basicConfig(filename='db_insert_errors.log', level=logging.ERROR)

try:
    # CSV 파일 읽기
    df_iter = pd.read_csv(
        file_path,
        sep=',',
        quotechar='"',
        escapechar='\\',
        engine='python',
        chunksize=3000,
        na_filter=True,
        dtype = str

    )

    # MySQL 연결
    with engine.connect() as connection:
        for chunk in df_iter:
            try:
                chunk.to_sql(
                    name='vod_mart2',
                    con=connection,
                    index=False,
                    if_exists='append',
                    method='multi'
                    
                )
                print("청크 데이터 삽입 성공!")

            except SQLAlchemyError as e:
                logging.error(f"SQLAlchemy 오류 발생: {e}")
                continue

except Exception as e:
    print(f"오류가 발생했습니다: {e}")
    logging.error(f"전체 오류 발생: {e}")