import pymysql

def delete_adult_genre():
    # MySQL 연결 정보
    connection = pymysql.connect(
        host='192.168.0.115',  # MySQL 서버 주소
        user='root',           # 사용자 이름
        password='1234',       # 비밀번호
        database='lg_hellovisionvod',  # 데이터베이스 이름
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            # 삭제 작업을 배치로 실행
            batch_size = 1000
            for month in range(1, 12):  # 1부터 11까지 반복
                table_name = f"vod_data_2023{month:02d}"
                print(f"Processing table: {table_name}")

                while True:
                    # DELETE 쿼리 실행 (배치 단위)
                    delete_query = f"""
                    DELETE FROM {table_name}
                    WHERE genre_of_ct_cl = '성인'
                    LIMIT %s;
                    """
                    cursor.execute(delete_query, (batch_size,))

                    # 변경 사항 저장
                    connection.commit()

                    # 삭제된 행 개수 확인
                    rows_deleted = cursor.rowcount
                    print(f"Deleted {rows_deleted} rows from {table_name}")

                    # 더 이상 삭제할 행이 없으면 종료
                    if rows_deleted < batch_size:
                        break

        print("All rows with '성인' genre_of_ct_cl have been deleted from all tables.")

    except Exception as e:
        print("Error:", e)

    finally:
        connection.close()

if __name__ == "__main__":
    delete_adult_genre()
