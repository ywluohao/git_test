WITH RankedEmails AS (
    SELECT 
        ID,
        email,
        date,
        ROW_NUMBER() OVER (PARTITION BY ID ORDER BY date DESC) AS rn
    FROM 
        your_table_name
),
FilteredEmails AS (
    SELECT 
        ID,
        email,
        rn
    FROM 
        RankedEmails
    WHERE 
        rn <= 2
),
DistinctEmails AS (
    SELECT 
        ID,
        MAX(CASE WHEN rn = 1 THEN email END) AS latest_email,
        MAX(CASE WHEN rn = 2 THEN email END) AS second_email
    FROM 
        FilteredEmails
    GROUP BY 
        ID
    HAVING 
        COUNT(DISTINCT email) = 2
)
SELECT 
    ID,
    latest_email,
    second_email
FROM 
    DistinctEmails;