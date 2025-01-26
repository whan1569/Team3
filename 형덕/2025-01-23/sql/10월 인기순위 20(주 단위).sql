WITH RankedMovies AS (
    SELECT 
        YEARWEEK(STR_TO_DATE(SUBSTRING(strt_dt, 1, 8), '%Y%m%d')) 
        - YEARWEEK(STR_TO_DATE(CONCAT('202310', '01'), '%Y%m%d')) + 1 AS week_in_month, -- 10월 기준 주차 계산
        asset_nm, -- 영화 제목
        COUNT(*) AS popularity, -- 인기도(중복된 횟수)
        RANK() OVER (PARTITION BY 
            YEARWEEK(STR_TO_DATE(SUBSTRING(strt_dt, 1, 8), '%Y%m%d')) 
            - YEARWEEK(STR_TO_DATE(CONCAT('202310', '01'), '%Y%m%d')) + 1 
            ORDER BY COUNT(*) DESC) AS `rank` -- 주별 인기 순위 계산
    FROM lg_hellovisionvod.vod_movie_10
    WHERE SUBSTRING(strt_dt, 1, 6) = '202310' -- 2023년 10월 데이터만 필터링
    GROUP BY 
        YEARWEEK(STR_TO_DATE(SUBSTRING(strt_dt, 1, 8), '%Y%m%d')) 
        - YEARWEEK(STR_TO_DATE(CONCAT('202310', '01'), '%Y%m%d')) + 1, -- 주별로 그룹화
        asset_nm -- 영화 제목별로 그룹화
)
SELECT 
    week_in_month, -- 월 기준 주차
    `rank`, -- 주별 인기 순위
    asset_nm, -- 영화 제목
    popularity -- 인기도(중복된 횟수)
FROM RankedMovies
WHERE `rank` <= 20 -- 주별로 상위 20위까지만 필터링
ORDER BY week_in_month, `rank`; -- 주차와 순위 기준으로 정렬
