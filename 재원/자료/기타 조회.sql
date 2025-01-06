SELECT * FROM lg_hellovisionvod.vod_data_202309
where sha2_hash like '79ee5ed89b853deb7bc2b5ac68a8dea90ae42c83090de3b4f2b58061c14ca594';

SELECT DISTINCT asset_nm 
FROM lg_hellovisionvod.vod_data_202310
WHERE asset_nm LIKE '%classic%';


SELECT * FROM lg_hellovisionvod.vod_data_202309
where asset_nm like '%회' and CT_CL like '기타';