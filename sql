# SQL Interview Question

You are given a table named `performance` with the following structure:

| team | employee | score |
|-------|----------|-------|
| A | Alice | 90 |
| A | Bob | 80 |
| B | Carol | 85 |
| A | Dave | 95 |
| B | Eve | 88 |

---

## Q1

**Write an SQL query to calculate the average score for each team.**

### Solution:
```sql
SELECT
team,
AVG(score) AS average_score
FROM
performance
GROUP BY
team;
```

---

## Q2

**Write an SQL query to rank all employees within their team based on their score (higher score = higher rank).
If two employees have the same score, assign them the same rank using dense ranking.**

### Solution:
```sql
SELECT
team,
employee,
score,
DENSE_RANK() OVER (
PARTITION BY team
ORDER BY score DESC
) AS rank_in_team
FROM
performance;
```

---

## Q3

**Write an SQL query to find the top performer(s) in each team. If multiple employees have the same highest score in a team, return all of them.**

### Solution:
```sql
WITH ranked AS (
SELECT
team,
employee,
score,
RANK() OVER (
PARTITION BY team
ORDER BY score DESC
) AS rnk
FROM
performance
)
SELECT
team,
employee,
score
FROM
ranked
WHERE
rnk = 1;
```

---

## Q4

**Write an SQL query to find all employees whose score is above the average score of their team.**

### Solution:
```sql
WITH team_avg AS (
SELECT
team,
AVG(score) AS avg_score
FROM
performance
GROUP BY
team
)
SELECT
p.team,
p.employee,
p.score
FROM
performance p
JOIN
team_avg t
ON
p.team = t.team
WHERE
p.score > t.avg_score;
```

# Pandas Solutions for SQL Interview Questions

We use the following DataFrame:

```python
import pandas as pd

df = pd.DataFrame({
"team": ["A", "A", "B", "A", "B"],
"employee": ["Alice", "Bob", "Carol", "Dave", "Eve"],
"score": [90, 80, 85, 95, 88]
})
```

---

## Q1 - Average score per team

```python
df.groupby("team")["score"].mean().reset_index(name="average_score")
```

**Result:**

| team | average_score |
|------|----------------|
| A | 88.33 |
| B | 86.50 |

---

## Q2 - Employee ranks within team (Dense Rank)

```python
df["rank_in_team"] = df.groupby("team")["score"].rank(method="dense", ascending=False)
```

**Result:**

| team | employee | score | rank_in_team |
|------|----------|-------|--------------|
| A | Alice | 90 | 2.0 |
| A | Bob | 80 | 3.0 |
| B | Carol | 85 | 2.0 |
| A | Dave | 95 | 1.0 |
| B | Eve | 88 | 1.0 |

---

## Q3 - Top performer(s) in each team

```python
top_scores = df.groupby("team")["score"].transform("max")
df[df["score"] == top_scores][["team", "employee", "score"]]
```

**Result:**

| team | employee | score |
|------|----------|-------|
| A | Dave | 95 |
| B | Eve | 88 |

---

## Q4 - Employees above team average

```python
avg_scores = df.groupby("team")["score"].transform("mean")
df[df["score"] > avg_scores][["team", "employee", "score"]]
```

**Result:**

| team | employee | score |
|------|----------|-------|
| A | Alice | 90 |
| A | Dave | 95 |
| B | Eve | 88 |

