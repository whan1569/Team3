import os
os.environ['PYSPARK_DRIVER_PYTHON'] = 'python'
os.environ['PYSPARK_PYTHON'] = 'python'

from pyspark.sql import SparkSession

# Spark 세션 시작
spark = SparkSession.builder.appName("MySQL Count") \
    .config("spark.jars", "C:/Users/USER/Desktop/Team3/동환/mysql-connector-j-9.1.0/mysql-connector-j-9.1.0.jar") \
    .getOrCreate()

# MySQL 연결 정보
jdbc_url = "jdbc:mysql://localhost:3306/lg_hellovisionvod"
properties = {"user": "root", "password": "1234", "driver": "com.mysql.cj.jdbc.Driver"}

# MySQL 데이터 불러오기
df = spark.read.jdbc(url=jdbc_url, table="vod_data", properties=properties)

# 행 수 출력
print(f"Total rows: {df.count()}")
