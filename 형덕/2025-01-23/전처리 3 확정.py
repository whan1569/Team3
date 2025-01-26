import pandas as pd
from sqlalchemy import create_engine, text
from sklearn.decomposition import TruncatedSVD

# MySQL 연결 정보 설정
host = "192.168.0.105"
port = 3306
user = "root"
password = "1234"
database = "lg_hellovisionvod"

# SQLAlchemy 엔진 생성
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")

# SQL 쿼리 작성
query = """
SELECT 
    sha2_hash AS user_id,              -- 사용자 ID
    asset_nm AS movie_id,              -- 영화 이름
    genre_of_ct_cl AS genre,           -- 장르
    use_tms,                           -- 시청 시간 (초)
    disp_rtm,                          -- 상영 시간 (시간 형식)
    strt_dt,                           -- 시작 날짜 및 시간
    TIME_TO_SEC(STR_TO_DATE(disp_rtm, '%H:%i')) AS disp_rtm_seconds -- 상영 시간을 초로 변환
FROM (
    SELECT sha2_hash, asset_nm, genre_of_ct_cl, use_tms, disp_rtm, strt_dt 
    FROM vod_movie_01
    WHERE use_tms > 60 AND asset_nm NOT LIKE '%예고%'
    UNION ALL 
    SELECT sha2_hash, asset_nm, genre_of_ct_cl, use_tms, disp_rtm, strt_dt 
    FROM vod_movie_02
    WHERE use_tms > 60 AND asset_nm NOT LIKE '%예고%'
    UNION ALL
    SELECT sha2_hash, asset_nm, genre_of_ct_cl, use_tms, disp_rtm, strt_dt 
    FROM vod_movie_03
    WHERE use_tms > 60 AND asset_nm NOT LIKE '%예고%'
    UNION ALL
    SELECT sha2_hash, asset_nm, genre_of_ct_cl, use_tms, disp_rtm, strt_dt 
    FROM vod_movie_04
    WHERE use_tms > 60 AND asset_nm NOT LIKE '%예고%'
    UNION ALL 
    SELECT sha2_hash, asset_nm, genre_of_ct_cl, use_tms, disp_rtm, strt_dt 
    FROM vod_movie_05
    WHERE use_tms > 60 AND asset_nm NOT LIKE '%예고%'
    UNION ALL
    SELECT sha2_hash, asset_nm, genre_of_ct_cl, use_tms, disp_rtm, strt_dt 
    FROM vod_movie_06
    WHERE use_tms > 60 AND asset_nm NOT LIKE '%예고%'
    UNION ALL
    SELECT sha2_hash, asset_nm, genre_of_ct_cl, use_tms, disp_rtm, strt_dt 
    FROM vod_movie_07
    WHERE use_tms > 60 AND asset_nm NOT LIKE '%예고%'
) AS combined_data;
"""

# 1. 데이터 가져오기
try:
    user_genre_data = pd.read_sql(text(query), engine)
    print("데이터 로드 완료")
    print(user_genre_data.head())
except Exception as e:
    print(f"데이터 로드 실패: {e}")

# 2. disp_rtm을 초 단위로 변환
def convert_to_seconds(time_str):
    try:
        hours, minutes = map(int, time_str.split(":"))
        return hours * 3600 + minutes * 60
    except ValueError:
        return None

user_genre_data['disp_rtm_seconds'] = user_genre_data['disp_rtm'].apply(convert_to_seconds)

# 3. use_tms를 숫자형으로 변환
user_genre_data['use_tms'] = pd.to_numeric(user_genre_data['use_tms'], errors='coerce')

# 4. 사용자-장르 빈도수 계산
genre_count_matrix = (
    user_genre_data.groupby(['user_id', 'genre'])
    .size()
    .unstack(fill_value=0)
)

# 5. 사용자별 총 빈도수 계산
user_total_counts = genre_count_matrix.sum(axis=1)
user_total_counts_df = user_total_counts.reset_index()
user_total_counts_df.columns = ['user_id', 'total_count']
print("사용자별 총 빈도수:")
print(user_total_counts_df.head())

# 6. 유효 항목이 5개 이상인 사용자 필터링
filtered_genre_count_matrix = genre_count_matrix[user_total_counts >= 5]
print(f"필터링 전 사용자 수: {len(genre_count_matrix)}")
print(f"필터링 후 사용자 수: {len(filtered_genre_count_matrix)}")

# 7. SVD 적용
svd = TruncatedSVD(n_components=10, random_state=42)
latent_matrix = svd.fit_transform(filtered_genre_count_matrix)

# 8. SVD 결과 저장
user_factors = pd.DataFrame(latent_matrix, index=filtered_genre_count_matrix.index)
user_factors.to_csv("C:/Users/USER/Desktop/user_latent_factors_svd.csv")
print("SVD 결과 저장 완료")

# 9. 사용자-장르 빈도수 데이터 저장
filtered_genre_count_matrix.to_csv("C:/Users/USER/Desktop/user_genre_frequency_svd.csv")
print("사용자-장르 빈도수 데이터 저장 완료")

# 10. 사용자-영화-장르 데이터에 watch_ratio와 strt_dt 포함 저장
user_genre_data['watch_ratio'] = user_genre_data.apply(
    lambda row: row['use_tms'] / row['disp_rtm_seconds'] if row['disp_rtm_seconds'] > 0 else 0,
    axis=1
)

user_genre_data[['user_id', 'movie_id', 'genre', 'watch_ratio', 'strt_dt']].to_csv(
    "C:/Users/USER/Desktop/user_genre_data_with_watch_ratio.csv",
    index=False
)
print("사용자-영화-장르 데이터(watch_ratio와 strt_dt 포함) 저장 완료")
