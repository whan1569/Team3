import mysql.connector
import pandas as pd

# MySQL 연결 함수
def connect_to_mysql():
    return mysql.connector.connect(
        host="localhost",  # MySQL 서버 주소
        user="root",       # MySQL 사용자
        password="1234",   # MySQL 비밀번호
        database="lg_hellovisionvod"  # 사용할 데이터베이스
    )

# 각 테이블에서 상위 30 sha2_hash 추출 함수
def fetch_top_sha2_hashes(table_name, limit=30):
    query = f"""
        SELECT sha2_hash, COUNT(*) AS count
        FROM {table_name}
        GROUP BY sha2_hash
        ORDER BY count DESC
        LIMIT {limit};
    """

    conn = connect_to_mysql()
    try:
        df = pd.read_sql(query, conn)
        return df
    finally:
        conn.close()

# 1월부터 11월까지 처리하고 CSV로 저장
def process_tables_and_save():
    months = [f"{i:02}" for i in range(1, 12)]  # 01 ~ 11
    base_table_name = "vod_movie_"

    for month in months:
        table_name = f"{base_table_name}{month}"
        print(f"Processing table: {table_name}")

        try:
            # 상위 30개 추출
            df = fetch_top_sha2_hashes(table_name)

            # CSV로 저장
            csv_filename = f"top_sha2_hash_{month}.csv"
            df.to_csv(csv_filename, index=False)
            print(f"Saved: {csv_filename}")

        except Exception as e:
            print(f"Error processing table {table_name}: {e}")

if __name__ == "__main__":
    process_tables_and_save()
