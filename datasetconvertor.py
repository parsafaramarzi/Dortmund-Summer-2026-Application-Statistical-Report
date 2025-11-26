import pandas as pd

df = pd.read_csv(
    'cycling.txt',
    delim_whitespace=True,
    quotechar='"'
)

print(df.head())

df.to_csv('cycling_clean.csv', index=False)
print("Data successfully converted to cycling_clean.csv!")