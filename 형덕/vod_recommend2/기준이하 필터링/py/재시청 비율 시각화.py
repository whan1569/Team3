import pandas as pd
import matplotlib.pyplot as plt

# CSV 파일 경로 설정
not_resumed_file = r"C:\Users\USER\Desktop\근거자료\shrt_watch\short_watch_not_resumed1_0_600.csv"
resumed_file = r"C:\Users\USER\Desktop\근거자료\shrt_watch\short_watch_resumed1_0_600.csv"
# CSV 데이터 읽기
not_resumed_df = pd.read_csv(not_resumed_file)
resumed_df = pd.read_csv(resumed_file)

# 기준 시간 구간 설정 (1분 단위, 0~600초)
thresholds = list(range(60, 301, 60))  # 1분(60초) ~ 5분(300초)

# 결과 저장 리스트
results = []

for i in range(len(thresholds)):
    lower_bound = thresholds[i - 1] if i > 0 else 0
    upper_bound = thresholds[i]

    # 각 시간 범위에 해당하는 데이터 필터링
    resumed_count = resumed_df[(resumed_df['first_watch_time'] > lower_bound) &
                               (resumed_df['first_watch_time'] <= upper_bound)].shape[0]
    not_resumed_count = not_resumed_df[(not_resumed_df['first_watch_time'] > lower_bound) &
                                       (not_resumed_df['first_watch_time'] <= upper_bound)].shape[0]

    # 다시 본 사람 비율 계산
    total_count = resumed_count + not_resumed_count
    resumed_ratio = (resumed_count / total_count) * 100 if total_count > 0 else 0

    # 결과 저장
    results.append({
        'threshold': f"{lower_bound//60}분-{upper_bound//60}분",
        'resumed_count': resumed_count,
        'not_resumed_count': not_resumed_count,
        'total_count': total_count,
        'resumed_ratio': resumed_ratio
    })

# 결과 데이터프레임 생성
results_df = pd.DataFrame(results)

# 단계 1: 충분히 본 사람 비율 저장
results_df.to_csv(r"C:\Users\USER\Desktop\resumed_ratio_analysis.csv", index=False, encoding='utf-8')
print("단계 1: Resumed Ratio 분석 결과가 CSV로 저장되었습니다!")

# 선형 그래프 시각화
plt.figure(figsize=(10, 5))
plt.plot(results_df['threshold'], results_df['resumed_ratio'], marker='o', color='blue', label='Resumed Ratio (%)')
plt.axhline(y=70, color='red', linestyle='--', label='70% 기준선')  # 70% 기준선 추가
plt.title('Resumed Ratio by Thresholds', fontsize=16)
plt.xlabel('Threshold (Minutes)', fontsize=12)
plt.ylabel('Resumed Ratio (%)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()


