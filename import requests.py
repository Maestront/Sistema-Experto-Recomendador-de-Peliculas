import pandas as pd
from collections import Counter

df = pd.read_csv("title.basics.tsv.gz", sep="\t", usecols=["genres"])

counter = Counter()

for genres in df["genres"].fillna(""):
    for g in genres.split(","):
        if g != "\\N" and g != "":
            counter[g] += 1

print(counter)
