import mysql.connector
from mysql.connector import Error

# MySQL 연결
try:
    connection = mysql.connector.connect(
        host="192.168.0.105", 
        user="root", 
        password="1234", 
        database="lg_hellovisionvod"
    )

    if connection.is_connected():
        print("MySQL 연결 성공")

        cursor = connection.cursor()

        # 월별로 데이터를 삽입하는 쿼리
        for month in range(2, 13):  # 1부터 12까지
            month_str = f"{month:02d}"  # 월을 2자리로 포맷 (01, 02, ..., 12)
            like_pattern = f"2023{month_str}%"  # 예시: '202301%', '202302%', ...

            # INSERT 쿼리 (중복된 sha2_hash 값은 무시)
            insert_query = """
            INSERT IGNORE INTO vod_user (sha2_hash)
            SELECT DISTINCT sha2_hash
            FROM vod_data
            WHERE strt_dt LIKE %s;
            """

            cursor.execute(insert_query, (like_pattern,))  # 쿼리 실행

            # 변경 사항 커밋
            connection.commit()
            print(f"2023년 {month_str}월 데이터 삽입 완료")

except Error as e:
    print(f"Error: {e}")

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL 연결 종료")
