import pandas as pd
from sqlalchemy import create_engine, text
from sklearn.decomposition import TruncatedSVD

# MySQL 연결 정보 설정
# MySQL 서버에 연결하기 위한 기본 정보를 설정합니다.
host = "192.168.0.105"  # MySQL 서버의 IP 주소
port = 3306             # MySQL 서버의 포트 번호 (기본값: 3306)
user = "root"           # MySQL 사용자 이름
password = "1234"       # MySQL 사용자 비밀번호
database = "lg_hellovisionvod"  # 사용할 데이터베이스 이름

# SQLAlchemy 엔진 생성
# Python과 MySQL 간의 연결을 담당하며, SQL 쿼리 실행에 사용됩니다.
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")

# SQL 쿼리 작성
# 여러 테이블(vod_movie_01 ~ vod_movie_07)에서 사용자 ID, 영화 이름, 장르 정보를 가져옵니다.
# vod_movie_04 테이블은 제외되었으며, UNION ALL로 데이터를 병합합니다.
query = """
SELECT 
    sha2_hash AS user_id,  -- 사용자 ID (해시 값으로 저장된 사용자 정보)
    asset_nm AS movie_id,  -- 영화 이름 (asset_nm 필드, 별칭으로 movie_id 사용)
    genre_of_ct_cl AS genre -- 장르 이름 (genre_of_ct_cl 필드)
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

# 1. 데이터 가져오기
try:
    # SQL 쿼리를 실행하여 데이터를 Pandas DataFrame으로 가져옵니다.
    user_genre_data = pd.read_sql(text(query), engine)
    print("데이터 로드 완료")  # 성공적으로 데이터가 로드되었음을 출력
    print(user_genre_data.head())  # 가져온 데이터의 첫 5행을 출력하여 확인
except Exception as e:
    # 데이터 로드 실패 시 발생하는 예외를 처리하고 오류 메시지를 출력합니다.
    print(f"데이터 로드 실패: {e}")

# 2. 사용자-장르 빈도수 계산
# 사용자 ID와 장르별로 데이터를 그룹화하고, 각 그룹의 데이터 개수를 계산하여 빈도수 매트릭스를 생성합니다.
genre_count_matrix = (
    user_genre_data.groupby(['user_id', 'genre'])  # user_id와 genre로 데이터를 그룹화
    .size()  # 각 그룹별 데이터 개수(빈도수)를 계산
    .unstack(fill_value=0)  # user_id를 행, genre를 열로 변환하며 빈 값은 0으로 채웁니다.
)

# 주석:
# - `.groupby(['user_id', 'genre'])`: 사용자 ID와 장르별로 데이터를 그룹화합니다.
# - `.size()`: 각 사용자-장르 조합에서 등장 횟수를 계산합니다.
# - `.unstack(fill_value=0)`: 데이터를 사용자 × 장르 매트릭스로 변환하며 NaN 값을 0으로 채웁니다.
# 결과: 사용자 × 장르의 빈도수 매트릭스 생성.

# 예시 데이터:
# | genre    | 액션 | 드라마 | 코미디 | 공포 |
# |----------|------|--------|--------|------|
# | user_id  |      |        |        |      |
# | 1        | 2    | 1      | 0      | 3    |
# | 2        | 0    | 4      | 2      | 0    |

# 3. SVD 적용
# 사용자-장르 매트릭스에 SVD(특이값 분해)를 적용하여 차원을 축소합니다.
svd = TruncatedSVD(n_components=5, random_state=42)  # 10차원으로 축소
latent_matrix = svd.fit_transform(genre_count_matrix)  # 사용자-장르 매트릭스에 SVD를 적용하여 잠재 요인 행렬 생성

# 주석:
# - `n_components=10`: 데이터를 10개의 잠재 요인으로 축소합니다.
# - `random_state=42`: 재현성을 위해 난수 시드를 고정합니다.
# - `fit_transform`: SVD 학습과 변환을 동시에 수행합니다.
# 결과: 10차원으로 축소된 사용자 잠재 요인 벡터.

# 5. SVD 결과 저장
# SVD로 축소된 사용자 잠재 요인 벡터를 CSV 파일로 저장합니다.
user_factors = pd.DataFrame(latent_matrix, index=genre_count_matrix.index)  # 사용자 ID를 인덱스로 설정
user_factors.to_csv("C:/Users/USER/Desktop/user_latent_factors_svd.csv")
print("SVD 결과 저장 완료")
# 주석: SVD로 축소된 데이터는 추천 시스템에서 유사도 계산 등에 활용됩니다.

# 6. 사용자-장르 빈도수 데이터 저장 (SVD 적용 전)
# 원본 사용자-장르 빈도수 데이터를 CSV 파일로 저장합니다.
genre_count_matrix.to_csv("C:/Users/USER/Desktop/user_genre_frequency_svd.csv")
print("사용자-장르 빈도수 데이터 저장 완료")
# 주석: SVD 적용 전 데이터를 저장하여 원본 구조를 유지하고, 분석 시 참조할 수 있습니다.

# 7. 원본 사용자-영화-장르 데이터 저장
# 사용자 ID(user_id), 영화 ID(movie_id), 장르 정보(genre)를 포함하여 원본 데이터를 CSV로 저장합니다.
user_genre_data[['user_id', 'movie_id', 'genre']].to_csv("C:/Users/USER/Desktop/user_genre_data2.csv", index=False)
print("사용자-영화-장르 원본 데이터 저장 완료")
# 주석:
# - 원본 데이터를 저장하여 사용자와 영화, 장르 간의 관계를 유지합니다.
# - 추천 시스템 또는 데이터 검증 단계에서 활용할 수 있습니다.
