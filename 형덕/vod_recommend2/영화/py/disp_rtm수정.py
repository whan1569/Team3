import pandas as pd

# CSV 파일 경로
file_path = r"C:\Users\USER\Desktop\vod_data\vod_KIDS_09.csv"

# CSV 파일 읽기
data = pd.read_csv(file_path)

# disp_rtm을 초 단위로 변환
def convert_to_seconds(time_str):
    try:
        if pd.isna(time_str):
            return None  # NaN 값 처리
        # 문자열로 변환 후 ':' 기준으로 분리
        time_str = str(time_str)
        hours, minutes = map(int, time_str.split(':'))
        return hours * 3600 + minutes * 60
    except ValueError:
        # 변환 실패 시 None 반환
        return None

# disp_rtm_seconds 컬럼 추가
data['disp_rtm_seconds'] = data['disp_rtm'].apply(convert_to_seconds)

# 결과 확인
print(data.head())

# 변환된 데이터를 새로운 CSV 파일로 저장
output_file_path = r"C:\Users\USER\Desktop\vod_data\entertainment_09.csv"
data.to_csv(output_file_path, index=False)

print(f"변환된 파일이 저장되었습니다: {output_file_path}")
