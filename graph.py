import matplotlib.pyplot as plt

x = [171,170,171,167,168]
y = [423,338,287,257,246]
z = [927,677,321,261,253]

fig = plt.figure()#subplots(nrows=1, ncols=3, figsize=(3, 5), sharey=True) 
fig.suptitle("Time to change 5 passwords")
ax1 = fig.add_subplot(131)
ax2 = fig.add_subplot(132,sharey=ax1)
ax2.get_yaxis().set_visible(False)
ax3 = fig.add_subplot(133,sharey=ax1)
ax3.get_yaxis().set_visible(False)
ax1.set_ylabel("Time (s)")
ax1.boxplot(x, labels=["Aiakos"], showmeans=True)
ax2.boxplot(y, labels=["Operator 1"], showmeans=True)
ax3.boxplot(z, labels=["Operator 2"], showmeans=True)
plt.savefig("aiakos_graph.png")
