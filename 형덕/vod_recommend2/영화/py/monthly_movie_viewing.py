from sqlalchemy import create_engine
import pandas as pd

# SQLAlchemy 엔진 생성
engine = create_engine("mysql+pymysql://root:1234@192.168.0.105:3306/lg_hellovisionvod")

# SQL 쿼리 작성
query = """
SELECT asset_nm, COUNT(*) AS view_count, 
       DATE_FORMAT(STR_TO_DATE(LEFT(strt_dt, 8), '%%Y%%m%%d'), '%%Y-%%m') AS month
FROM vod_data
WHERE CT_CL LIKE '%%영화%%' AND use_tms > 60
GROUP BY month, asset_nm
ORDER BY month, view_count DESC;
"""

# 데이터 가져오기 (chunksize 사용)
dataframes = []
chunk_size = 10000  # 한 번에 가져올 행 수
chunk_number = 0  # 청크 번호 추적

try:
    # 데이터를 청크 단위로 읽어오기
    for chunk in pd.read_sql(query, engine, chunksize=chunk_size):
        chunk_number += 1
        dataframes.append(chunk)
        print(f"Batch {chunk_number} 처리 완료: {len(chunk)} rows")

    # 모든 데이터를 합치기
    final_df = pd.concat(dataframes, ignore_index=True)

    # 결과를 CSV 파일로 저장
    output_path = r"C:\Users\USER\Desktop\monthly_movie_viewing.csv"
    final_df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"CSV 파일 저장 완료: {output_path}")

except Exception as e:
    print(f"오류 발생: {e}")
