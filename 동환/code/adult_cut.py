import mysql.connector
from mysql.connector import Error

def delete_adult_entries_by_month():
    try:
        # 원격 MySQL 서버 연결
        remote_connection = mysql.connector.connect(
            host="192.168.0.105",
            user="root",
            password="1234",
            database="lg_hellovisionvod"
        )

        if remote_connection.is_connected():
            print("원격 MySQL 연결 성공")

            remote_cursor = remote_connection.cursor()

            # 월별로 데이터를 삭제하는 작업
            for month in range(1, 13):
                month_str = f"2023{month:02d}"  # 월을 2자리로 포맷 (예: 202301, 202302)

                # DELETE 쿼리 실행
                delete_query = """
                DELETE FROM vod_data
                WHERE CT_CL = '성인' AND strt_dt LIKE %s;
                """
                remote_cursor.execute(delete_query, (f"{month_str}%",))

                # 변경 사항 커밋
                remote_connection.commit()

                # 삭제된 행 수 기록
                deleted = remote_cursor.rowcount
                print(f"{month_str}월: {deleted} rows deleted.")

            print("모든 '성인' 데이터 삭제 완료.")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if remote_connection.is_connected():
            remote_cursor.close()
            remote_connection.close()
            print("원격 MySQL 연결 종료")

# 함수 실행
delete_adult_entries_by_month()
