import chromadb
from sentence_transformers import SentenceTransformer
import mysql.connector
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

# ChromaDB 클라이언트 초기화 (최신 방식)
logging.info("ChromaDB 클라이언트 초기화 중...")
client = chromadb.Client()  # 최신 방식에서 그냥 기본 클라이언트로 설정

# 컬렉션 로드 또는 생성
collection_name = "movies"
logging.info(f"컬렉션 '{collection_name}' 로드 중...")
collection = client.get_or_create_collection(name=collection_name)  # 컬렉션을 불러오거나 새로 만듬
logging.info(f"컬렉션 '{collection_name}' 로드 완료.")

# 추천 함수
def recommend_content(asset):
    # asset에서 앞의 4글자 제거
    asset_id = asset[4:]
    
    # ChromaDB에서 유사한 콘텐츠 검색
    logging.info(f"asset_id '{asset_id}'와 유사한 콘텐츠 검색 중...")

    # 사용자 asset_id와 관련된 텍스트 검색
    query_text = f"asset_id: {asset_id}"

    # 쿼리 텍스트를 사용하여 검색
    results = collection.query(
        query_texts=[query_text],  # 사용자 시청 asset과 관련된 텍스트
        n_results=5
    )

    # 추천 결과 반환
    recommendations = []
    for i in range(len(results["ids"])):
        recommendations.append({
            "asset_id": results["ids"][i],
            "metadata": results["metadatas"][i]
        })
    return recommendations

# MySQL에서 사용자의 마지막 시청 asset 가져오기
logging.info("사용자 시청 기록 조회 중...")
cursor.execute("SELECT asset FROM vod_movie_11 LIMIT 1")  # 예시로 첫 번째 레코드 사용
user_asset = cursor.fetchone()[0]
logging.info(f"사용자의 마지막 시청 asset: {user_asset}")

# 추천 수행
recommendations = recommend_content(user_asset)
logging.info("추천 결과:")
for rec in recommendations:
    logging.info(f"추천 asset_id: {rec['asset_id']}, metadata: {rec['metadata']}")

# 커넥션 종료
logging.info("MySQL 커넥션 종료 중...")
cursor.close()
db.close()
logging.info("MySQL 커넥션 종료 완료.")
