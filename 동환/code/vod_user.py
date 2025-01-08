from sqlalchemy import create_engine, String
import mysql.connector
import pandas as pd
import re
import hashlib

# 105 컴퓨터 MySQL 연결 설정 (데이터 읽기)
db_connection_105 = mysql.connector.connect(
    host='192.168.0.105',  # 105 컴퓨터의 IP 주소
    user='root',
    password='1234',  # 105 컴퓨터 MySQL 비밀번호
    database='lg_hellovisionvod'
)

# 115 컴퓨터 MySQL 연결 설정 (SQLAlchemy 사용)
def create_db_connection():
    return create_engine('mysql+mysqlconnector://root:1234@192.168.0.115/lg_hellovisionvod')

db_connection_115 = create_db_connection()

# 테이블 목록
tables = [
    'vod_drama_06', 'vod_movie_06', 'vod_kids_06', 'vod_entertainment_06',
    'vod_drama_07', 'vod_movie_07', 'vod_kids_07', 'vod_entertainment_07',
    'vod_drama_08', 'vod_movie_08', 'vod_kids_08', 'vod_entertainment_08',
    'vod_drama_09', 'vod_movie_09', 'vod_kids_09', 'vod_entertainment_09',
    'vod_drama_10', 'vod_movie_10', 'vod_kids_10', 'vod_entertainment_10',
    'vod_drama_11', 'vod_movie_11', 'vod_kids_11', 'vod_entertainment_11'
]

# 회차 정보를 제거하는 함수 (asset_nm만 수정)
def remove_episode_info(text):
    return re.sub(r'\s[0-9]{1,3}회\([^)]*\)', '', text)

# SHA-2 해시 생성 함수
def generate_sha2_hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

# 데이터베이스 처리 및 결과를 115에 삽입
chunk_size = 1000  # 한 번에 처리할 데이터의 크기 (1000개씩 처리)

for table in tables:
    cursor_105 = db_connection_105.cursor()
    
    # 105 컴퓨터에서 데이터 가져오기
    query = f"SELECT asset_nm, asset, CT_CL, genre_of_ct_cl, use_tms, disp_rtm, strt_dt, category FROM {table}"
    cursor_105.execute(query)
    
    rows = cursor_105.fetchall()
    
    # 데이터프레임으로 변환하여 사용
    data = [
        (
            remove_episode_info(row[0]),  # 수정된 asset_nm
            row[1],  # asset
            generate_sha2_hash(row[1]),  # sha2_hash 생성
            row[2],  # CT_CL
            row[3],  # genre_of_ct_cl
            row[4],  # use_tms
            row[5],  # disp_rtm
            row[6],  # strt_dt
            row[7]   # category
        )
        for row in rows
    ]
    
    # 데이터프레임 생성
    df = pd.DataFrame(data, columns=['asset_nm', 'asset', 'sha2_hash', 'CT_CL', 'genre_of_ct_cl', 'use_tms', 'disp_rtm', 'strt_dt', 'category'])

    # 청크 단위로 데이터 삽입
    try:
        for start in range(0, len(df), chunk_size):
            chunk = df.iloc[start:start + chunk_size]
            chunk.to_sql(table, db_connection_115, if_exists='append', index=False, method='multi', dtype={
                'asset_nm': String(255),
                'asset': String(255),
                'sha2_hash': String(64),  # SHA-2 해시는 64자 길이
                'CT_CL': String(255),
                'genre_of_ct_cl': String(255),
                'use_tms': String(255),
                'disp_rtm': String(255),
                'strt_dt': String(255),
                'category': String(255)
            })
    except Exception as e:
        print(f"Error occurred while inserting data into {table}: {e}")
        db_connection_115.dispose()  # 연결을 닫고
        db_connection_115 = create_db_connection()  # 새 연결 생성

    cursor_105.close()

# MySQL 연결 종료
db_connection_105.close()

print("105에서 연산한 결과와 원본 데이터를 115 컴퓨터에 삽입 완료.")
