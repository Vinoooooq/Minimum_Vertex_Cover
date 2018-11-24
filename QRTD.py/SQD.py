import matplotlib.pyplot as plt
import os

def plotSQD(filename, optimal):
	timeArr = []
	sol = []
	trace = open(filename, 'r')
	for line in trace:
		info= list(map(lambda x: x, line.split(',')))
		timeArr.append(float(info[0]))
		sol.append(int(info[1]))
	trace.close()
	print timeArr
	print sol
	top = max(timeArr)
	but = min(timeArr)
	size = len(sol)
	step = (top - but) / 10
	timestep = [(i + 6) * step + but for i in range(5)]
	x = []
	y = []
	for a in range(5):	
		x.append([])
		y.append([])
		for i in range(20):
			thredshold = optimal + (i + 1) * 0.05 * optimal
			count = 0
			for idx in range(len(timeArr)):
				if timeArr[idx] > timestep[a]:
					break
				if sol[idx] <= thredshold:
					count += 1
			x[a].append(1+(i + 1) * 0.05)
			y[a].append(1.0 * count / len(sol))
			print a
			print y[a]
		plt.plot(x[a],y[a],label=str(timestep[a])+' seconds')
	plt.legend()
	plt.show()



name = './ls2.trace'
plotSQD(name, 4542)


