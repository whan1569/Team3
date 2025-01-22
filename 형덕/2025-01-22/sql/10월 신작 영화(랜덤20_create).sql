CREATE OR REPLACE VIEW lg_hellovisionvod.vod_mart_10_weekly_random AS
WITH RankedData AS (
    SELECT 
        YEARWEEK(STR_TO_DATE(created, '%Y%m%d')) 
        - YEARWEEK(STR_TO_DATE(CONCAT(SUBSTRING(created, 1, 6), '01'), '%Y%m%d')) + 1 AS week_in_month, -- 월 기준 주차 계산
        created, -- 데이터 생성일 (YYYYMMDDHHMMSS 형식)
        CT_CL, -- 콘텐츠 유형 ('영화', '드라마' 등)
        asset_nm, -- 영화 이름 또는 에셋 이름
        ROW_NUMBER() OVER (PARTITION BY 
            YEARWEEK(STR_TO_DATE(created, '%Y%m%d')) 
            - YEARWEEK(STR_TO_DATE(CONCAT(SUBSTRING(created, 1, 6), '01'), '%Y%m%d')) + 1 
            ORDER BY RAND()) AS rn -- 주별로 무작위로 순번 부여
    FROM lg_hellovisionvod.vod_mart
    WHERE SUBSTRING(created, 1, 6) = '202310' -- 2023년 10월 데이터만 필터링
      AND CT_CL = '영화' -- 콘텐츠 유형이 '영화'인 데이터만 필터링
)
SELECT 
    week_in_month, -- 월 기준 주차
    created, -- 데이터 생성일
    CT_CL, -- 콘텐츠 유형
    asset_nm -- 영화 이름
FROM RankedData
WHERE rn <= 20 -- 주별로 상위 20개 데이터 선택
ORDER BY week_in_month, created; -- 월 기준 주차와 생성일 순으로 정렬
