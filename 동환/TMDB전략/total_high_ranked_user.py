import pandas as pd
import glob

# CSV 파일 경로 패턴
file_pattern = 'top_sha2_hash_*.csv'

# 모든 CSV 파일 읽기
all_files = glob.glob(file_pattern)
df_list = [pd.read_csv(file) for file in all_files]

# 모든 데이터프레임을 하나로 합침
combined_df = pd.concat(df_list)

# 'sha2_hash'별로 count 합산
summed_df = combined_df.groupby('sha2_hash')['count'].sum().reset_index()

# 총 사용량이 많은 상위 10명 추출
top_10_users = summed_df.nlargest(10, 'count')

# 결과 출력 (또는 저장)
print(top_10_users)

# 결과를 CSV로 저장하고 싶다면:
top_10_users.to_csv('top_sha2_hash.csv', index=False)
