import mysql.connector
import pickle
import numpy as np

# MySQL 연결
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="lg_hellovisionvod"
)
cursor = db.cursor()

# 역직렬화된 벡터 데이터 로드
pickle_file_path = r"C:\Users\USER\Desktop\Team3\동환\줄거리기반 추천 전략\vectorDB\movie_vectors_batch_60.pkl"
with open(pickle_file_path, "rb") as f:
    movie_vectors = pickle.load(f)

# MySQL에서 벡터 데이터 가져오기
cursor.execute("SELECT asset_id, asset_nm, genre, rlse_year, director, actr_disp, rate, orgnl_cntry, smry FROM vod_movie")
movies_from_db = cursor.fetchall()

# 데이터 비교
mismatch_count = 0

for movie in movie_vectors:
    asset_id = movie["asset_id"]
    vector = movie["vector"]
    
    # MySQL에서 해당 asset_id로 데이터를 가져옴
    cursor.execute("""
        SELECT asset_nm, genre, rlse_year, director, actr_disp, rate, orgnl_cntry, smry
        FROM vod_movie WHERE asset_id = %s
    """, (asset_id,))
    movie_from_db = cursor.fetchone()

    if movie_from_db:
        # MySQL 데이터 unpack
        asset_nm, genre, rlse_year, director, actr_disp, rate, orgnl_cntry, smry = movie_from_db
        
        # 벡터 비교 (수치적 근사치 사용)
        if np.allclose(vector, np.array(movie["vector"])) and smry == movie["smry"]:
            print(f"asset_id {asset_id} (제목: {asset_nm}) 데이터 일치")
            print(f"  장르: {genre}, 출시 연도: {rlse_year}, 감독: {director}, 출연진: {actr_disp}, 연령 등급: {rate}, 제작 국가: {orgnl_cntry}")
            print(f"  벡터 값 및 줄거리 일치")
        else:
            print(f"asset_id {asset_id} (제목: {asset_nm}) 벡터 또는 줄거리 일치하지 않음")
            print(f"  장르: {genre}, 출시 연도: {rlse_year}, 감독: {director}, 출연진: {actr_disp}, 연령 등급: {rate}, 제작 국가: {orgnl_cntry}")
            mismatch_count += 1
    else:
        print(f"asset_id {asset_id} (제목: {movie['asset_nm']}) MySQL에 해당 데이터 없음")
        mismatch_count += 1

# 최종 결과 출력
if mismatch_count == 0:
    print("모든 데이터가 일치합니다.")
else:
    print(f"{mismatch_count}개의 데이터에서 불일치가 발생했습니다.")

# 커넥션 종료
cursor.close()
db.close()
