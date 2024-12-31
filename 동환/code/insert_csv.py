import pandas as pd
from sqlalchemy import create_engine

# MySQL 연결 설정 (SQLAlchemy 사용)
db_url = 'mysql+mysqlconnector://root:1234@localhost/lg_hellovisionvod'
engine = create_engine(db_url)

# CSV 파일 경로 및 리스트
csv_files = [f"C:/Users/USER/Desktop/data/{month}_VOD.csv" for month in range(202301, 202312)]

# 데이터 삽입 함수 (청크 단위로 처리)
def insert_csv_to_mysql(file_path):
    # CSV 파일을 청크 단위로 읽어옵니다.
    for chunk in pd.read_csv(file_path, chunksize=1000):
        # 데이터프레임을 MySQL에 삽입 (테이블 이름은 'vod_data'로 가정)
        chunk.to_sql('vod_data', con=engine, if_exists='append', index=False)
        print(f"{file_path}의 데이터를 삽입했습니다.")

# 각 CSV 파일 처리
for file_path in csv_files:
    insert_csv_to_mysql(file_path)

print("모든 CSV 파일 처리 완료.")
