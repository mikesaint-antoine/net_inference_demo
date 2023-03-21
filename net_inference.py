import csv
import numpy as np
import scipy.stats
from operator import itemgetter
import sys




## reading in data
genes = []
data = []
with open("fake_data.csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:

        # print(row)
        # input()

        genes.append(row[0])
        data.append(row[1:])



## get rid of heading row, and cast data from strings to floats
genes = genes[1:]
samps = data[0]
data = data[1:]
data = np.array(data).astype(float)





## check to make sure everything got read in correctly
print(data)
print(f"number of genes: {len(genes)}")
print(f"number of samples: {len(samps)}")
print(f"expression matrix shape: {data.shape}")






# number of genes
N = len(genes)


## define empty edges matrix
edges = np.zeros(shape=(N,N))

## fill up edges matrix with edge weights, using pearson correlation
for i in range(N):
    for j in range(N):
        if i != j:
            cor, p_value = scipy.stats.pearsonr(data[i,:],data[j,:])
            edges[i,j] = abs(cor)


# # more clever way for symmetrical methods
# for i in range(N):
#     for j in range(i+1,N):
#         cor, p_value = scipy.stats.pearsonr(data[i,:],data[j,:])
#         edges[i,j] = abs(cor)
#         edges[j,i] = abs(cor)





## write output


threshold = 0.2

to_write = []

for i in range(N):
    for j in range(N):
        if abs(edges[i,j]) >= threshold:
            to_write.append([genes[i],genes[j],abs(edges[i,j])])



to_write = sorted(to_write, key=itemgetter(2), reverse=True)


f = open("output.txt", "w")

for row in to_write:
    f.write(f"{row[0]}\t{row[1]}\t{row[2]}\n")

f.close()


