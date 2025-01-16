import mysql.connector
import pandas as pd

# MySQL 연결 정보
host = "192.168.0.105"
port = 3306
user = "root"
password = "1234"
database = "lg_hellovisionvod"

# 테이블 목록
table_list = [
    "vod_movie_01", "vod_movie_02", "vod_movie_03", "vod_movie_04",
    "vod_movie_05", "vod_movie_06", "vod_movie_07", "vod_movie_08", "vod_movie_09"
]

# MySQL 연결
try:
    conn = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )
    print("MySQL 데이터베이스 연결 성공")
except mysql.connector.Error as err:
    print(f"연결 실패: {err}")
    exit()

# 존재하는 테이블 확인 및 동적 쿼리 생성
existing_tables = []
for table in table_list:
    try:
        cursor = conn.cursor()
        cursor.execute(f"SHOW TABLES LIKE '{table}';")
        if cursor.fetchone():
            existing_tables.append(table)
    except Exception as e:
        print(f"테이블 확인 중 오류 발생: {e}")
    finally:
        cursor.close()

if not existing_tables:
    print("존재하는 테이블이 없습니다.")
    conn.close()
    exit()

# 동적 쿼리 생성
union_query = " UNION ALL ".join([f"SELECT sha2_hash, genre_of_ct_cl, asset_nm FROM {table}" for table in existing_tables])

query = f"""
SELECT 
    sha2_hash, 
    genre_of_ct_cl, 
    asset_nm 
FROM (
    {union_query}
) AS combined_data;
"""

# Pandas로 데이터 로드
try:
    data = pd.read_sql(query, conn)
    print("데이터 로드 성공")
except Exception as e:
    print(f"데이터 로드 실패: {e}")
finally:
    conn.close()

# 데이터 분석 및 추천 작업
# 특정 사용자 ID
user_id = '12f69e355ab709ab1c5711907526a7eb4061f817a47076d71e9ad01d0cece8b5'

# Step 1: 사용자가 가장 많이 본 장르
user_genres = data[data['sha2_hash'] == user_id]['genre_of_ct_cl'].value_counts()
if not user_genres.empty:
    top_genre = user_genres.idxmax()
    print(f"사용자 {user_id}의 가장 많이 본 장르: {top_genre}")

    # Step 2: 해당 장르를 많이 본 사용자 찾기
    similar_users = data[(data['genre_of_ct_cl'] == top_genre) & (data['sha2_hash'] != user_id)]
    similar_users_count = similar_users['sha2_hash'].value_counts()
    print("가장 유사한 장르를 많이 본 사용자들:")
    print(similar_users_count)

    # Step 3: 동일한 영화를 본 사용자 찾기
    user_movies = set(data[data['sha2_hash'] == user_id]['asset_nm'])
    similar_user_movies = similar_users[similar_users['asset_nm'].isin(user_movies)]
    similar_user_counts = similar_user_movies['sha2_hash'].value_counts()
    print("같은 영화를 많이 본 사용자들:")
    print(similar_user_counts)

    # Step 4: 사용자가 보지 않은 영화 추천
    unseen_movies = data[
        (data['sha2_hash'].isin(similar_users_count.index)) &  # 유사한 사용자가 본 영화
        (~data['asset_nm'].isin(user_movies))  # 사용자가 보지 않은 영화
    ]['asset_nm'].unique()

    print(f"추천 영화 목록: {unseen_movies}")
else:
    print(f"사용자 {user_id}의 데이터를 찾을 수 없습니다.")
