import matplotlib.pyplot as plt

def plotData(plt, data, legend, col):
	x = [p[0] for p in data]
	y = [p[1] for p in data]
	plt.plot(x, y, label=legend, color=col)


rightList = list()
leftList = list()
rDot=0
lDot=0

with open('dataLog.txt') as fp:
	for line in fp:
		if line.split(',')[0] == 'R':
			rightList.append((rDot, line.split(',')[1]))
			rDot += 1
		elif line.split(',')[0] == 'L':
			leftList.append((lDot, line.split(',')[1]))
			lDot += 1

#plotData(plt, rightList, 'Right', 'teal')
#plotData(plt, leftList, 'Left', 'brown')
fig = plt.figure()
ax = plt.subplot(111)
ax.plot([p[0] for p in rightList], [p[1] for p in rightList], label='Right')
ax.plot([p[0] for p in leftList], [p[1] for p in leftList], label='Left')
plt.title('Rehab History')
ax.legend(loc='lower right', frameon=False)
plt.savefig('./Rehab History.png')
