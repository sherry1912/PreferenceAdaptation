import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


with open("C:\\Users\\12052\\Desktop\\sherryResearchWork\\attribute_seams工作\\round3_differentation.txt", 'r', encoding='utf-8') as f:
    data = f.readlines()

# print(data)
realdata = {}

for one in data:
    tmp = one.replace("[","").replace("]","").replace(","," ").split(" ")
    w1 = float(tmp[0])
    w2 = float(tmp[1])
#    t = int(one[l+2:l+3])
    t = int(100*float(tmp[3]))
    print(t)
    realdata[(w1,w2)]=t

'''
for one in data:
    i = one.find('[')
    j = one.find(',')
    k = one.find(',',j+1,len(one))
    l = one.find(']')
    # print(k,one[j+1:k])
    # print(one[i+1:j])
    w1 = float(one[i+1:j])
    w2 = float(one[j+1:k])
#    t = int(one[l+2:l+3])
    t = 100*float(one[l+2:l+3])
    print(t)
    realdata[(w1,w2)]=t
'''


flights2=np.zeros((18,18),float)

for i in range(18):
    for j in range(18):
        flights2[i,j]=-1


w1,w2 = 0.05, 0.05
i = 17
while w1<1:
    j = 0
    w2 = 0.05
    while w1+w2<1:
        flights2[i, j] = realdata[(w1, w2)]
        w2 = round(w2 + 0.05, 2)
        j = j + 1
    w1 = round(w1 + 0.05, 2)
    i = i -1




# f, ax = plt.subplots(figsize=(9, 6))
# # sns.heatmap(flights1, annot=True, linewidths=.5, ax=ax,cmap="binary",vmin=0,vmax=4)
# sns.heatmap(flights2, annot=True, linewidths=.5, ax=ax,cmap="winter_r",vmin=-1,vmax=3)
# plt.show()


# corr = np.corrcoef(np.random.randn(10, 200))
mask = np.zeros_like(flights2)
mask[np.triu_indices_from(mask)] = True
for i in range(18):
    mask[i,i] = False
with sns.axes_style("whitegrid"):
    ax = sns.heatmap(flights2, mask =mask,
                     vmin=0,vmax=100, square=True,cmap="BuPu",
                     yticklabels=[0.9,0.85,0.8,0.75,0.7,0.65,0.6,0.55,0.5,0.45,0.4,0.35,
                                  0.3,0.25,0.2,0.15,0.1,0.05],
                     xticklabels=[0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,
                                0.65,0.7,0.75,0.8,0.85,0.9]
                     )
figure = ax.get_figure()
#annot=True,
plt.show()

