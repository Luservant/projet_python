import pandas as pd

for sep in [";", ",", "\t", "|"]:
    df = pd.read_csv("data-es-equipement.csv", sep=sep, nrows=5)
    print(f"sep='{sep}' → {df.shape[1]} colonnes : {list(df.columns)[:5]}")