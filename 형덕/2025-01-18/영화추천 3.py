import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
import time

# 전체 실행 시간 측정 시작
start_time = time.time()

# CSV 파일 로드
user_factors = pd.read_csv("C:/Users/USER/Desktop/user_latent_factors.csv", index_col=0)
user_genre_data = pd.read_csv("C:/Users/USER/Desktop/user_genre_data.csv")

# 검색할 사용자 ID
search_user_id = "5820da2f5e1327c9c6657ca2584f00c598b984b9f5248d29e2775d2f633c7678"

# 사용자와 영화 ID를 숫자로 매핑
user_genre_data['user_index'] = user_genre_data['user_id'].astype('category').cat.codes
user_genre_data['movie_index'] = user_genre_data['movie_id'].astype('category').cat.codes

# 희소 행렬 생성 (사용자-영화 매트릭스)
sparse_matrix = csr_matrix(
    (np.ones(len(user_genre_data)), 
     (user_genre_data['user_index'], user_genre_data['movie_index'])),
    shape=(
        user_genre_data['user_index'].nunique(), 
        user_genre_data['movie_index'].nunique()
    )
)

print(f"Sparse Matrix Shape: {sparse_matrix.shape}")

# 검색 사용자 벡터
try:
    search_user_index = user_genre_data[user_genre_data['user_id'] == search_user_id]['user_index'].iloc[0]
    target_user_vector = sparse_matrix[search_user_index]
except IndexError:
    print(f"사용자 {search_user_id}가 데이터에 존재하지 않습니다.")
    exit()

# 코사인 유사도 계산
cosine_sim = cosine_similarity(target_user_vector, sparse_matrix).flatten()

# 상위 20명의 유사 사용자
top_n_sim_indices = np.argsort(cosine_sim)[::-1][1:21]  # 본인 제외
similar_users_df = pd.DataFrame({
    'user_index': top_n_sim_indices,
    'similarity': cosine_sim[top_n_sim_indices]
})
similar_users_df['user_id'] = similar_users_df['user_index'].map(
    dict(zip(user_genre_data['user_index'], user_genre_data['user_id']))
)

# 중복해서 본 영화가 많은 사용자 계산
user_movies = user_genre_data[user_genre_data['user_id'] == search_user_id]['movie_id']
common_movies_users = user_genre_data[user_genre_data['movie_id'].isin(user_movies)]
common_user_counts = common_movies_users['user_id'].value_counts()
common_users_df = pd.DataFrame({
    'user_id': common_user_counts.index,
    'common_movie_count': common_user_counts.values
}).head(20)

# 상위 20명의 유사 사용자 그룹에서 공통적으로 본 영화 추천
similar_users_movies_all = user_genre_data[
    user_genre_data['user_id'].isin(similar_users_df['user_id'])
]['movie_id']
similar_users_common_movies = similar_users_movies_all.value_counts()  # 영화별 시청 횟수 계산
similar_users_recommended = similar_users_common_movies[
    ~similar_users_common_movies.index.isin(user_movies)  # 검색 사용자가 보지 않은 영화
].head(20).index.tolist()

# 중복 사용자 그룹에서 공통적으로 본 영화 추천
common_users_movies_all = user_genre_data[
    user_genre_data['user_id'].isin(common_users_df['user_id'])
]['movie_id']
common_users_common_movies = common_users_movies_all.value_counts()  # 영화별 시청 횟수 계산
common_users_recommended = common_users_common_movies[
    ~common_users_common_movies.index.isin(user_movies)  # 검색 사용자가 보지 않은 영화
].head(20).index.tolist()

# 전체 실행 시간 측정 종료
end_time = time.time()
execution_time = end_time - start_time

# 결과 출력
print("코사인 유사도 상위 20명의 사용자 및 유사도:")
print(similar_users_df[['user_id', 'similarity']])

print("중복해서 본 영화가 많은 사용자 상위 20명 및 중복 수:")
print(common_users_df)

print(f"추천 영화 목록 (유사도 높은 사용자 공통 영화 기반, 최대 20개): {similar_users_recommended}")
print(f"추천 영화 목록 (중복 사용자 공통 영화 기반, 최대 20개): {common_users_recommended}")
print(f"전체 실행 시간: {execution_time:.2f}초")
