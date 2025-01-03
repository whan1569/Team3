import mysql.connector
from mysql.connector import Error

# 원격 MySQL 서버 연결
try:
    remote_connection = mysql.connector.connect(
        host="192.168.0.105",  # 원격 서버 주소
        user="root",           # 원격 서버 사용자
        password="1234",       # 원격 서버 비밀번호
        database="lg_hellovisionvod"  # 원격 DB
    )

    if remote_connection.is_connected():
        print("원격 MySQL 연결 성공")

        remote_cursor = remote_connection.cursor()

        # 월별로 데이터를 가져오는 쿼리
        for month in range(10, 13):  # 7월부터 12월까지
            month_str = f"{month:02d}"  # 월을 2자리로 포맷 (07, 08, ..., 12)
            like_pattern = f"2023{month_str}%"  # 예시: '202307%', '202308%', ...

            # SELECT 쿼리
            select_query = """
            SELECT DISTINCT sha2_hash
            FROM vod_data
            WHERE strt_dt LIKE %s;
            """

            remote_cursor.execute(select_query, (like_pattern,))  # 원격 서버에서 쿼리 실행

            # 데이터 추출
            rows = remote_cursor.fetchall()

            # 로컬 MySQL 서버에 연결
            local_connection = mysql.connector.connect(
                host="192.168.0.115",   # 로컬 서버 주소
                user="root",        # 로컬 서버 사용자
                password="1234",    # 로컬 서버 비밀번호
                database="lg_hellovisionvod"  # 로컬 DB (적절한 DB 이름으로 변경)
            )

            if local_connection.is_connected():
                print(f"로컬 MySQL 연결 성공 - 2023년 {month_str}월 데이터 삽입 중...")

                local_cursor = local_connection.cursor()

                # 데이터 삽입 쿼리 (중복된 sha2_hash 값은 무시)
                insert_query = """
                INSERT IGNORE INTO vod_user (sha2_hash)
                VALUES (%s);
                """

                # 데이터 삽입
                local_cursor.executemany(insert_query, rows)  # 여러 데이터를 한 번에 삽입
                local_connection.commit()  # 커밋

                print(f"2023년 {month_str}월 데이터 로컬 DB에 삽입 완료")

                local_cursor.close()
                local_connection.close()  # 로컬 DB 연결 종료

except Error as e:
    print(f"Error: {e}")

finally:
    if remote_connection.is_connected():
        remote_cursor.close()
        remote_connection.close()  # 원격 DB 연결 종료
        print("MySQL 연결 종료")
