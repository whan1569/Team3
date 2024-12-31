import pandas as pd
from sqlalchemy import create_engine
import os

# MySQL 연결 정보
mysql_config = {
    'user': 'root',
    'password': '1234',
    'host': 'localhost',
    'database': 'lg_hellovisionvod'
}

# SQLAlchemy 연결 문자열
engine = create_engine(f"mysql+pymysql://{mysql_config['user']}:{mysql_config['password']}@{mysql_config['host']}/{mysql_config['database']}")

# CSV 파일들이 있는 디렉토리 경로
directory_path = r"C:\\Users\\USER\\Desktop\\data"

# 테이블 이름
table_name = 'vod_mart'

# 청크 크기
chunk_size = 1000

try:
    # 디렉토리 내의 모든 CSV 파일 처리
    for filename in sorted(os.listdir(directory_path)):
        if filename.endswith(".csv") and filename.startswith("vod_mart_data"):
            file_path = os.path.join(directory_path, filename)
            print(f"처리 중: {filename}")

            # CSV 파일을 청크 단위로 읽기
            for chunk in pd.read_csv(file_path, chunksize=chunk_size, on_bad_lines='skip'):
                # 특수문자를 빈 문자열로 대체하여 생략
                chunk = chunk.replace(r'[^a-zA-Z0-9\s]', '', regex=True)
                
                # MySQL에 데이터 삽입
                chunk.to_sql(table_name, engine, if_exists='append', index=False)
                
            print(f"{filename} 처리 완료!")
except Exception as e:
    print(f"오류 발생: {e}")
