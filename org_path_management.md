# Org Path Management

此文档汇总了从零开始实现每日员工组织路径快照与历史区间查询的全部代码示例。

---

## 1. SQL 架构：`OrgSnapshots`

```sql
-- 创建持久快照表
CREATE TABLE dbo.OrgSnapshots (
  SnapshotDate DATE         NOT NULL,
  EmployeeID   INT          NOT NULL,
  OrgPath      VARCHAR(500) NOT NULL,
  CONSTRAINT PK_OrgSnapshots PRIMARY KEY (SnapshotDate, EmployeeID)
);

-- 列存压缩与索引
CREATE CLUSTERED COLUMNSTORE INDEX CCI_OrgSnapshots
  ON dbo.OrgSnapshots;

CREATE NONCLUSTERED INDEX IX_OrgSnapshots_EmpDate
  ON dbo.OrgSnapshots(EmployeeID, SnapshotDate);
```

---

## 2. 日常加载：Python 脚本

```python
import pandas as pd
from sqlalchemy import create_engine
import sqlalchemy

# 2.1 构造当天快照 DataFrame
# df_today = pd.DataFrame({
#     "EmployeeID": [...],
#     "OrgPath":   [...],
#})
df_today["SnapshotDate"] = pd.to_datetime("today").date()

# 2.2 连接字符串（ODBC Driver 18）
conn_str = (
    "mssql+pyodbc:///?odbc_connect="
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=your_server;DATABASE=your_db;UID=...;PWD=..."
)
engine = create_engine(conn_str)

# 2.3 批量追加至 OrgSnapshots
# 注意：列名需与目标表一致
# df_today.rename(columns={"id":"EmployeeID"}, inplace=True)
df_today.to_sql(
    "OrgSnapshots",
    schema="dbo",
    con=engine,
    if_exists="append",
    index=False,
    dtype={"OrgPath": sqlalchemy.types.VARCHAR(500)}
)
```

---

## 3. 历史区间查询：纯 SQL 实现

```sql
DECLARE @EmployeeID INT = 1234;
DECLARE @StartDate  DATE = DATEADD(YEAR,-2,CAST(GETDATE() AS DATE));

WITH UserSnaps AS (
    SELECT SnapshotDate, OrgPath
      FROM dbo.OrgSnapshots
     WHERE EmployeeID   = @EmployeeID
       AND SnapshotDate >= @StartDate
), MarkPrev AS (
    SELECT
      SnapshotDate,
      OrgPath,
      LAG(OrgPath)     OVER (ORDER BY SnapshotDate)    AS PrevPath,
      LAG(SnapshotDate) OVER (ORDER BY SnapshotDate)    AS PrevDate
    FROM UserSnaps
), FlagNew AS (
    SELECT
      SnapshotDate,
      OrgPath,
      CASE
        WHEN OrgPath <> PrevPath
          OR DATEDIFF(DAY, PrevDate, SnapshotDate) > 1
        THEN 1 ELSE 0
      END AS IsNewGroup
    FROM MarkPrev
), Numbered AS (
    SELECT
      SnapshotDate,
      OrgPath,
      SUM(IsNewGroup) OVER (
        ORDER BY SnapshotDate
        ROWS UNBOUNDED PRECEDING
      ) AS GroupID
    FROM FlagNew
)
SELECT
  MIN(SnapshotDate) AS ValidFrom,
  MAX(SnapshotDate) AS ValidTo,
  OrgPath
FROM Numbered
GROUP BY GroupID, OrgPath
ORDER BY ValidFrom;
```

---

## 4. 修复快照：Python 批量删 & 重新插入

```python
import pandas as pd
from sqlalchemy import create_engine, text
import sqlalchemy

# 4.1 连接
conn_str = (
    "mssql+pyodbc:///?odbc_connect="
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=your_server;DATABASE=your_db;UID=...;PWD=..."
)
engine = create_engine(conn_str)

# 4.2 定义需修复的日期列表
dates_to_fix = ['2025-07-20', '2025-07-21']

# 4.3 删除旧数据
with engine.begin() as conn:
    conn.execute(
        text("DELETE FROM dbo.OrgSnapshots WHERE SnapshotDate IN :dates"),
        {"dates": tuple(dates_to_fix)}
    )

# 4.4 准备修正后的 DataFrame：df_fix
# df_fix 必须包含 ['SnapshotDate','EmployeeID','OrgPath']
df_fix['SnapshotDate'] = pd.to_datetime(df_fix['SnapshotDate']).dt.date

# 4.5 重新插入
df_fix.to_sql(
    "OrgSnapshots",
    con=engine,
    schema="dbo",
    if_exists="append",
    index=False,
    dtype={"OrgPath": sqlalchemy.types.VARCHAR(500)}
)
```

---

*End of file*

