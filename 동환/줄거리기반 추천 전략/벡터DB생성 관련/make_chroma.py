import mysql.connector
from sentence_transformers import SentenceTransformer
import pickle
import logging

# 로그 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# MySQL 연결
logging.info("MySQL에 연결 중...")
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="lg_hellovisionvod"
)
cursor = db.cursor()
logging.info("MySQL 연결 성공.")

# Sentence-BERT 모델 로드
logging.info("Sentence-BERT 모델 로드 중...")
model = SentenceTransformer('all-MiniLM-L6-v2')
logging.info("Sentence-BERT 모델 로드 완료.")

# MySQL에서 영화 데이터 가져오기
logging.info("영화 데이터 조회 시작...")
cursor.execute("SELECT asset_id, smry, director, actr_disp FROM vod_movie")
movies = cursor.fetchall()
logging.info(f"총 {len(movies)}개의 영화 데이터를 조회하였습니다.")

# 전처리 및 벡터화
movie_vectors = []  # 벡터화된 데이터를 담을 리스트
batch_size = 1000  # 배치 크기
logging.info(f"배치 크기 설정: {batch_size}")

for idx, movie in enumerate(movies):
    asset_id = movie[0]
    text = f"줄거리: {movie[1]} 감독: {movie[2]} 출연진: {movie[3]}"
    vector = model.encode([text])[0]  # 768차원 벡터화
    
    movie_vectors.append({
        "asset_id": asset_id,
        "vector": vector
    })
    
    # 배치 단위로 저장
    if (idx + 1) % batch_size == 0 or idx == len(movies) - 1:
        batch_num = idx // batch_size + 1
        logging.info(f"배치 {batch_num} 저장 중... (총 {len(movie_vectors)}개 항목)")
        with open(f"movie_vectors_batch_{batch_num}.pkl", "wb") as f:
            pickle.dump(movie_vectors, f)
        movie_vectors.clear()  # 메모리 절약을 위해 배치 저장 후 클리어
        logging.info(f"배치 {batch_num} 저장 완료.")

# 커넥션 종료
logging.info("MySQL 커넥션 종료 중...")
cursor.close()
db.close()
logging.info("MySQL 커넥션 종료 완료.")
