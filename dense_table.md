# Dense Table Aggregation

This document shows how to:

1. Create a unified view over your 700 daily tables  
2. Run the “islands” query in T-SQL to collapse consecutive days with the same path  
3. Pull the result down in Python with one simple script  

---

## 1. Create/Alter the Union View

```sql
CREATE OR ALTER VIEW dbo.v_AllDaily AS
SELECT [Date], [ID], [Path] FROM dbo.Daily_20230101
UNION ALL
SELECT [Date], [ID], [Path] FROM dbo.Daily_20230102
UNION ALL
-- … repeat for each daily table …
SELECT [Date], [ID], [Path] FROM dbo.Daily_20231231;
GO
```

> **Tip:** Automate that `UNION ALL` list via a quick query on `sys.tables` if your tables follow a strict `Daily_YYYYMMDD` pattern.

---

## 2. T-SQL “Islands” Query

```sql
WITH cte AS (
  SELECT
    [Date],
    [ID],
    [Path],
    SUM(
      CASE
        WHEN LAG([Path]) OVER (PARTITION BY [ID] ORDER BY [Date]) = [Path]
          THEN 0
        ELSE 1
      END
    ) OVER (
      PARTITION BY [ID]
      ORDER BY [Date]
      ROWS UNBOUNDED PRECEDING
    ) AS grp
  FROM dbo.v_AllDaily
)
SELECT
  [ID],
  [Path],
  MIN([Date]) AS Date_From,
  MAX([Date]) AS Date_To
FROM cte
GROUP BY
  [ID],
  [Path],
  grp
ORDER BY
  [ID],
  Date_From;
```

> This will collapse each stretch of identical `Path` values into one row with its start/end dates.

---

## 3. Python Glue Script

```python
import pyodbc
import pandas as pd

# 1. Connect to SQL Server
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=your_server;DATABASE=your_db;"
    "UID=your_user;PWD=your_pwd"
)

# 2. Define the dense-table query
sql = """
WITH cte AS (
  SELECT
    [Date],
    [ID],
    [Path],
    SUM(
      CASE WHEN LAG([Path]) OVER (PARTITION BY [ID] ORDER BY [Date]) = [Path]
           THEN 0 ELSE 1 END
    ) OVER (PARTITION BY [ID] ORDER BY [Date]
            ROWS UNBOUNDED PRECEDING) AS grp
  FROM dbo.v_AllDaily
)
SELECT
  [ID],
  [Path],
  MIN([Date]) AS Date_From,
  MAX([Date]) AS Date_To
FROM cte
GROUP BY [ID], [Path], grp
ORDER BY [ID], Date_From;
"""

# 3. Run the query and load into pandas
df_dense = pd.read_sql(sql, conn)
conn.close()

# 4. Inspect the result
print(df_dense.head())
```
