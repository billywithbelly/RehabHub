import matplotlib.pyplot as plt

def plotData(plt, data, legend, col):
	x = [p[0] for p in data]
	y = [p[1] for p in data]
	plt.plot(x, y, label=legend, color=col)


rightList = list()
leftList = list()
rightList.append((0,0))
leftList.append((0,0))


alist = [line.rstrip() for line in open('dataLog.txt')]
for line in alist:
	if line.split(',')[0] == 'R':
		rightList.append((line.split(',')[1], line.split(',')[2]))
	elif line.split(',')[0] == 'L':
		leftList.append((line.split(',')[1], line.split(',')[2]))


#plotData(plt, rightList, 'Right', 'teal')
#plotData(plt, leftList, 'Left', 'brown')
fig = plt.figure()
ax = plt.subplot(111)
ax.scatter([x[0] for x in rightList if x[1] != 0], [x[1] for x in rightList if x[1] != 0], color='red', label='Right')
ax.scatter([x[0] for x in leftList if x[1] != 0], [x[1] for x in leftList if x[1] != 0], color='cyan', label='Left')
#ax.plot([x[0] for x in rightList if x[1] != 0], [x[1] for x in rightList if x[1] != 0], label='Right')
#ax.plot([x[0] for x in leftList if x[1] != 0], [x[1] for x in leftList if x[1] != 0], label='Left')
plt.title('Rehab History')
ax.legend(loc='lower right', frameon=False)
plt.savefig('./Rehab History.png')
