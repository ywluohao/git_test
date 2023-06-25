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
