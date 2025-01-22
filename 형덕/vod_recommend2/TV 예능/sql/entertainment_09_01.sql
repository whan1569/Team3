CREATE VIEW entertainment_09_01 AS
SELECT 
    genre_of_ct_cl, 
    asset_nm, 
    disp_rtm_seconds, 
    AVG(use_tms) AS avg_use_tms, 
    COUNT(*) AS view_count, 
    (AVG(use_tms) / disp_rtm_seconds) * 100 AS watch_ratio
FROM 
    lg_hellovisionvod.entertainment_09
WHERE 
    CT_CL IN ('classic') 
    AND use_tms > 60
GROUP BY 
    genre_of_ct_cl, asset_nm, disp_rtm_seconds
ORDER BY 
    view_count DESC
LIMIT 20; -- 상위 20개만
