import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# CSV 파일 경로
csv_path = r"C:\Users\USER\Desktop\project\updated_movie_assets.csv"
output_path = r"C:\Users\USER\Desktop\project\movie_assets_with_ratings.csv"

# Selenium WebDriver 초기화
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 네이버 영화 검색 URL
base_url = "https://search.naver.com/search.naver?query=영화+({})"

# CSV 파일 읽기
df = pd.read_csv(csv_path)

# 평점과 관객수 저장 리스트
ratings = []
audiences = []

# 영화 제목으로 네이버 영화에서 평점과 관객수 크롤링
for movie in df['asset_nm']:
    try:
        # "영화 (영화 제목)" 형태로 검색
        search_query = f"영화 ({movie})"
        search_url = base_url.format(movie)
        print(f"검색 URL: {search_url}")

        # 네이버 영화 검색 URL 접속
        driver.get(search_url)
        time.sleep(2)

        # 평점 추출
        try:
            rating_element = driver.find_element(By.CLASS_NAME, "cm_icon_star")
            parent_text = rating_element.find_element(By.XPATH, "..").text.strip()
            rating = parent_text.split()[-1]
        except Exception as e:
            print(f"평점 추출 실패: {e}")
            rating = "N/A"

        # 관객수 추출
        try:
            info_groups = driver.find_elements(By.CLASS_NAME, "info_group")  # 모든 info_group 가져오기
            audience_dd = info_groups[3].find_element(By.TAG_NAME, "dd")  # 세 번째 info_group의 dd 태그
            audience = audience_dd.text.strip()
        except Exception as e:
            print(f"관객수 추출 실패: {e}")
            audience = "N/A"

        print(f"영화: {movie}, 평점: {rating}, 관객수: {audience}")
        ratings.append(rating)
        audiences.append(audience)
    except Exception as e:
        print(f"오류 발생 - 영화: {movie}, 원인: {e}")
        ratings.append("Error")
        audiences.append("Error")
    time.sleep(1)

# WebDriver 종료
driver.quit()

# 기존 데이터프레임에 평점과 관객수 컬럼 추가
df['rating'] = ratings
df['audience'] = audiences

# 업데이트된 CSV 파일 저장
df.to_csv(output_path, index=False, encoding="utf-8")
print(f"평점 및 관객수 추가 완료: {output_path}")
