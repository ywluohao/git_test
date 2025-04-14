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