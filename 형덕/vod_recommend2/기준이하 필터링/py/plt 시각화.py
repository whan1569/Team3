import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc

# 한글 폰트 설정 (Windows 환경에서 맑은 고딕 사용)
plt.rc('font', family='Malgun Gothic')

# CSV 파일 경로
file_path = r"C:\Users\USER\Desktop\vod_recommend\기준이하 필터링\shrt_watch\short_watch_resumed_with_ratio.csv"

# CSV 파일 불러오기
try:
    data = pd.read_csv(file_path)

    # 필요한 컬럼 추출 및 결측치 제거
    data_filtered = data[["first_watch_time", "watch_ratio"]].dropna()

    # 시간 구간 설정
    bins = [0, 60, 120, 180, 240, 300]
    labels = ["0~60초", "61~120초", "121~180초", "181~240초", "241~300초"]

    # 데이터 구간화
    data_filtered["time_group"] = pd.cut(data_filtered["first_watch_time"], bins=bins, labels=labels, right=False)

    # 구간별 평균 watch_ratio 계산
    mean_watch_ratios = data_filtered.groupby("time_group")["watch_ratio"].mean()

    # 그래프 그리기
    plt.figure(figsize=(10, 6))
    mean_watch_ratios.plot(kind="bar", rot=0)
    plt.title("기준이하 필터링\n시간 구간별 평균 시청 비율")  # 제목 설정
    plt.xlabel("first_watch_time")  # X축 이름 설정
    plt.ylabel("watch_ratio")  # Y축 이름 설정
    plt.xticks(ticks=range(len(labels)), labels=labels, rotation=0)  # X축 레이블 수정
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()

except FileNotFoundError:
    print("지정된 파일 경로를 찾을 수 없습니다. 경로를 확인하고 다시 시도해주세요.")
except Exception as e:
    print(f"오류 발생: {e}")
