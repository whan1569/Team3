import mysql.connector
import logging
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os

# 로그 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# MySQL 연결
db = None
cursor = None
try:
    logging.info("MySQL에 연결 중...")
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="lg_hellovisionvod"
    )
    cursor = db.cursor()
    logging.info("MySQL 연결 성공.")
except mysql.connector.Error as e:
    logging.error(f"MySQL 연결 실패: {e}")
    exit()

# 사용자 시청 기록 조회
user_assets = []
try:
    logging.info("사용자 시청 기록 조회 중...")
    cursor.execute("SELECT asset FROM vod_movie_11 LIMIT 5")  # 여러 개 가져오기
    user_assets = [row[0] for row in cursor.fetchall()]
    trimmed_asset_ids = [asset[4:] for asset in user_assets]  # ID에서 필요한 부분 추출
    logging.info(f"사용자 시청 asset: {user_assets}")
    logging.info(f"Trimmed asset IDs: {trimmed_asset_ids}")
except Exception as e:
    logging.error(f"사용자 시청 기록 조회 실패: {e}")
    if cursor:
        cursor.close()
    if db:
        db.close()
    exit()

# smry 조회 및 벡터화
smry_map = {}
try:
    logging.info("smry 데이터 조회 및 벡터화 시작.")
    cursor.execute(
        "SELECT asset_id, smry FROM vod_movie WHERE asset_id IN (%s)" % 
        ', '.join(['%s'] * len(trimmed_asset_ids)), 
        tuple(trimmed_asset_ids)
    )
    results = cursor.fetchall()
    smry_map = {row[0]: row[1] for row in results}
    logging.info(f"조회된 smry 데이터: {smry_map}")
except Exception as e:
    logging.error(f"smry 데이터 조회 실패: {e}")
    if cursor:
        cursor.close()
    if db:
        db.close()
    exit()

if cursor:
    cursor.close()
if db:
    db.close()
logging.info("MySQL 연결 종료.")

# SentenceTransformer 모델 초기화
logging.info("SentenceTransformer 모델 로드 중...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# .pkl 파일에서 벡터 로드
all_vectors = []
metadata = []
try:
    logging.info("벡터DB(.pkl 파일) 로드 중...")
    vector_path = r"C:\Users\USER\Desktop\Team3\동환\줄거리기반 추천 전략\vectorDB"
    vector_files = [os.path.join(vector_path, f) for f in os.listdir(vector_path) if f.endswith('.pkl')]

    for file in vector_files:
        logging.info(f"로딩 중: {file}")
        with open(file, 'rb') as f:
            data = pickle.load(f)  # pkl 파일이 리스트라면, 직접 리스트에서 데이터를 추출해야 함
            if isinstance(data, list):
                all_vectors.extend([item['vector'] for item in data if 'vector' in item])  # 벡터 리스트를 추가
                metadata.extend([item['asset_id'] for item in data if 'asset_id' in item])  # asset_id 추가
            else:
                logging.error(f"파일 '{file}'의 데이터 형식이 리스트가 아닙니다.")
                continue

    all_vectors = np.array(all_vectors)
    logging.info("벡터DB 로드 완료.")
except Exception as e:
    logging.error(f"벡터DB 로드 실패: {e}")
    exit()

# 유사도 계산 및 추천
logging.info("유사도 계산 및 추천 시작.")
recommendations = []

for asset_id, smry in smry_map.items():
    if not smry:
        logging.warning(f"asset_id '{asset_id}'에 대한 smry 데이터가 없습니다.")
        continue
    
    try:
        smry_vector = model.encode(smry)
        # smry_vector가 numpy 배열인지 확인
        if not isinstance(smry_vector, np.ndarray):
            logging.warning(f"asset_id '{asset_id}'에 대한 벡터화된 데이터가 numpy 배열이 아닙니다.")
            continue
    except Exception as e:
        logging.warning(f"asset_id '{asset_id}'에 대한 벡터화 실패: {e}")
        continue
    
    try:
        similarities = cosine_similarity([smry_vector], all_vectors)[0]
        
        # 유사도가 올바른 형식인지 체크
        if not isinstance(similarities, np.ndarray):
            logging.warning(f"asset_id '{asset_id}'에 대한 유사도 계산 실패: 유사도가 numpy 배열이 아닙니다.")
            continue
        
    except Exception as e:
        logging.warning(f"asset_id '{asset_id}'에 대한 유사도 계산 실패: {e}")
        continue
    
    top_indices = similarities.argsort()[-5:][::-1]  # 상위 5개 유사도
    
    recommendations.append({
        "asset_id": asset_id,
        "recommendations": [(metadata[idx], similarities[idx]) for idx in top_indices]
    })

# 추천 결과 출력
logging.info("추천 결과:")
for rec in recommendations:
    logging.info(f"사용자 시청 Asset ID: {rec['asset_id']}")
    for content, score in rec['recommendations']:
        logging.info(f"  추천 콘텐츠: {content}, 유사도: {score:.4f}")
