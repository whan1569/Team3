import pandas as pd

# CSV 파일 경로
not_resumed_file = r"C:\Users\USER\Desktop\근거자료\shrt_watch\short_watch_not_resumed1_0_600.csv"
resumed_file = r"C:\Users\USER\Desktop\근거자료\shrt_watch\short_watch_resumed1_0_600.csv"

# CSV 파일 로드
not_resumed_df = pd.read_csv(not_resumed_file)
resumed_df = pd.read_csv(resumed_file)

# 시청 비율 계산 (Watch Ratio)
# total_watch_time / disp_rtm_seconds * 100
not_resumed_df['watch_ratio'] = (not_resumed_df['total_watch_time'] / not_resumed_df['disp_rtm_seconds']) * 100
resumed_df['watch_ratio'] = (resumed_df['total_watch_time'] / resumed_df['disp_rtm_seconds']) * 100

# 계산된 결과를 새로운 CSV 파일로 저장
not_resumed_df.to_csv(r"C:\Users\USER\Desktop\근거자료\shrt_watch\short_watch_not_resumed_with_ratio.csv", index=False, encoding='utf-8')
resumed_df.to_csv(r"C:\Users\USER\Desktop\근거자료\shrt_watch\short_watch_resumed_with_ratio.csv", index=False, encoding='utf-8')

print("시청 비율 계산 완료! 결과가 다음 파일로 저장되었습니다:")
print("- short_watch_not_resumed_with_ratio.csv")
print("- short_watch_resumed_with_ratio.csv")
