import mysql.connector
import pandas as pd
from sqlalchemy import create_engine

# 105 컴퓨터에서 데이터 가져오기
host_105 = '192.168.0.105'
user = 'root'
password = '1234'
database = 'lg_hellovisionvod'

# 105 연결
engine_105 = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host_105}/{database}')

# 데이터를 105 컴퓨터에서 가져옵니다.
query = "SELECT * FROM vod_data WHERE strt_dt BETWEEN '20230101' AND '20231130'"
df = pd.read_sql(query, engine_105)

# 'strt_dt'를 날짜형으로 변환
df['strt_dt'] = pd.to_datetime(df['strt_dt'], format='%Y%m%d')

# 115 컴퓨터에 연결
host_115 = '192.168.0.115'  # 115 컴퓨터의 IP 주소
engine_115 = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host_115}/{database}')

# 월별로 데이터를 나누어 저장
for month in range(1, 7):  # 1월(01)부터 11월(11)까지
    # 월별 데이터 필터링
    month_df = df[df['strt_dt'].dt.month == month]
    
    # 테이블명: vod_data_2023mm 형식
    table_name = f"vod_data_2023{month:02d}"

    # 데이터프레임을 115 MySQL 서버로 저장
    month_df.to_sql(table_name, engine_115, if_exists='replace', index=False)
    print(f"데이터가 {table_name} 테이블에 115 서버에 저장되었습니다.")
