import mysql.connector
import pandas as pd
from sqlalchemy import create_engine

# 105 컴퓨터에서 데이터 가져오기
host_105 = '192.168.0.105'
user = 'root'
password = '1234'
database = 'lg_hellovisionvod'

# 115 컴퓨터에 연결
host_115 = '192.168.0.115'  # 115 컴퓨터의 IP 주소
engine_115 = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host_115}/{database}')

# 105 컴퓨터에서 데이터 가져오기
engine_105 = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host_105}/{database}')

# 월별로 데이터를 반복하여 처리
for month in range(1, 12):  # 1월부터 11월까지 반복
    # 월별 조건에 맞는 SQL 쿼리
    query = f"""
        SELECT * 
        FROM vod_data
        WHERE strt_dt LIKE '2023{month:02d}%'
    """
    
    # 데이터를 105 컴퓨터에서 가져오기
    df = pd.read_sql(query, engine_105)

    # strt_dt를 텍스트 형식으로 처리 (변환하지 않고 그대로 둡니다)
    df['strt_dt'] = df['strt_dt'].astype(str)

    # 테이블명: vod_data_2023mm 형식
    table_name = f"vod_data_2023{month:02d}"

    # 데이터가 비어있는지 확인
    if df.empty:
        print(f"{table_name}에 데이터가 없습니다.")
    else:
        # 데이터를 청크 단위로 나누어 삽입
        try:
            for i in range(0, len(df), 1000):
                chunk = df.iloc[i:i+1000]
                chunk.to_sql(table_name, engine_115, if_exists='append', index=False)
                print(f"청크 {i//1000 + 1}이 {table_name} 테이블에 115 서버에 저장되었습니다.")
        except Exception as e:
            print(f"테이블 {table_name}에 데이터를 저장하는데 오류가 발생했습니다: {e}")
