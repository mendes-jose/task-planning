import random
import pygraphviz as pgv
from collections import deque

class FluentA(object):
	def __init__(self, value):
		self.value = value
	def holdsIn(self, b):
		if 'A' in [f for f in b]:
			return b['A'] == self.value
		else:
			return False

class FluentB(object):
	def __init__(self, value):
		self.value = value
	def holdsIn(self, b):
		if 'B' in [f for f in b]:
			return b['B'] == self.value
		else:
			return False

class FluentC(object):
	def __init__(self, value):
		self.value = value
	def holdsIn(self, b):
		if 'C' in [f for f in b]:
			return b['C'] == self.value
		else:
			return False

class FluentD(object):
	def __init__(self, value):
		self.value = value
	def holdsIn(self, b):
		if 'D' in [f for f in b]:
			return b['D'] == self.value
		else:
			return False

class FluentE(object):
	def __init__(self, value):
		self.value = value
	def holdsIn(self, b):
		if 'E' in [f for f in b]:
			return b['E'] == self.value
		else:
			return False

class Pre(object):
	def __init__(self, fluent, abstLevel):
		self.fluent = fluent
		self.abstLevel = abstLevel

class Op1(object):
	def __init__(self):
		self.effect = [FluentD(True)]
		self.pre = [Pre(FluentA(True), 1)]
		self._hasPrim = True

	def isPrim(self, abstLevel):
		return self._hasPrim and all([p.abstLevel <= abstLevel for p in self.pre])

class Op2(object):
	def __init__(self):
		self.effect = [FluentE(True)]
		self.pre = [Pre(FluentC(True), 0)]
		self._hasPrim = True

	def isPrim(self, abstLevel):
		return self._hasPrim and all([p.abstLevel <= abstLevel for p in self.pre])

class Op3(object):
	def __init__(self):
		self.effect = [FluentA(True)]
		self.pre = [Pre(FluentB(True), 0)]
		self._hasPrim = True

	def isPrim(self, abstLevel):
		return self._hasPrim and all([p.abstLevel <= abstLevel for p in self.pre])

#class Op4(object):
#	def __init__(self):
#		self.effect = [FluentA(False)]
#		self.pre = [Pre(FluentB(True), 0)]
#
class Agent(object):
	def __init__(self, world, goal):
		self._operators = [Op1(), Op2(), Op3()]
		self._goal = goal
		self._world = world

	def _visit(self, preImage, searchedLeaf, abstLevel):

		childrenPI = list()
#		print '\n\nFATHER\n', preImage, '\n\n'
		random.shuffle(self._operators)
		for op in self._operators:

			childPreImage = list()
			
#			print '\n\nOP\n', op, '\n\n'
#			print '\n\nOP EFFECT\n', op.effect, '\n\n'
#			print '\n\nOP PRECOND\n', [p.fluent for p in op.pre], '\n\n'
			for f1 in preImage:
				takeF1Out = False
				for f2 in op.effect:
					if type(f1) == type(f2):
						takeF1Out = True
						break
				if not takeF1Out:
					childPreImage.append(f1)

			for precond in op.pre:
				doNotAdd = False
				if precond.abstLevel <= abstLevel:
					for f3 in childPreImage:
						if type(f3) == type(precond.fluent):
							doNotAdd = True
							break
					if not doNotAdd:
						childPreImage.append(precond.fluent)

			childrenPI.append([op, childPreImage])
		# print '\n\n CHILD \n', childrenPI ,'\n\n'
		return childrenPI

	def _plan(self, bnow, goal, abstLevel):

		root = goal
		searchedLeaf = bnow

		if all([f.holdsIn(searchedLeaf) for f in root]):
			return []

		tree = list()
		tree.append([[None, root], None])
		cntr = 0
		findSearchedLeaf = False

		while True:

			preImage = tree[cntr][0]

			pImages = self._visit(preImage[1], searchedLeaf, abstLevel)

			for preImage in pImages:

				tree.append([preImage, cntr])

				if all([f.holdsIn(searchedLeaf) for f in preImage[1]]):
					findSearchedLeaf = True
					break

			if findSearchedLeaf:
				break
			
			cntr += 1

		# save tree in DOT format
		file = open('./mygraph.dot', 'w')
		file.write('digraph planningTree {\n')
		file.write('\tr0 [label="' + '^\\n'.join([type(f).__name__ for f in root]) + '", shape=box];\n')
		fid = 0
		cntr = 1
		fName = 'r0'

		while cntr < len(tree):
			if tree[cntr][1] != fid:
				fName = 'r' + str(tree[cntr][1])
				fid = tree[cntr][1]
				continue
			file.write('\tr' + str(cntr) + ' [label="' + '^\\n'.join([type(f).__name__ for f in tree[cntr][0][1]]) + '", shape=box];\n')
			file.write('\tr' + str(cntr) + ' -> ' + fName + ' [label="' + type(tree[cntr][0][0]).__name__ + '"];\n')
			cntr += 1

		# get solution path from tree
		plan = list()
		idx = len(tree)-1
		while idx > 0:
			plan.append(tree[idx][0])
#			file.write('\tr' + str(idx) + ' -> ' + 'r' + str(tree[idx][1]) + ' [color=red, label="' + type(tree[idx][0][0]).__name__ + '"];\n')
			file.write('\tr' + str(idx) + '[color = red];\n')
			idx = tree[idx][1]


		file.write('}')
		file.close()
		G = pgv.AGraph("./mygraph.dot")
		G.layout(prog='dot')
		G.draw('mygraph.png')

		return plan

	def _nextLevel(self, abstLevel, operator):
		return abstLevel + 1;

	def _bHPN(self, bnow, goal, abstLevel):

		#print bnow
		print '\nGOAL:\n', goal, '\n'
		#print abstLevel

		p = self._plan(bnow, goal, abstLevel) # updates

		print '\n\nPLAN ( abs=', abstLevel, '):\n', p, '\n\n'

		if len(p) == 0:
			return goal

		while True:
			
			currBHoldingList = [all([f.holdsIn(bnow) for f in wg[1]]) for wg in p] # while bnow is in union_{i = 0}^{n-1} g_i(p)

			if any(currBHoldingList) != True:
				break

			index = (len(currBHoldingList) - 1) - currBHoldingList[::-1].index(True)
			
			if p[index][0].isPrim(abstLevel):
				print '\nExecute:\n', p[index][0], '\n'
				#obs = world.execute(p[index][0])
				#bnow.update(p[index][0], obs)
				# SIMPLIFING:
				bnow = self._world.execute(p[index][0])
			else:
				newGoal = goal if index+1 >= len(p) else p[index+1][1]
				bnow = self._bHPN(bnow, newGoal, self._nextLevel(abstLevel, p[index][0]))

			if all([f.holdsIn(bnow) for f in goal]):
				break

		return bnow

	def _bHPNTOp(self):
		bnow = self._world.bnow
		file = open('./hpngraph.dot', 'w')
		file.write('digraph hpnTree {\n')
		while not all([f.holdsIn(bnow) for f in self._goal]):
			bnow = self._bHPN(bnow, self._goal, 0)

	def go(self):
		self._bHPNTOp()



class WorldSim(object):
	""" This class is a container of all simulation elements and also the
	interface for running the simulation.
	"""

	def __init__(self, binit):
		self.bnow = binit

	def execute(self, operator):
		for eff in operator.effect:
			#TODO
			if not eff.holdsIn(self.bnow):
				if type(eff) == FluentA:
					if random.uniform(0, 1) < 0.8:
						self.bnow['A'] = eff.value
					else:
						self.bnow[random.choice('BCDE')] = random.choice([True, False])
				elif type(eff) == FluentB:
					if random.uniform(0, 1) < 0.8:
						self.bnow['B'] = eff.value
					else:
						self.bnow[random.choice('ACDE')] = random.choice([True, False])
				elif type(eff) == FluentC:
					if random.uniform(0, 1) < 0.8:
						self.bnow['C'] = eff.value
					else:
						self.bnow[random.choice('ABDE')] = random.choice([True, False])
				elif type(eff) == FluentD:
					if random.uniform(0, 1) < 0.8:
						self.bnow['D'] = eff.value
					else:
						self.bnow[random.choice('ABCE')] = random.choice([True, False])
				elif type(eff) == FluentE:
					if random.uniform(0, 1) < 0.8:
						self.bnow['E'] = eff.value
					else:
						self.bnow[random.choice('ABCD')] = random.choice([True, False])
		return self.bnow


# MAIN ########################################################################

if __name__ == '__main__':

	binit = {'B': True, 'C': True, 'D': False}
	goal = [FluentD(True), FluentE(True)]

	w = WorldSim(binit)

	a = Agent(w, goal)

	a.go()
