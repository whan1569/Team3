CREATE VIEW movie_09_02 AS
SELECT 
    genre_of_ct_cl, 
    asset_nm, 
    disp_rtm_seconds, 
    AVG(use_tms) AS avg_use_tms, 
    COUNT(*) AS view_count, 
    (AVG(use_tms) / disp_rtm_seconds) * 100 AS watch_ratio
FROM 
    lg_hellovisionvod.vod_movie_09
WHERE 
    genre_of_ct_cl LIKE '%공포%' -- 'SF/판타지'와 비슷한 데이터도 포함
    AND use_tms > 60
GROUP BY 
    genre_of_ct_cl, asset_nm, disp_rtm_seconds
ORDER BY 
    view_count DESC
LIMIT 20; -- 상위 20개만
