from collections import deque
import os
import time

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

	def _plan(self, bnow, abstLevel):

		root = self._goal
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

		# get solution path from tree
		plan = list()
		idx = len(tree)-1
		while idx > 0:
			plan.append(tree[idx][0])
			idx = tree[idx][1]

		return plan

	def _nextLevel(self, abstLevel, operator):
		return abstLevel + 1;

	def _bHPN(self, bnow, goal, abstLevel):

		#print bnow
		print '\nGOAL:\n', goal, '\n'
		#print abstLevel

		p = self._plan(bnow, abstLevel) # updates

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
					self.bnow['A'] = eff.value
				elif type(eff) == FluentB:
					self.bnow['B'] = eff.value
				elif type(eff) == FluentC:
					self.bnow['C'] = eff.value
				elif type(eff) == FluentD:
					self.bnow['D'] = eff.value
				elif type(eff) == FluentE:
					self.bnow['E'] = eff.value
		return self.bnow


# MAIN ########################################################################

if __name__ == '__main__':

	binit = {'B': True, 'C': True, 'D': False}
	goal = [FluentD(True), FluentE(True)]

	w = WorldSim(binit)

	a = Agent(w, goal)

	a.go()
