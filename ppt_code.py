from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth
import pandas as pd


# Example dataset
dataset = [
['Bread', 'Milk'],
['Bread', 'Diapers', 'Beer', 'Eggs'],
['Milk', 'Diapers', 'Beer', 'Coke'],
['Bread', 'Milk', 'Diapers', 'Beer'],
['Bread', 'Milk', 'Diapers', 'Coke']
]


# Convert the dataset into a transaction format
te = TransactionEncoder()
te_ary = te.fit(dataset).transform(dataset)
print(te_ary)
df = pd.DataFrame(te_ary, columns=te.columns_)
# Run FP-Growth algorithm
frequent_itemsets = fpgrowth(df, min_support=0.5, use_colnames=True)
# Print the frequent itemsets
print(frequent_itemsets)
