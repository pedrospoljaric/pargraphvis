import time
start_time = time.time()

import sys
from gexf import Gexf

def formatTime(time):
	if 'e+' in time:
		calctime = time.split('e+')
		time = str(float(calctime[0]) * pow(10, int(calctime[1])))		  
	elif 'e-' in time:
		calctime = time.split('e-')
		time = str(float(calctime[0]) * pow(10, int(calctime[1]) * (-1)))	
	return time

lsArgs = sys.argv

trace_file = open(lsArgs[1], 'r')
trace_lines = trace_file.readlines()
trace_file.close()

gexf = Gexf("Pedro and David", "Dynamic graph")
graph = gexf.addGraph("directed", "dynamic", "Graph")
idTotalNodeDuration = graph.addNodeAttribute("Total Duration", "0.0", "float") #name, default, type
idTotalEdgeDuration = graph.addEdgeAttribute("Total Duration", "0.0", "float")
idLinkType = graph.addEdgeAttribute("Type", "None", "string")
idNumMsgs = graph.addEdgeAttribute("Number of messages", "0", "integer")

dicEvents = {}

i = 0
while (trace_lines[i].startswith('%') == True):

	if ('%EventDef' in trace_lines[i]):
	
		lsLine = trace_lines[i].split(' ')
		eventName = str(lsLine[1])
		eventId = lsLine[2].replace('\n', '')
		
		dicEvents[eventName] = eventId
	
	i += 1

dicValues = [dicEvents['PajeCreateContainer'], dicEvents['PajeDestroyContainer'], dicEvents['PajeStartLink'], dicEvents['PajeEndLink']]

totalNodes = 0
dicNodes = {}
dicEdges = {}
i2 = i
for i in range(i2, len(trace_lines)):

	if (trace_lines[i].startswith(dicValues[0])) and ('CT_Thread' in trace_lines[i]):
	
		lsLine = trace_lines[i].split(' ')
		
		items = []
		items.append(lsLine[0])
		
		j = 1		
		while True:		
			
			it = ''
			
			if (str(lsLine[j])[0] == '"'):
				while True:
					it += str(lsLine[j])
					j += 1
					if (len(str(lsLine[j-1])) > 0):
						if (str(lsLine[j-1])[-1] == '"' or str(lsLine[j-1]).endswith('\n')): break
					it += ' '
					
			else:
				it += str(lsLine[j])
				j += 1
			
			items.append(it.replace('\n', ''))
				
			if '\n' in it: break
			
		idNode = int((((items[2].split('_'))[0]).split('#'))[1])
		
		dicNodes[idNode] = []
		(dicNodes[idNode]).append(formatTime(items[1]))
		
		totalNodes += 1
	
	elif (trace_lines[i].startswith(dicValues[1])) and ('CT_Thread' in trace_lines[i]):
	
		lsLine = trace_lines[i].split(' ')
		
		items = []
		items.append(lsLine[0])
		
		j = 1		
		while True:		
			
			it = ''
			
			if str(lsLine[j])[0] == '"':			
				while True:
					it += str(lsLine[j])
					j += 1
					if (len(str(lsLine[j-1])) > 0):
						if (str(lsLine[j-1])[-1] == '"' or str(lsLine[j-1]).endswith('\n')): break
					it += ' '
					
			else:
				it += str(lsLine[j])
				j += 1
			
			items.append(it.replace('\n', ''))
				
			if '\n' in it: break
			
		idNode = int((((items[2].split('_'))[0]).split('#'))[1])
		
		(dicNodes[idNode]).append(formatTime(items[1]))
	
	elif (trace_lines[i].startswith(dicValues[2])):
	
		lsLine = trace_lines[i].split(' ')
		
		items = []
		items.append(lsLine[0])
		
		j = 1		
		while True:		
			
			it = ''
			
			if str(lsLine[j])[0] == '"':			
				while True:
					it += str(lsLine[j])
					j += 1
					if (len(str(lsLine[j-1])) > 0):
						if (str(lsLine[j-1])[-1] == '"' or str(lsLine[j-1]).endswith('\n')): break
					it += ' '
					
			else:
				it += str(lsLine[j])
				j += 1
			
			items.append(it.replace('\n', ''))
				
			if '\n' in it: break
			
		linkBet = str(items[6])
		
		tipoLink = 'Collective'
		
		if ('L_MPI_P2P' in trace_lines[i]):
			weight = ((items[5].split(', '))[2]).replace('len=', '')
			tipoLink = 'P2P'
		else: weight = '1'
		
		if (linkBet not in dicEdges): dicEdges[linkBet] = []
		if len(dicEdges[linkBet]) == 0:
			(dicEdges[linkBet]).append(tipoLink)
			(dicEdges[linkBet]).append(linkBet)
			(dicEdges[linkBet]).append(weight)
		(dicEdges[linkBet]).append(float(formatTime(items[1])))
			
	elif (trace_lines[i].startswith(dicValues[3])):
		
		lsLine = trace_lines[i].split(' ')
		
		items = []
		items.append(lsLine[0])
		
		j = 1		
		while True:		
			
			it = ''
			
			if str(lsLine[j])[0] == '"':			
				while True:
					it += str(lsLine[j])
					j += 1
					if (len(str(lsLine[j-1])) > 0):
						if (str(lsLine[j-1])[-1] == '"' or str(lsLine[j-1]).endswith('\n')): break
					it += ' '
					
			else:
				it += str(lsLine[j])
				j += 1
			
			items.append(it.replace('\n', ''))
				
			if '\n' in it: break
			
		linkBet = str(items[6])
		
		tipoLink = 'Collective'
		
		if ('L_MPI_P2P' in trace_lines[i]):
			weight = ((items[5].split(', '))[2]).replace('len=', '')
			tipoLink = 'P2P'
		else: weight = '1'
		
		if (linkBet not in dicEdges): dicEdges[linkBet] = []
		if len(dicEdges[linkBet]) == 0:
			(dicEdges[linkBet]).append(tipoLink)
			(dicEdges[linkBet]).append(linkBet)
			(dicEdges[linkBet]).append(weight)
		(dicEdges[linkBet]).append(float(formatTime(items[1])))

lsEdges = dicEdges.values()
mapEdges = map(list, zip(*lsEdges))
lsEdges = zip(mapEdges[3], mapEdges[4], mapEdges[1], mapEdges[2], mapEdges[0])
lsEdges.sort()

lsEdges = zip(*lsEdges)
lsEdges[0] = list(lsEdges[0])
lsEdges[1] = list(lsEdges[1])
lsEdges[2] = list(lsEdges[2])
lsEdges[3] = list(lsEdges[3])
lsEdges[4] = list(lsEdges[4])
		
for key in dicNodes:

	if (dicNodes[key])[1]:
		graph.addNode(str(key), 'P#'+str(key))#, str((dicNodes[key])[0]), str((dicNodes[key])[1]))
	else:
		graph.addNode(str(key), 'P#'+str(key))#, str((dicNodes[key])[0]))

dicL = {} # dl = dicLinks
for n1 in range(totalNodes):
	for n2 in range(totalNodes):
		if (n2 != n1):		
			dicL[str(n1) + '_' + str(n2)] = [[], [], [], []] # []start []end []weight []type

maxt = 0
for i in range(len(lsEdges[0])):

	edgeSource = (((lsEdges[2])[i].split('_'))[0]).replace('"', '')
	edgeTarget = ((lsEdges[2])[i].split('_'))[1]
	edgeStart = float((lsEdges[0])[i])
	edgeEnd = float((lsEdges[1])[i])
	edgeLen = float((lsEdges[3])[i])
	edgeType = str(lsEdges[4][i])
	
	rn = edgeSource + '_' + edgeTarget	# rn = relatedNodes
	if len((dicL[rn])[0]) == 0:
	
		(dicL[rn])[0].append(edgeStart)
		(dicL[rn])[1].append(edgeEnd)
		(dicL[rn])[2].append(edgeLen)
		(dicL[rn])[3].append(edgeType)
		
	else:
		
		lsStartTimes = (dicL[rn])[0]
		
		t = -1
		while edgeStart < float(lsStartTimes[t]) and float(lsStartTimes[t]) != float(lsStartTimes[0]):
			t -= 1
		
		k = len(dicL[rn][0]) + t
		
		for j in range(k, len(dicL[rn][0])):
			
			if ((dicL[rn])[1])[j] > edgeStart:
			
				newStart = max(edgeStart, dicL[rn][0][j])
				newEnd = min(dicL[rn][1][j], edgeEnd)
				newWeight = dicL[rn][2][j] + edgeLen
				
				edgeEnd = max(edgeEnd, dicL[rn][1][j])
				if (edgeEnd == dicL[rn][1][j]): edgeLen = dicL[rn][2][j]
				edgeStart = newEnd
				
				dicL[rn][1][j] = newStart
				
				(dicL[rn])[0].append(newStart)
				(dicL[rn])[1].append(newEnd)
				(dicL[rn])[2].append(newWeight)
				(dicL[rn])[3].append(edgeType)
			
		(dicL[rn])[0].append(edgeStart)
		(dicL[rn])[1].append(edgeEnd)
		(dicL[rn])[2].append(edgeLen)
		(dicL[rn])[3].append(edgeType)
		
id = 0
for item in dicL:

	for i in range(len((dicL[item])[0])):
		
		if ((dicL[item])[0])[i] != ((dicL[item])[1])[i]:
		
			id += 1
			srcdst = item.split('_')
			edgeDuration = ((dicL[item])[1])[i] - ((dicL[item])[0])[i]
			e = graph.addEdge(str(id), str(srcdst[0]), str(srcdst[1]), ((dicL[item])[2])[i], str(dicL[item][0][i]), str(((dicL[item])[1])[i]), str(item))
			e.addAttribute(idLinkType, dicL[item][3][i])
			e.addAttribute(idTotalEdgeDuration, str(edgeDuration))

import os
dir = ('Grafos/' + (lsArgs[1].split('.'))[0]).replace('arq\\', '')
try:
	os.mkdir(dir)
except OSError:
	print 'Pasta ja existe'
gexf_file = open(dir + "/" + ((lsArgs[1].split('.'))[0]).replace('arq\\', '') + ".gexf", "w")
gexf.write(gexf_file)

print("::.. %s seconds ..::" % (time.time() - start_time))