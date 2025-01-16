from sqlalchemy import create_engine
import pandas as pd

# SQLAlchemy 엔진 생성
engine = create_engine("mysql+pymysql://root:admin1234@127.0.0.1:3306/lg_hellovisionvod")

# disp_rtm을 초 단위로 변환
def convert_to_seconds(time_str):
    """
    시간을 'hh:mm' 형식으로 받으면 초 단위로 변환합니다.
    """
    try:
        if isinstance(time_str, str) and ":" in time_str:
            hours, minutes = map(int, time_str.split(":"))
            return hours * 3600 + minutes * 60
    except ValueError:
        return 0  # 잘못된 형식의 데이터를 처리하기 위해 기본값 반환
    return 0

# SQL 쿼리 작성
query = """
SELECT 
    genre_of_ct_cl, 
    asset_nm, 
    disp_rtm, -- disp_rtm 포함
    AVG(use_tms) AS avg_use_tms, -- 같은 asset_nm의 use_tms 평균 계산
    COUNT(*) AS view_count, 
    DATE_FORMAT(STR_TO_DATE(LEFT(strt_dt, 8), '%%Y%%m%%d'), '%%Y-%%m') AS month
FROM 
    vod_data_202301
WHERE 
    CT_CL LIKE '%%영화%%' 
    AND use_tms > 60
GROUP BY 
    month, genre_of_ct_cl, asset_nm, disp_rtm
ORDER BY 
    month, genre_of_ct_cl, view_count DESC;
"""

# 데이터 가져오기 (chunksize 사용)
dataframes = []
chunk_size = 10000  # 한 번에 가져올 행 수
chunk_number = 0  # 청크 번호 추적

try:
    # 데이터를 청크 단위로 읽어오기
    for chunk in pd.read_sql(query, engine, chunksize=chunk_size):
        # disp_rtm 컬럼을 초 단위로 변환
        if 'disp_rtm' in chunk.columns:
            chunk['disp_rtm_seconds'] = chunk['disp_rtm'].apply(convert_to_seconds)
        
        # watch_ratio 계산: use_tms 평균을 disp_rtm_seconds로 나눔
        chunk['watch_ratio'] = (chunk['avg_use_tms'] / chunk['disp_rtm_seconds']) * 100
        chunk_number += 1
        dataframes.append(chunk)
        print(f"Batch {chunk_number} 처리 완료: {len(chunk)} rows")

    # 모든 데이터를 합치기
    final_df = pd.concat(dataframes, ignore_index=True)

    # 결과를 CSV 파일로 저장
    output_path = r"C:\\Users\\USER\\Desktop\\monthly_genre_movie_viewing2.csv"
    final_df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"CSV 파일 저장 완료: {output_path}")

except Exception as e:
    print(f"오류 발생: {e}")
