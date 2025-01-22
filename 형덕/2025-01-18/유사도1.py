import pandas as pd
from sqlalchemy import create_engine, text

# MySQL 연결 정보
host = "192.168.0.105"
port = 3306
user = "root"
password = "1234"
database = "lg_hellovisionvod"

# SQLAlchemy 엔진 생성
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")

# 동적 쿼리 생성 (vod_movie_04 제외)
query = """
SELECT 
    sha2_hash AS user_id,
    asset_nm AS movie_id,
    genre_of_ct_cl AS genre
FROM (
    SELECT sha2_hash, asset_nm, genre_of_ct_cl FROM vod_movie_01
    UNION ALL
    SELECT sha2_hash, asset_nm, genre_of_ct_cl FROM vod_movie_02
    UNION ALL
    SELECT sha2_hash, asset_nm, genre_of_ct_cl FROM vod_movie_03
    UNION ALL
    SELECT sha2_hash, asset_nm, genre_of_ct_cl FROM vod_movie_05
    UNION ALL
    SELECT sha2_hash, asset_nm, genre_of_ct_cl FROM vod_movie_06
    UNION ALL
    SELECT sha2_hash, asset_nm, genre_of_ct_cl FROM vod_movie_07
) AS combined_data;
"""

# 데이터 가져오기
try:
    user_genre_data = pd.read_sql(text(query), engine)
    print("데이터 로드 완료")
    print(user_genre_data.head())  # 데이터 확인
except Exception as e:
    print(f"데이터 로드 실패: {e}")

from sklearn.preprocessing import MultiLabelBinarizer

# 장르 벡터화
user_genre_data['genre_list'] = user_genre_data['genre'].str.split(',')  # 쉼표로 장르 분리
mlb = MultiLabelBinarizer()
genre_matrix = pd.DataFrame(
    mlb.fit_transform(user_genre_data['genre_list']),
    columns=mlb.classes_,
    index=user_genre_data.index
)

# 사용자-장르 행렬 생성 (asset_nm 제외)
user_genre_matrix = genre_matrix.join(user_genre_data[['user_id']]).groupby('user_id').sum()
print("사용자-장르 행렬 생성 완료")

from sklearn.decomposition import TruncatedSVD

# SVD 학습
svd = TruncatedSVD(n_components=14, random_state=42)  # 14차원으로 압축
latent_matrix = svd.fit_transform(user_genre_matrix)

# 사용자 잠재 벡터
user_factors = pd.DataFrame(latent_matrix, index=user_genre_matrix.index)
print("사용자 잠재 벡터 생성 완료")

# 사용자 잠재 벡터 저장
user_factors.to_csv("C:/Users/USER/Desktop/user_latent_factors2.csv")
print("사용자 잠재 벡터 저장 완료")

# 사용자-장르 데이터 저장 (asset_nm 포함, 벡터화 제외)
user_genre_data[['user_id', 'movie_id', 'genre']].to_csv("C:/Users/USER/Desktop/user_genre_data2.csv", index=False)
print("사용자-장르 데이터 저장 완료")
