WITH RankedData AS (
    SELECT 
        YEARWEEK(STR_TO_DATE(created, '%Y%m%d')) 
        - YEARWEEK(STR_TO_DATE(CONCAT(SUBSTRING(created, 1, 6), '01'), '%Y%m%d')) + 1 AS week_in_month, -- 월 기준 주차 계산
        created,
        CT_CL,
        asset_nm,
        ROW_NUMBER() OVER (PARTITION BY 
            YEARWEEK(STR_TO_DATE(created, '%Y%m%d')) 
            - YEARWEEK(STR_TO_DATE(CONCAT(SUBSTRING(created, 1, 6), '01'), '%Y%m%d')) + 1 
            ORDER BY RAND()) AS rn -- 각 주별로 무작위로 순번 부여
    FROM lg_hellovisionvod.vod_mart
    WHERE SUBSTRING(created, 1, 6) = '202310' -- 2023년 10월 데이터만 필터링
      AND CT_CL = '영화' -- 콘텐츠 유형이 '영화'인 데이터만 필터링
)
SELECT 
    week_in_month, 
    created, 
    CT_CL, 
    asset_nm
FROM RankedData
WHERE rn <= 20 -- 주별로 상위 20개만 선택
ORDER BY week_in_month, rn; -- 주차와 순번 기준으로 정렬
