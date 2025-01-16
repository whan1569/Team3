from sqlalchemy import create_engine
import pandas as pd

# SQLAlchemy 엔진 생성
engine = create_engine("mysql+pymysql://root:1234@192.168.0.105:3306/lg_hellovisionvod")

# SQL 쿼리 작성
query = """
SELECT sha2_hash, asset_nm, use_tms, disp_rtm, CT_CL
FROM vod_data
WHERE CT_CL = '영화';
"""

try:
    # MySQL 데이터 읽기
    df = pd.read_sql(query, engine)

    # disp_rtm을 초 단위로 변환
    def convert_to_seconds(time_str):
        if isinstance(time_str, str) and ":" in time_str:
            parts = list(map(int, time_str.split(":")))
            if len(parts) == 2:  # 분:초 형식
                minutes, seconds = parts
                return minutes * 60 + seconds
            elif len(parts) == 3:  # 시:분:초 형식
                hours, minutes, seconds = parts
                return hours * 3600 + minutes * 60 + seconds
        return 0

    df['disp_rtm_seconds'] = df['disp_rtm'].apply(convert_to_seconds)

    # use_tms가 60초 이하인 데이터 제거
    df = df[df['use_tms'] > 60]

    # 동일 사용자가 동일 콘텐츠를 본 횟수 계산
    df['view_count'] = df.groupby(['sha2_hash', 'asset_nm'])['use_tms'].transform('count')

    # 각 사용자-콘텐츠 단위의 총 시청 시간 계산
    df['total_watch_time'] = df.groupby(['sha2_hash', 'asset_nm'])['use_tms'].transform('sum')

    # 각 사용자-콘텐츠 단위의 총 시청 비율 계산
    df['total_watch_ratio'] = df['total_watch_time'] / df['disp_rtm_seconds']

    # 각 시청 기록의 시청 비율 계산
    df['watch_ratio'] = df['use_tms'] / df['disp_rtm_seconds']

    # 단일 시청자 처리
    # 0.6 이상 시청한 단일 시청자
    df['is_single_high_watch'] = (df['view_count'] == 1) & (df['watch_ratio'] >= 0.6)

    # 0.6 미만 시청한 단일 시청자
    df['is_single_low_watch'] = (df['view_count'] == 1) & (df['watch_ratio'] < 0.6)

    # 다중 시청자 처리
    # 0.3~0.5 비율의 다중 시청자 (중간 재시청)
    df['is_mid_rewatch'] = (df['view_count'] >= 2) & (df['total_watch_ratio'] >= 0.3) & (df['total_watch_ratio'] < 0.5)

    # 다중 시청자 기준 (첫 시청 0.3 미만 & 총 시청 0.5 이상)
    df['is_rewatch'] = (df['view_count'] >= 2) & (
        (df['watch_ratio'] < 0.3) & (df['total_watch_ratio'] >= 0.5)
    )

    # 탐색형 시청자 처리
    df['is_exploratory'] = ~df['is_single_high_watch'] & ~df['is_single_low_watch'] & ~df['is_rewatch'] & ~df['is_mid_rewatch']

    # 결과 확인
    print(df)

    # 결과를 CSV로 저장
    output_path = r"C:\Users\USER\Desktop\watch_analysis_detailed.csv"
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"CSV 파일 저장 완료: {output_path}")

except Exception as e:
    print(f"오류 발생: {e}")
