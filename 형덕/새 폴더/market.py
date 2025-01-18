import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# CSV 파일 경로
file_path = r"C:\Users\USER\Desktop\lg자료\data\VOD\vod_mart_data.csv"

# MySQL 연결 문자열
host = "localhost"
database = "lg_hellovisionvod"
user = "root"
password = "admin1234"
port = "3306"

# SQLAlchemy 엔진 생성
engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}')

try:
    # CSV 파일 읽기
    df_iter = pd.read_csv(
        file_path,
        sep=',',
        quotechar='"',
        escapechar='\\',
        on_bad_lines='skip',
        engine='python',
        chunksize=1000
    )

    # MySQL 연결
    with engine.connect() as connection:
        for chunk in df_iter:
            try:
                chunk.to_sql(
                    name='vod_market',
                    con=connection,
                    index=False,
                    if_exists='append',
                    method='multi'
                )
                print("청크 데이터 삽입 성공!")

            except SQLAlchemyError as e:
                print(f"SQLAlchemy 오류 발생: {e}")
                continue

except Exception as e:
    print(f"오류가 발생했습니다: {e}")

