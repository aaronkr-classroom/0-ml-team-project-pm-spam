import csv
import random
import re
import chardet
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


input_file = "test_data_set.csv"

data = pd.read_csv(input_file, encoding="utf-8")


values = data["v1"].value_counts()

sns.barplot(x=values.index, y=values.values, palette='viridis')
plt.title("Number of category", fontsize=16)
plt.xlabel("category", fontsize=16)
plt.ylabel("count", fontsize=16)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.show()
