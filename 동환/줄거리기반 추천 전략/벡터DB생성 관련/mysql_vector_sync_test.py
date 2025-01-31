import mysql.connector
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

# 사용자 마지막 시청 기록 가져오기
logging.info("사용자 시청 기록 조회 중...")
cursor.execute("SELECT asset FROM vod_movie_11 LIMIT 1")  # 예시로 첫 번째 레코드 사용
user_asset = cursor.fetchone()[0]
trimmed_asset_id = user_asset[4:]  # 앞의 4글자 제거
logging.info(f"사용자의 마지막 시청 asset: {user_asset}, trimmed_asset_id: {trimmed_asset_id}")

# vod_movie에서 smry 가져오기
logging.info(f"asset_id '{trimmed_asset_id}'에 해당하는 smry 조회 중...")
cursor.execute("""
    SELECT m.smry
    FROM vod_movie AS m
    WHERE m.asset_id = %s
""", (trimmed_asset_id,))

smry_result = cursor.fetchone()
if smry_result:
    smry = smry_result[0]
    logging.info(f"smry 조회 성공: {smry}")
else:
    smry = None
    logging.error(f"smry를 찾을 수 없습니다. asset_id: {trimmed_asset_id}")

# 필요한 작업 추가 (벡터DB 조회나 추천 수행 등)
if smry:
    logging.info(f"smry: {smry} 기반으로 벡터DB에서 유사 콘텐츠를 검색하세요.")
    # 이후 벡터DB 로직과 통합하여 추천 수행 가능

# 커넥션 종료
logging.info("MySQL 커넥션 종료 중...")
cursor.close()
db.close()
logging.info("MySQL 커넥션 종료 완료.")
