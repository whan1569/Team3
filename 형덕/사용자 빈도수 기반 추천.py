import pandas as pd
import time
import pymysql
from sqlalchemy import create_engine

# MySQL 연결 정보
host = "localhost"
database = "lg_hellovisionvod"  # 실제 MySQL 데이터베이스 이름
user = "root"
password = "admin1234"
port = "3306"

# MySQL 연결 엔진 생성
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")

# 🔹 검색할 기간 설정 (YYYYMM 형식, 범위)
search_start_month = "202301"  # 시작 월 (예: 2023년 1월)
search_end_month = "202303"  # 종료 월 (예: 2023년 6월)

# 🔹 SQL 쿼리 작성 (범위 선택)
query = f"""
SELECT user_id, movie_id, strt_dt
FROM movie_all
WHERE LEFT(strt_dt, 6) BETWEEN '{search_start_month}' AND '{search_end_month}';
"""

# 전체 실행 시간 측정 시작
start_time = time.time()

# 🔹 MySQL에서 데이터 로드
user_genre_data = pd.read_sql(query, engine)

# 🔹 검색할 사용자 ID 설정
search_user_id = "12f69e355ab709ab1c5711907526a7eb4061f817a47076d71e9ad01d0cece8b5"

# 🔹 검색 사용자가 본 영화 리스트 (고유 영화 리스트)
user_movies = user_genre_data[user_genre_data['user_id'] == search_user_id]['movie_id'].unique()
print(f"검색 사용자가 본 영화 수: {len(user_movies)}")
print(f"검색 사용자가 본 영화 리스트: {user_movies}")

# 🔹 각 사용자별로 검색 사용자와 겹치는 영화 개수 계산
grouped_users = (
    user_genre_data.groupby('user_id')['movie_id']
    .apply(set)  # 각 사용자별로 고유 영화 집합 생성
)

common_movie_counts = grouped_users.apply(lambda x: len(x.intersection(user_movies)))

# 🔹 검색 사용자와 겹치는 영화 개수 상위 20명 추출 (자기 자신 제외)
common_users_df = (
    common_movie_counts.reset_index(name='common_movie_count')
    .sort_values(by='common_movie_count', ascending=False)
)
common_users_df = common_users_df[common_users_df['user_id'] != search_user_id]
top_20_users = common_users_df.head(20)

print("상위 20명의 사용자 ID와 겹치는 영화 개수 (자기 자신 제외):")
print(top_20_users)

# 🔹 상위 20명의 사용자들이 본 영화 중 검색 사용자가 보지 않은 영화 추천
movies_by_top_20_users = user_genre_data[user_genre_data['user_id'].isin(top_20_users['user_id'])]
movies_not_watched_by_search_user = movies_by_top_20_users[~movies_by_top_20_users['movie_id'].isin(user_movies)]

recommended_movies = (
    movies_not_watched_by_search_user.drop_duplicates(subset=['user_id', 'movie_id'])
    .groupby('movie_id')
    .size()
    .reset_index(name='popularity')
    .sort_values(by='popularity', ascending=False)
    .head(20)
)

# 🔹 추천 영화 출력
print("추천 영화 리스트 (상위 20개):")
print(recommended_movies)

# 전체 실행 시간 측정 종료
end_time = time.time()
execution_time = end_time - start_time
print(f"전체 실행 시간: {execution_time:.2f}초")
