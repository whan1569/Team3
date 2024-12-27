import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# CSV 파일 경로
file_path = r"C:\Users\USER\Desktop\lg자료\data\VOD\vod_mart_data.csv"

# MySQL 연결 문자열
host = "localhost"
database = "lg_hellovisionvod"  # 실제 MySQL 데이터베이스 이름
user = "root"
password = "admin1234"
port = "3306"  # MySQL 기본 포트

# SQLAlchemy 엔진 생성
engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}')

# 청크 크기 설정
chunk_size = 1000  # 한 번에 처리할 행의 개수

try:
    # CSV 파일 읽기
    df_iter = pd.read_csv(file_path, chunksize=chunk_size)  # 청크 단위로 읽기

    # MySQL 연결
    with engine.connect() as connection:
        for chunk in df_iter:
            try:
                # 트랜잭션 시작
                trans = connection.begin()
                
                # 청크별 데이터 삽입
                chunk.to_sql(
                    name='vod_market',
                    con=connection,
                    index=False,
                    if_exists='append',  # 테이블이 없으면 생성, 있으면 데이터 추가
                    method='multi'
                )
                
                # 트랜잭션 커밋
                trans.commit()
                print("청크 데이터 삽입 성공!")

            except SQLAlchemyError as e:
                # 트랜잭션 롤백
                trans.rollback()
                print(f"SQLAlchemy 오류 발생: {e}")
                continue  # 다음 청크로 진행

except FileNotFoundError:
    print("CSV 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
except Exception as e:
    print(f"오류가 발생했습니다: {e}")
