import logging
import pickle

logging.basicConfig(level=logging.INFO)
file_path = 'C:\\Users\\USER\\Desktop\\Team3\\동환\\줄거리기반 추천 전략\\vectorDB\\movie_vectors_batch_1.pkl'

# 파일 경로 확인
logging.info(f"파일 경로 확인 완료: {file_path}")

try:
    # 파일 로드
    with open(file_path, 'rb') as f:
        data = pickle.load(f)
    
    logging.info(f"파일 '{file_path}' 로드 성공")
    
    # 내용의 처음 5개 항목 출력
    logging.info(f"파일 내용의 처음 2개 항목: {data[:2]}")
    
    # 벡터 내용 일부 출력 (vector 부분만)
    for item in data[:5]:  # 처음 5개 항목만 출력
        logging.info(f"asset_id: {item['asset_id']}, vector (첫 10개 값): {item['vector'][:10]}")
        
except Exception as e:
    logging.error(f"파일 로드 실패: {e}")
