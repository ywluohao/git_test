import pandas as pd

df = pd.read_excel("output/results/accountability_evidence.xlsx")

print(len(df))
print(df["objective"].nunique())