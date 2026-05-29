import pandas as pd

df = pd.read_excel("output/results/accountability_evidence.xlsx")

print(len(df))
print(df["objective"].nunique())



for objective, group in df.groupby("objective"):
    send only that objective's rows to Claude
    save one markdown file per objective