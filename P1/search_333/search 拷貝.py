# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).

Good luck and happy searching!
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())

    Data structures to be used for depth first graph search
    frontier = util.Stack()
    exploredSet = set()

    to choose a leaf node and and remove it from the frontier use
        node = frontier.pop()

    to check if the frontier is empty and return no solution use
        if frontier.isEmpty(): return None

    to add to the frontier use
        frontier.push(...)

    to add to the exploredSet use
        exploredSet.add(...)

    """

    "*** YOUR CODE HERE ***"
    frontier = util.Stack()
    frontier.push([problem.getStartState(),[]])
    exploredSet = set()
    
    while not frontier.isEmpty():
        state, actions = frontier.pop()
        if (problem.isGoalState(state)):
            return actions
        if not (state in exploredSet):
            exploredSet.add(state)
            for nextState, newAction, cost in problem.getSuccessors(state):
                frontier.push([nextState, actions+[newAction]])

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first.

    Data structures to be used for breadth first graph search
    frontier = util.Queue()
    exploredSet = set()

    """

    "*** YOUR CODE HERE ***"
    frontier = util.Queue()
    frontier.push([problem.getStartState(),[]])
    exploredSet = set()
    
    while not frontier.isEmpty():
        state, actions = frontier.pop()
        if (problem.isGoalState(state)):
            return actions
        if not (state in exploredSet):
            exploredSet.add(state)
            for nextState, newAction, cost in problem.getSuccessors(state):
                frontier.push([nextState, actions+[newAction]])

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first.

    Data structures to be used for uniform coast graph search
    frontier = util.PriorityQueue()
    exploredSet = set()

    """
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()
    frontier.push([problem.getStartState(),[],0],0)
    exploredSet = set()
    
    while not frontier.isEmpty():
        state, actions, stepCost = frontier.pop()
        if (problem.isGoalState(state)):
            return actions
        if not (state in exploredSet):
            exploredSet.add(state)
            for nextState, newAction, cost in problem.getSuccessors(state):
                frontier.push([nextState, actions+[newAction],cost], problem.getCostOfActions(actions+[newAction]))
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    print heuristic(problem.getStartState(),problem)
    frontier = util.PriorityQueue()
    frontier.push([problem.getStartState(),[],0],0+heuristic(problem.getStartState(),problem))
    exploredSet = set()
    
    while not frontier.isEmpty():
        state, actions, stepCost = frontier.pop()
        if (problem.isGoalState(state)):
            return actions
        if not (state in exploredSet):
            exploredSet.add(state)
            for nextState, newAction, cost in problem.getSuccessors(state):
                frontier.push([nextState, actions+[newAction],cost], problem.getCostOfActions(actions+[newAction])+heuristic(nextState,problem))
                
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
