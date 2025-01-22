import pandas as pd
import matplotlib.pyplot as plt

# CSV 파일 경로 설정
file_path = r"C:\Users\USER\Desktop\vod_data\vod_KIDS_09.csv"

try:
    # CSV 데이터 읽기
    df = pd.read_csv(file_path)

    # '예고'가 포함된 asset_nm 제거
    df = df[~df['asset_nm'].str.contains("예고", na=False)]

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

    df['disp_rtm_seconds'] = df['disp_rtm'].apply(convert_to_seconds)

    # 데이터 검증: 상영 시간이 0인 경우 제거
    df = df[df['disp_rtm_seconds'] > 0]

    # 동일 사용자가 동일 콘텐츠를 본 경우에 대해 총 시청 시간 계산
    user_content_stats = df.groupby(['sha2_hash', 'asset_nm']).agg(
        total_watch_time=('use_tms', 'sum'),
        disp_rtm_seconds=('disp_rtm_seconds', 'first'),
        watch_count=('use_tms', 'count'),
        first_watch_time=('use_tms', 'first')
    ).reset_index()

    # 여러 기준 테스트 (1분부터 5분까지 1분 간격)
    thresholds = list(range(0, 90, 10))  # 60초부터 300초까지 60초 간격
    results = {}

    combined_not_resumed = pd.DataFrame()
    combined_resumed = pd.DataFrame()

    for i in range(len(thresholds)):
        lower_bound = thresholds[i - 1] if i > 0 else 0  # 이전 임계값 (하한)
        upper_bound = thresholds[i]  # 현재 임계값 (상한)

        short_watch_not_resumed = user_content_stats[
            (user_content_stats['first_watch_time'] > lower_bound) &  # 하한보다 크고
            (user_content_stats['first_watch_time'] <= upper_bound) &  # 상한보다 작거나 같은
            (user_content_stats['watch_count'] == 1)                # 한 번만 시청
        ]

        short_watch_resumed = user_content_stats[
            (user_content_stats['first_watch_time'] > lower_bound) &  # 하한보다 크고
            (user_content_stats['first_watch_time'] <= upper_bound) &  # 상한보다 작거나 같은
            (user_content_stats['watch_count'] > 1)                 # 여러 번 시청
        ]

        # 결과 저장
        results[upper_bound] = {
            'not_resumed_count': len(short_watch_not_resumed),
            'resumed_count': len(short_watch_resumed),
            'not_resumed': short_watch_not_resumed,
            'resumed': short_watch_resumed
        }

        # 결과 합치기
        combined_not_resumed = pd.concat([combined_not_resumed, short_watch_not_resumed])
        combined_resumed = pd.concat([combined_resumed, short_watch_resumed])

        # 결과 출력
        print(f"기준 {lower_bound}~{upper_bound}초: 짧게 보고 중단한 사용자 수 = {len(short_watch_not_resumed)}")
        print(f"기준 {lower_bound}~{upper_bound}초: 짧게 보고 이어서 본 사용자 수 = {len(short_watch_resumed)}")

    # 기준별 데이터 저장 (0~600초로 통합 저장)
    combined_not_resumed.to_csv(r"C:\\Users\\USER\\Desktop\\short_watch_not_resumed_kids09.csv", index=False, encoding="utf-8")
    combined_resumed.to_csv(r"C:\\Users\\USER\\Desktop\\short_watch_resumed_kids09.csv", index=False, encoding="utf-8")


except Exception as e:
    print(f"오류 발생: {e}")
