SELECT 
    genre_of_ct_cl, 
    asset_nm, 
    disp_rtm, 
    AVG(use_tms) AS avg_use_tms, -- 같은 asset_nm의 use_tms 평균
    COUNT(*) AS view_count, -- asset_nm별 시청 횟수
    DATE_FORMAT(STR_TO_DATE(LEFT(strt_dt, 8), '%Y%m%d'), '%Y-%m') AS month, -- 월 정보
    (AVG(use_tms) / 
     (HOUR(TIME_FORMAT(disp_rtm, '%H:%i')) * 3600 + MINUTE(TIME_FORMAT(disp_rtm, '%H:%i')) * 60)
    ) * 100 AS watch_ratio -- 평균 시청 시간 / 상영 시간 비율
FROM 
    vod_data_202301
WHERE 
    CT_CL LIKE '%영화%' 
    AND use_tms > 60
GROUP BY 
    month, genre_of_ct_cl, asset_nm, disp_rtm
ORDER BY 
    month, genre_of_ct_cl, view_count DESC;
