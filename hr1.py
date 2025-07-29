DROP TABLE IF EXISTS [hr_db].[hr_schema].[hr_query_combined_org_path_table_raw];

WITH CombinedData AS (
  -- your UNION ALL of all daily tables
  SELECT * FROM [hr_db].[hr_schema].[2023_07_31_daily_org_path]
  UNION ALL
  SELECT * FROM [hr_db].[hr_schema].[2023_08_01_daily_org_path]
  -- …etc…
),

-- 1) flag each row when the path changes (or it's the first row for that employee)
cte_flag AS (
  SELECT
    IDP_DATA_DATE,
    EMPLID,
    ORG_PATH_BY_NAME,
    CASE 
      WHEN LAG(ORG_PATH_BY_NAME) 
           OVER (PARTITION BY EMPLID ORDER BY IDP_DATA_DATE) = ORG_PATH_BY_NAME
      THEN 0
      ELSE 1
    END AS IsNewIsland
  FROM CombinedData
),

-- 2) running total of that flag gives you a “group #” for each stretch of identical path
cte_grp AS (
  SELECT
    IDP_DATA_DATE,
    EMPLID,
    ORG_PATH_BY_NAME,
    SUM(IsNewIsland) 
      OVER (PARTITION BY EMPLID 
            ORDER BY IDP_DATA_DATE 
            ROWS UNBOUNDED PRECEDING) AS grp
  FROM cte_flag
)

-- 3) collapse each (EMPLID, path, grp) into one row
SELECT
  MIN(IDP_DATA_DATE) AS Date_From,
  MAX(IDP_DATA_DATE) AS Date_To,
  EMPLID,
  ORG_PATH_BY_NAME
INTO [hr_db].[hr_schema].[hr_query_combined_org_path_table_raw]
FROM cte_grp
GROUP BY
  EMPLID,
  ORG_PATH_BY_NAME,
  grp
ORDER BY
  EMPLID,
  Date_From;