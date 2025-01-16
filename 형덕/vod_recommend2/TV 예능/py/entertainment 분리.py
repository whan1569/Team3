import pandas as pd

# CSV 파일 경로
file_path = r"C:\Users\USER\Desktop\vod_data\vod_data_202309.csv"
output_path = r"C:\Users\USER\Desktop\vod_data\filtered_vod_data.csv"  # 필터링된 데이터를 저장할 경로

# CSV 파일 불러오기
try:
    # 데이터 읽기
    data = pd.read_csv(file_path)

    # CT_CL 컬럼에서 필요한 값만 필터링
    filtered_data = data[data['CT_CL'].isin(['classic', 'TV 시사/교양', 'TV 연예/오락', '다큐'])]

    # 필터링된 데이터 저장
    filtered_data.to_csv(output_path, index=False, encoding='utf-8-sig')

    print(f"필터링된 데이터를 '{output_path}'에 저장했습니다.")

except FileNotFoundError:
    print("지정된 파일 경로를 찾을 수 없습니다. 경로를 확인하고 다시 시도해주세요.")
except Exception as e:
    print(f"오류 발생: {e}")
