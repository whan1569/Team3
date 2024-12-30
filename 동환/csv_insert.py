import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# CSV 파일 경로
file_path = r"C:\Users\USER\Desktop\lg자료\(2기) DX데이터스쿨_VOD\4월\VOD시청_4월.csv"

# MySQL 연결 문자열
host = "localhost" 
database = "lg_hellovisionvod"  # 실제 MySQL 데이터베이스 이름으로 수정
user = "root"
password = "admin1234"
port = "3306"  # MySQL 기본 포트

# SQLAlchemy 엔진 생성
engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}')

# 청크 크기 설정
chunk_size = 1000  # 한 번에 처리할 행의 개수

try:
    # CSV 파일 읽기
    df_iter = pd.read_csv(file_path, chunksize=chunk_size)  # 청크 크기만큼 읽기

    # 연결 및 데이터 삽입
    with engine.connect() as connection:
        trans = connection.begin()  # 트랜잭션 시작

        try:
            for chunk in df_iter:
                # 청크별로 데이터 삽입
                chunk.to_sql(
                    name='vod_detail4',
                    con=connection,
                    index=False,
                    if_exists='append',  # 테이블이 없으면 생성, 있으면 데이터 추가
                    method='multi'
                )
            trans.commit()  # 성공 시 커밋
            print("데이터가 성공적으로 삽입되었습니다!")

        except SQLAlchemyError as e:
            trans.rollback()  # 오류 발생 시 롤백
            print(f"SQLAlchemy 오류 발생: {e}")  # 상세 오류 메시지 제한적으로 출력

except FileNotFoundError:
    print("CSV 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
except Exception as e:
    print(f"오류가 발생했습니다: {e}")  # 일반 예외 메시지 출력
