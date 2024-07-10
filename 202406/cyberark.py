WITH ExtractedValue AS (
    SELECT 
        -- Extract the part after 'CN=' and before the comma
        SUBSTRING(
            YourColumnName, 
            CHARINDEX('=', YourColumnName) + 1, 
            CHARINDEX(',', YourColumnName) - CHARINDEX('=', YourColumnName) - 1
        ) AS extracted_value
    FROM 
        YourTableName
)
SELECT 
    -- Extract 'aaa' part
    LEFT(extracted_value, LEN(extracted_value) - CHARINDEX('_', REVERSE(extracted_value))) AS aaa,
    -- Extract 'bbb' part
    RIGHT(extracted_value, CHARINDEX('_', REVERSE(extracted_value)) - 1) AS bbb
FROM 
    ExtractedValue;