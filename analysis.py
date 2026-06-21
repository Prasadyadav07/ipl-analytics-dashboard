import pandas as pd

matches = pd.read_csv("data/matches.csv")
deliveries = pd.read_csv("data/deliveries.csv")

print("MATCHES COLUMNS")
print(matches.columns.tolist())

print("\nDELIVERIES COLUMNS")
print(deliveries.columns.tolist())