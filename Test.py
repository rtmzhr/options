import pandas as pd


data = pd.read_csv("Data/4.csv")
data = data.replace('-', 0)
calls = data.iloc[:, 0]
strikes = data.iloc[:, 5]
puts = data.iloc[:, 6]
data = pd.concat([calls, strikes, puts], axis=1)
strike = int(data.iloc[24 - 6, 1])

price = float(data[data.iloc[:, 1] == 250].iloc[0, 1])

print()