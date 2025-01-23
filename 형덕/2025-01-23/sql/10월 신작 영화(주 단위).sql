-- 주차별로 중복 없는 영화 데이터를 조회하는 쿼리
SELECT DISTINCT
    -- YEARWEEK(): 데이터가 포함된 주차를 연-주(Year-Week) 형식으로 계산
    -- 10월의 첫 주와 비교해 해당 월의 주차를 계산
    YEARWEEK(STR_TO_DATE(created, '%Y%m%d')) 
    - YEARWEEK(STR_TO_DATE(CONCAT(SUBSTRING(created, 1, 6), '01'), '%Y%m%d')) + 1 AS week_in_month, -- 월 기준 주차 계산

    -- created 컬럼: 데이터 생성일 (형식: YYYYMMDDHHMMSS)
    created,

    -- CT_CL 컬럼: 콘텐츠 유형 ('영화', '드라마' 등)
    CT_CL,

    -- asset_nm 컬럼: 영화 이름 또는 에셋 이름
    asset_nm
FROM 
    -- 원본 테이블: lg_hellovisionvod.vod_mart
    lg_hellovisionvod.vod_mart
WHERE 
    -- SUBSTRING(): created 컬럼에서 연월(YYYYMM)만 추출해 2023년 10월 데이터 필터링
    SUBSTRING(created, 1, 6) = '202310'

    -- 콘텐츠 유형이 '영화'인 데이터만 필터링
    AND CT_CL = '영화'
ORDER BY 
    -- 월 기준 주차별 정렬
    week_in_month, 

    -- 같은 주차 내에서는 생성일 기준 정렬
    created;
    
    -- 주차별로 중복 없는 10월 영화 데이터를 뷰 테이블로 저장
CREATE OR REPLACE VIEW lg_hellovisionvod.vod_mart_10_weekly AS
SELECT DISTINCT
    -- YEARWEEK(): 데이터가 포함된 주차를 연-주(Year-Week) 형식으로 계산
    -- 10월의 첫 주와 비교해 해당 월의 주차를 계산
    YEARWEEK(STR_TO_DATE(created, '%Y%m%d')) 
    - YEARWEEK(STR_TO_DATE(CONCAT(SUBSTRING(created, 1, 6), '01'), '%Y%m%d')) + 1 AS week_in_month, -- 월 기준 주차 계산

    -- created 컬럼: 데이터 생성일 (형식: YYYYMMDDHHMMSS)
    created,

    -- CT_CL 컬럼: 콘텐츠 유형 ('영화', '드라마' 등)
    CT_CL,

    -- asset_nm 컬럼: 영화 이름 또는 에셋 이름
    asset_nm
FROM 
    -- 원본 테이블: lg_hellovisionvod.vod_mart
    lg_hellovisionvod.vod_mart
WHERE 
    -- SUBSTRING(): created 컬럼에서 연월(YYYYMM)만 추출해 2023년 10월 데이터 필터링
    SUBSTRING(created, 1, 6) = '202310'

    -- 콘텐츠 유형이 '영화'인 데이터만 필터링
    AND CT_CL = '영화'
ORDER BY 
    -- 월 기준 주차별 정렬
    week_in_month, 

    -- 같은 주차 내에서는 생성일 기준 정렬
    created;

