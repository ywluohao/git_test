import pandas as pd
import json

# ---------- Option A: small walker (no extra deps) ----------
def _as_roots(x):
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return []
    if isinstance(x, str):
        x = json.loads(x)
    if isinstance(x, dict):
        return [x]
    return x if isinstance(x, list) else []

def extract_paths_to_leaves(x, value_key="value", children_key="children"):
    roots = _as_roots(x)
    paths = []
    stack = [(r, [r.get(value_key)]) for r in roots if isinstance(r, dict)]
    while stack:
        node, path = stack.pop()
        children = node.get(children_key) or []
        if children:
            for ch in children:  # multiple children => multiple output paths
                if isinstance(ch, dict):
                    stack.append((ch, path + [ch.get(value_key)]))
        else:
            paths.append(path)
    return paths

# ---------- Example data (multiple children + variable depth) ----------
df = pd.DataFrame({
    "id": [1],
    "TREE_TASK_DATA": [[
        {
            "value": "AE",
            "children": [
                {
                    "value": "RISK-001",
                    "children": [
                        {"value": "CTRL-01", "children": [{"value": "Q-1"}, {"value": "Q-2"}]},
                        {"value": "CTRL-02"}  # shorter branch (no children)
                    ]
                },
                {
                    "value": "RISK-002",
                    "children": [{"value": "CTRL-03", "children": [{"value": "Q-3"}]}]
                }
            ]
        }
    ]]
})

# ---------- Convert to l1..l5 ----------
out = (
    df.assign(_path=df["TREE_TASK_DATA"].apply(extract_paths_to_leaves))
      .explode("_path", ignore_index=True)
)

levels = out["_path"].apply(lambda p: pd.Series((p + [None]*5)[:5], index=["l1","l2","l3","l4","l5"]))
out = pd.concat([out.drop(columns=["_path"]), levels], axis=1)

print(out[["id","l1","l2","l3","l4","l5"]])