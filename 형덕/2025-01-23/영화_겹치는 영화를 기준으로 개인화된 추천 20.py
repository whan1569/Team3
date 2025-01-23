import pandas as pd
import time

# 전체 실행 시간 측정 시작
start_time = time.time()

# 1. CSV 파일 로드
# 데이터는 사용자 ID(user_id), 영화 ID(movie_id) 등의 정보를 포함합니다.
user_genre_data = pd.read_csv(r"C:\Users\USER\Desktop\1-7\user_genre_data_with_watch_ratio.csv")

# 2. 검색할 사용자 ID 설정
# 분석의 기준이 되는 검색 사용자 ID를 설정합니다.
search_user_id = "12f69e355ab709ab1c5711907526a7eb4061f817a47076d71e9ad01d0cece8b5"

# 3. 검색 사용자가 본 영화 리스트 (고유 영화 리스트)
# 검색 사용자가 본 영화 ID를 고유값으로 추출합니다.
# unique()는 중복 제거된 고유한 값만 반환합니다.
user_movies = user_genre_data[user_genre_data['user_id'] == search_user_id]['movie_id'].unique()
print(f"검색 사용자가 본 영화 수: {len(user_movies)}")
print(f"검색 사용자가 본 영화 리스트: {user_movies}")

# 4. 각 사용자별로 검색 사용자와 겹치는 영화 개수 계산
# - 사용자별로 그룹화하여 고유 영화 리스트를 만듭니다.
# groupby('user_id')로 각 사용자별 데이터를 묶고, movie_id 컬럼을 set으로 변환합니다.
grouped_users = (
    user_genre_data.groupby('user_id')['movie_id']
    .apply(set)  # 각 사용자별로 고유 영화 집합 생성
)

# - 검색 사용자와 겹치는 영화 개수를 계산합니다.
# 각 사용자의 영화 집합과 검색 사용자의 영화 집합의 교집합 크기를 계산합니다.
# intersection: 두 집합의 공통 요소를 계산합니다.
common_movie_counts = grouped_users.apply(lambda x: len(x.intersection(user_movies)))

# 5. 검색 사용자와 겹치는 영화 개수 상위 20명 추출 (자기 자신 제외)
# - 공통 영화 개수를 데이터프레임으로 변환하고, 내림차순으로 정렬합니다.
# reset_index()는 Series를 데이터프레임으로 변환합니다.
common_users_df = (
    common_movie_counts.reset_index(name='common_movie_count')
    .sort_values(by='common_movie_count', ascending=False)  # 공통 영화 개수 기준으로 정렬
)
# - 검색 사용자는 제외합니다.
# 자기 자신을 제외하여 추천의 신뢰성을 높입니다.
common_users_df = common_users_df[common_users_df['user_id'] != search_user_id]
# - 상위 20명의 사용자 ID와 공통 영화 개수를 추출합니다.
top_20_users = common_users_df.head(20)
print("상위 20명의 사용자 ID와 겹치는 영화 개수 (자기 자신 제외):")
print(top_20_users)

# 6. 상위 20명의 사용자들이 본 영화 중 검색 사용자가 보지 않은 영화 추천
# - 상위 20명의 사용자가 본 영화 데이터를 필터링합니다.
# isin: 특정 사용자 ID를 기준으로 데이터를 필터링합니다.
movies_by_top_20_users = user_genre_data[user_genre_data['user_id'].isin(top_20_users['user_id'])]

# - 검색 사용자가 이미 본 영화는 제외합니다.
# ~isin: 검색 사용자가 본 영화가 아닌 데이터를 필터링합니다.
movies_not_watched_by_search_user = movies_by_top_20_users[~movies_by_top_20_users['movie_id'].isin(user_movies)]

# - 중복 제거 후 영화별 시청 횟수(인기도)를 계산합니다.
# drop_duplicates: 동일 사용자가 동일 영화를 여러 번 본 경우 중복 제거.
# groupby: 영화 ID를 기준으로 그룹화.
# size: 각 영화의 중복된 횟수를 계산하여 인기도를 측정.
recommended_movies = (
    movies_not_watched_by_search_user.drop_duplicates(subset=['user_id', 'movie_id'])  # 사용자-영화 중복 제거
    .groupby('movie_id')  # 영화별로 그룹화
    .size()  # 각 영화의 시청 횟수 계산
    .reset_index(name='popularity')  # 시청 횟수를 'popularity'로 저장
    .sort_values(by='popularity', ascending=False)  # 인기도 기준 내림차순 정렬
    .head(20)  # 상위 20개의 영화를 선택
)

# 7. 추천 영화 출력
# 추천 영화 리스트를 출력합니다.
print("추천 영화 리스트 (상위 20개):")
print(recommended_movies)

# 전체 실행 시간 측정 종료
end_time = time.time()
execution_time = end_time - start_time

# 실행 시간 출력
# 코드 실행에 걸린 총 시간을 초 단위로 출력합니다.
print(f"전체 실행 시간: {execution_time:.2f}초")
