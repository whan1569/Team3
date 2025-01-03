import pymysql

# MySQL 연결 정보
host = '192.168.0.105'
user = 'root'
password = '1234'
database = 'lg_hellovisionvod'

# MySQL 데이터베이스에 연결
connection = pymysql.connect(host=host, user=user, password=password, database=database)

try:
    # 커서 생성
    with connection.cursor() as cursor:
        # 삭제 쿼리 작성
        delete_query = "DELETE FROM vod_mart WHERE ct_cl = '성인'"
        
        # 쿼리 실행
        cursor.execute(delete_query)
        
        # 변경사항 커밋
        connection.commit()
        print("삭제가 완료되었습니다.")
        
except Exception as e:
    print(f"에러 발생: {e}")
    # 예외가 발생하면 롤백
    connection.rollback()

finally:
    # 연결 종료
    connection.close()
