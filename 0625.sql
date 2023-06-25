
-- method 1

-- Create a new table with three columns
CREATE TABLE SplitValues (
    ID INT,
    Enumerator INT,
    Value VARCHAR(50)
);

-- Insert sample data into the original table
INSERT INTO OriginalTable (Column1, Column2)
VALUES (1, 'a, b, c'),
       (2, 'a, b, c, d, e');

-- Split and insert the values into the new table
WITH SplitRows AS (
    SELECT
        Column1 AS ID,
        CAST('<S>' + REPLACE(Column2, ',', '</S><S>') + '</S>' AS XML) AS Data
    FROM OriginalTable
)
INSERT INTO SplitValues (ID, Enumerator, Value)
SELECT
    ID,
    ROW_NUMBER() OVER (PARTITION BY ID ORDER BY (SELECT NULL)) AS Enumerator,
    LTRIM(RTRIM(Split.a.value('.', 'VARCHAR(50)'))) AS Value
FROM SplitRows
CROSS APPLY Data.nodes('/S') AS Split(a);

-- Select data from the split table
SELECT * FROM SplitValues;


-- method 2

-- Create a new table with three columns
CREATE TABLE SplitValues (
    ID INT,
    Enumerator INT,
    Value VARCHAR(50)
);

-- Insert sample data into the original table
INSERT INTO OriginalTable (Column1, Column2)
VALUES (1, 'a, b, c'),
       (2, 'a, b, c, d, e');

-- Split and insert the values into the new table
WITH SplitRows AS (
    SELECT
        Column1 AS ID,
        Column2,
        CHARINDEX(',', Column2) AS CommaIndex
    FROM OriginalTable
)
INSERT INTO SplitValues (ID, Enumerator, Value)
SELECT
    ID,
    ROW_NUMBER() OVER (PARTITION BY ID ORDER BY (SELECT NULL)) AS Enumerator,
    CASE
        WHEN CommaIndex > 0 THEN LTRIM(RTRIM(SUBSTRING(Column2, 1, CommaIndex - 1)))
        ELSE LTRIM(RTRIM(Column2))
    END AS Value
FROM SplitRows
CROSS APPLY (VALUES (Column2, CommaIndex)) AS X(Column2, CommaIndex)
WHERE LEN(Column2) > 0
UNION ALL
SELECT
    ID,
    ROW_NUMBER() OVER (PARTITION BY ID ORDER BY (SELECT NULL)) AS Enumerator,
    LTRIM(RTRIM(SUBSTRING(Column2, CommaIndex + 1, LEN(Column2) - CommaIndex)))
FROM SplitRows
CROSS APPLY (VALUES (Column2, CommaIndex)) AS X(Column2, CommaIndex)
WHERE CommaIndex > 0;

-- Select data from the split table
SELECT * FROM SplitValues;
