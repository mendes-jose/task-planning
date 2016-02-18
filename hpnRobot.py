"""
The :mod:`hpnRobot` module implements classes and functions to simulate a
scenarion.

.. codeauthor:: Jose Magno MENDES FILHO <josemagno.mendes@gmail.com>
"""
# 03/2016
# Copyright 2015 CEA

import random
import pygraphviz as pgv
import math
from collections import deque

__version__ = '1.0.1'

def merge_two_dicts(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    z = x.copy()
    z.update(y)
    return z

###############################################################################
# (Belief) state
###############################################################################
class BeliefState(object):
	""" Belief state class
	"""
	def __init__(self, shelfs, delivZones, objects, robots):
		""" Constructor
		"""
		self.shelfs = shelfs
		self.delivZones = delivZones
		self.objects = objects
		self.robots = robots
		self.allCont = merge_two_dicts(shelfs, delivZones)
		self.allCont.update(objects)
		self.allCont.update(robots)

	def update(self, operator, observation):
		""" Belief state estimator. Uses previous belief state, observation and operator to estimate the new belief state

		.. todo:: Make this function an UKF update
		"""

		# UPDATE SPACE TOO !!! TODO
		# if a object that is not in the belief state was seen the discrete
		# space has to be updated

		return observation
		#if operator == None:




###############################################################################
# Fluents
###############################################################################

class Fluent(object):
	""" Base class for implementing fluents. Intaces of fluents represent the subset of states such as, for each possible state in that subset, the fluent with the given arguments has value equals to the value argument
    """
	def __init__(self, value, **kwargs):
		""" Class constructor

		Input
        	*value*: value of the fluent
        	*kwargs*: dictionary of arguments
		"""
		self.value = value
		""" Fluent value
		"""
		self.kwargs = kwargs
		""" Dictionary of arguments
		"""
		self._argsDic = kwargs

	def _loadVarArgs(self, b, **kwargs):
		""" Method for loading variable arguments
		"""
		self._argsDic = self.kwargs
		for k, v in kwargs.iteritems():
			self._argsDic[k] = v

class BIn(Fluent):
	""" BIn(obj, R) fluent
	"""
	def holdsIn(self, b, **kwargs):
		""" T(BIn, b, obj, R)
		"""

		Fluent._loadVarArgs(self, b, kwargs)

		# check stuff
		if not self._argsDic['objID'] in b.allCont:
			# if obj is not in belief state, let us assume
			# that the robot does not belief that obj is in R
			return False

		return True if b.allCont[self._argsDic['objID']].isIn(
				self._argsDic['reg']) else False

class BOverlaps(Fluent):
	""" BOverlaps(obj, R) fluent
	"""
	def holdsIn(self, b, **kwargs):
		""" T(BOverlaps, b, obj, R)
		"""

		Fluent._loadVarArgs(self, b, kwargs)

		# check stuff
		if not self._argsDic['objID'] in b.allCont:
			# if obj is not in belief state, let us assume
			# that the robot does not belief that obj is in R
			return False

		return True if b.allCont[self._argsDic['objID']].overlaps(self._argsDic['reg']) else False
		# Check if region will be indeed updated here when updated in b

class BClear(Fluent):
	""" BClear(R, objs) fluent
	"""
	def holdsIn(self, b, **kwargs):
		""" T(BClear, b, R, objs)
		"""
		Fluent._loadVarArgs(self, b, kwargs)

		#knownObjs = [v for k, v in b.iteritems() if type(v) == type(Object())]

		# check if that space is free in the space representation
		# if not return False (the robot does not belief that the R is clear)

		# else, if any of the objects in the objs list is not in b, it does
		# not matter its a exeption list

		# else, check if any of b obstacles that are not in objs overlaps
		# R

		boolArr = [obj.overalps(self._argsDic['reg']) for objID, objV in
				merge_two_dicts(b.objects, b.robots).iteritems() if objID
				not in self._argsDic['listObjs']]

		return False if any(boolArr) else True

class BHolding(Fluent):
	""" Holding(obj) fluent
	"""
	def holdsIn(self, b, **kwargs):
		""" T(Holding, b, obj)
		"""
		Fluent._loadVarArgs(self, b, kwargs)

		return True if b['g'] == self._argsDic['obj'] else False

###############################################################################
# Objects
###############################################################################

class RecObject(object):
	""" Rectangular representation of a object
	"""
	def __init__(self, eyed, length, width, x, y, theta):
		""" Class constructor

		Input
			*eyed*: object ID
			*length*: object length
			*width*: object width
			*x*: object x position
			*y*: object y position
			*theta*: object orientation
		"""
		self.eyed = eyed
		""" ID
		"""
		self.w = width
		""" width
		"""
		self.l = length
		""" length
		"""
		self.x = x
		""" x
		"""
		self.y = y
		""" y
		"""
		self.t = theta
		""" theta
		"""

	def isIn(self, reg):
		""" Return true if the object is entirely inside the region *reg*
		"""

	def overlaps(self, reg):
		"""
		"""

class RobotObject(object):
	""" Representation of a robot
	"""
	def __init__(self, eyed, length, width, x, y, theta, g, detecRad,
			detecField, sizeOfGridInMeters):
		""" Class constructor

		Input
			*eyed*: robot eyed
			*length*: robot length
			*width*: robot width
			*x*: robot x position
			*y*: robot y position
			*theta*: robot orientation
			*g*: robot gripper state
		"""
		self.eyed = eyed
		""" robot ID
		"""
		self.w = width
		""" width
		"""
		self.l = length
		""" length
		"""
		self.x = x
		""" x
		"""
		self.y = y
		""" y
		"""
		self.t = theta
		""" theta
		"""
		self.g = g
		""" gripper state
		"""
		self.detecRad = detecRad
		""" gripper state
		"""
		self.detecField = detecField
		""" gripper state
		"""
		self._sizeOfGridInMeters = sizeOfGridInMeters
		""" gripper state
		"""


	def isIn(self, reg):
		""" Return true if the object is entirely inside the region *reg*
		"""

	def overlaps(self, reg):
		"""
		"""

###############################################################################
# Operators
###############################################################################

#class Operator(object):
#	def __init__(self):

#class Pick(object):
#	def __init__(self):


# class Op1(object):
# 	def __init__(self):
# 		self.effect = [FluentD(True)]
# 		self.pre = [Pre(FluentA(True), 1)]
# 		self._hasPrim = True

# 	def isPrim(self, abstLevel):
# 		return self._hasPrim and all([p.abstLevel <= abstLevel for p in self.pre])

# class Op2(object):
# 	def __init__(self):
# 		self.effect = [FluentE(True)]
# 		self.pre = [Pre(FluentC(True), 0)]
# 		self._hasPrim = True

# 	def isPrim(self, abstLevel):
# 		return self._hasPrim and all([p.abstLevel <= abstLevel for p in self.pre])

# class Op3(object):
# 	def __init__(self):
# 		self.effect = [FluentA(True)]
# 		self.pre = [Pre(FluentB(True), 0)]
# 		self._hasPrim = True

# 	def isPrim(self, abstLevel):
# 		return self._hasPrim and all([p.abstLevel <= abstLevel for p in self.pre])

# class Pre(object):
# 	def __init__(self, fluent, abstLevel):
# 		self.fluent = fluent
# 		self.abstLevel = abstLevel

class Agent(object):
	""" Agent, the decision maker class
	"""
	def __init__(self, world, goal, operators):
		""" Class constructor

		Input
			*world*: where operations take place and observations come from
			*goal*: agent's goal
			*operators*: agent's operators
		"""
		self._operators = operators
		self._goal = goal
		self._world = world
		self._planCounter = 0
		self._execCounter = 0
		self._file = open('./execGraph.dot', 'w')
		self._file.write('digraph execTree {\n')
		

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
		file = open('./planningGraph' + str(self._planCounter) + '.dot', 'w')
		file.write('digraph planningTree {\n')
		file.write('\tr0 [label="GOAL\n' + '^\\n'.join([type(f).__name__ for f in root]) + '", shape=box, color=red];\n')
		fid = 0
		cntr = 1
		fName = 'r0'

		while cntr < len(tree):
			if tree[cntr][1] != fid:
				fName = 'r' + str(tree[cntr][1])
				fid = tree[cntr][1]
				continue
			file.write('\tr' + str(cntr) + ' [label="' + '^\\n'.join([type(f).__name__ for f in tree[cntr][0][1]]) + '", shape=box];\n')
			file.write('\tr' + str(cntr) + ' -> ' + fName + ' [label="' + type(tree[cntr][0][0]).__name__ + '_' + str(abstLevel) + '"];\n')
			cntr += 1

		# get solution path from tree
		plan = list()
		idx = len(tree)-1
		while idx > 0:
			plan.append(tree[idx][0])
			file.write('\tr' + str(idx) + '[color = green];\n')
			idx = tree[idx][1]

		file.write('\tbnow [shape=box, color=blue, label="b_{now} = ' + str(bnow) + '"];\n')
		file.write('\tbnow -> r' + str(len(tree)-1) + ' [label="in", style=dotted];\n')

		file.write('}')
		file.close()
		G = pgv.AGraph('./planningGraph' + str(self._planCounter) + '.dot')
		G.layout(prog='dot')
		G.draw('planningGraph' + str(self._planCounter) + '.png')

		self._planCounter += 1

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
				self._world.execute(p[index][0])
				obs = self._world.observe(self._eyed)
				bnow.update(p[index].operator, obs)
				self._execCounter += 1
				self._file.write('\tb_' +str(self._execCounter) + ' [label="b = ' + str(bnow) + '", shape=box, color=blue]\n')
				self._file.write('\tb_' + str(self._execCounter-1) + ' -> ' +
					'b_' + str(self._execCounter) + '[label="' + type(p[index][0]).__name__ + '"]\n' )
				
			else:
				newGoal = goal if index+1 >= len(p) else p[index+1][1]
				#self._hpnCounter += 1
				bnow = self._bHPN(bnow, newGoal, self._nextLevel(abstLevel, p[index][0]))

			if all([f.holdsIn(bnow) for f in goal]):
				break

		return bnow

	def _bHPNTOp(self):
		bnow = self._world.observe()
		self._file.write('\tb_0 [label="b = ' + str(bnow) + '", shape=box, color=blue]\n')
		while not all([f.holdsIn(bnow) for f in self._goal]):
			#self._hpnCounter += 1
			bnow = self._bHPN(bnow, self._goal, 0)

	def go(self):
		self._bHPNTOp()

		self._file.write('}')
		self._file.close()
		G = pgv.AGraph('./execGraph.dot')
		G.layout(prog='dot')
		G.draw('execGraph.png')


class Robot(Agent):
	""" Robot who makes decisions and acts on the world
	"""
	def __init__(self, eyed, world, goal, operators, bShelfs, bDelivZones, bObjects, bRobots):
		""" Class constructor

		Input
			*eyed*: robot ID
			*world*: where operations take place and observations come from
			*goal*: agent's goal
			*operators*: agent's operators
			*bShelfs*: dictionary with known shelfs ID as keys and Object
			instances as values
			*bDelivZones*: dictionary with known delivZones ID as keys and
			Object instances as values
			*bRobots*: dictionary with known robots ID as keys and Object
			instances as values
		"""
		self._eyed = eyed

		Agent.__init__(self, world, goal, operators)



class WorldSim(object):
	""" This class is a container of all simulation elements and also the
	interface for running the simulation.
	"""
	def __init__(
		self, worldLength = 10.0,
		worldWidth = 10.0,
		shelfs,
		delivZone,
		objects,
		robots):

		self.wl = worldLength
		self.ww = worldWidth
		#self.size
		self._shelfs = shelfs
		self._objects = objects
		self._robots = robots

		self._odomet =
		{
			'x': 0.0,
			'y': 0.0,
			'theta': 0.0
		}

		#self.occGrid = [[0]*worldLength/sizeOfGridInMeters]*worldWidth/sizeOfGridInMeters


	def observe(self, rID):
		
		obs = {}

		for objID, objV in self._objects.iteritems():
			if objV.overlaps(robots[rID].x, robots[rID].y, robots[rID].t,
					robots[rID].detecRad, robot[rID].detecField):
				# put this objecjt id, pose (relative to true robot pose) in
				# the return information
				obs[objID] =
				{
					'x': objV.x - robots[rID].x
					'y': objV.y - robots[rID].y
					'theta': wrapAng(objV.t - robots[rID].t)
				}

		for objID, objV in self._shelfs.iteritems():
			if objV.overlaps(robots[rID].x, robots[rID].y, robots[rID].t,
					robots[rID].detecRad, robot[rID].detecField):
				# put this shelf id, pose (relative to true robot pose) in
				# the return information
				obs[objID] =
				{
					'x': objV.x - robots[rID].x
					'y': objV.y - robots[rID].y
					'theta': wrapAng(objV.t - robots[rID].t)
				}

		for objID, objV in self._robots.iteritems():
			if objID != rID and objV.overlaps(robots[rID].x,
					robots[rID].y, robots[rID].t,
					robots[rID].detecRad, robot[rID].detecField):
				# put this robot id, pose (relative to true robot pose) in
				# the return information
				obs[objID] =
				{
					'x': objV.x - robots[rID].x
					'y': objV.y - robots[rID].y
					'theta': wrapAng(objV.t - robots[rID].t)
				}

		obs['odomet'] = self._odomet

		return obs

	def execute(self, operator):

#		for eff in operator.effect:
#			#TODO
#			if not eff.holdsIn(self.bnow):
#				if type(eff) == FluentA:
#					if random.uniform(0, 1) < 0.8:
#						self.bnow['A'] = eff.value
#					else:
						#self.bnow[random.choice('BCDE')] = random.choice([True, False])
#				elif type(eff) == FluentB:
#					if random.uniform(0, 1) < 0.8:
#						self.bnow['B'] = eff.value
#					else:
						#self.bnow[random.choice('ACDE')] = random.choice([True, False])
#				elif type(eff) == FluentC:
#					if random.uniform(0, 1) < 0.8:
#						self.bnow['C'] = eff.value
#					else:
						#self.bnow[random.choice('ABDE')] = random.choice([True, False])
#				elif type(eff) == FluentD:
#					if random.uniform(0, 1) < 0.8:
#						self.bnow['D'] = eff.value
#					else:
						#self.bnow[random.choice('ABCE')] = random.choice([True, False])
#				elif type(eff) == FluentE:
#					if random.uniform(0, 1) < 0.8:
#						self.bnow['E'] = eff.value
#					else:
						#self.bnow[random.choice('ABCD')] = random.choice([True, False])
#		return self.bnow


# MAIN ########################################################################

if __name__ == '__main__':


	worldLength = 10.0
	worldWidth = 10.0

	sizeOfGridInMeters = 0.1

	shelf0 =
	{
		'eyed': 'shelf0',
		'length': 1.0,
		'width': 6.0,
		'x': 3.5,
		'y': 5.0,
		'theta': 0.0
	}

	shelf1 =
	{
		'eyed': 'shelf1',
		'length': 1.0,
		'width': 6.0,
		'x': 6.5,
		'y': 5.0,
		'theta': 0.0
	}

	delivZone0 =
	{
		'eyed': 'delivZone0',
		'length': 3.0,
		'width': 1.0,
		'x': 8.5,
		'y': 9.5,
		'theta': 0.0
	}

	product0 =
	{
		'eyed': 'obj0',
		'length': 0.2,
		'width': 0.2,
		'x': 4.1,
		'y': 7.0,
		'theta': 0.0
	}

	product0 =
	{
		'eyed': 'obj1',
		'length': 0.2,
		'width': 0.2,
		'x': 4.1,
		'y': 7.0,
		'theta': 0.0
	}

	robot0 =
	{
		'eyed': 'bb8'
		'length': 0.5,
		'width': 0.5,
		'x': 4.1,
		'y': 7.0,
		'theta': math.pi/2.0
		'g': False
		'detecRad': 4
		'detecField': math.pi
		'sizeOfGridInMeters': 0.01
	}

	###########################################################################
	# World absolute information
	###########################################################################
	objects =
	{
		product1['eyed']: RecObject(**product1),
		product2['eyed']: RecObject(**product2)
	}

	delivZones =
	{
		delivZone0['eyed']: RecObject(**delivZone0)
	}

	shelfs =
	{
		shelf0['eyed']: RecObject(**shelf0),
		shelf1['eyed']: RecObject(**shelf1)
	}
	###########################################################################
	# Agent robot belief information
	###########################################################################
	bObjects =
	{
		product1['eyed']: RecObject(**product1),
		product2['eyed']: RecObject(**product2)
	}

	bDelivZones =
	{
		delivZone0['eyed']: RecObject(**delivZone0)
	}

	bShelfs =
	{
		shelf0['eyed']: RecObject(**shelf0),
		shelf1['eyed']: RecObject(**shelf1)
	}

	bRobots =
	{
		robot0['eyed']: RobotObject(**robot0)
	}

	operators = [Pick(), Place(), MoveRobot(), LookToVerify(), Clear()]

	w = WorldSim(worldLength, worldWidth, shelfs, delivZones, objects, robots)

	goal = [BIn(True, objID=objects[0]['eyed'],
			reg=bDelivZones[delivZone0['eyed']])]

	r = Robot(bRobots[0]['eyed'], w, goal, operators, bShelfs, bDelivZones, bObjects, bRobots)

	r.go()
