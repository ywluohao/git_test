WITH ExtractedValue AS (
    SELECT 
        SUBSTRING(
            YourColumnName, 
            CHARINDEX('=', YourColumnName) + 1, 
            CHARINDEX(',', YourColumnName) - CHARINDEX('=', YourColumnName) - 1
        ) AS extracted_value
    FROM 
        YourTableName
)
SELECT 
    LEFT(extracted_value, CHARINDEX('_', extracted_value) - 1) AS aaaa,
    SUBSTRING(extracted_value, CHARINDEX('_', extracted_value) + 1, LEN(extracted_value)) AS bbb
FROM 
    ExtractedValue;