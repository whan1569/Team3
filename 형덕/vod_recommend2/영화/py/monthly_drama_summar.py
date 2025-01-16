import pandas as pd

# CSV 파일 경로
file_path = r"C:\Users\USER\Desktop\csv 모음\monthly_drama_viewing.csv"

# CSV 파일 읽기
df = pd.read_csv(file_path)

# 드라마 제목 추출 (띄어쓰기와 '회' 이전까지만 추출)
df['drama_title'] = df['asset_nm'].str.extract(r'^(.*?)(?=\s\d{1,3}회)')

# 월별로 드라마 제목별 view_count 합계 계산
monthly_summary = df.groupby(['month', 'drama_title'])['view_count'].sum().reset_index()

# 월별로 정렬
monthly_summary = monthly_summary.sort_values(by=['month', 'drama_title']).reset_index(drop=True)

# 결과를 저장
output_file_path = r"C:\Users\USER\Desktop\csv 모음\monthly_drama_summary.csv"
monthly_summary.to_csv(output_file_path, index=False)

# 결과 출력
print(monthly_summary)


