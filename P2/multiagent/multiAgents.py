# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

import pdb

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        'pdb.set_trace()'
        '''print "new successorGameState : ",successorGameState
        print "new Pos : ",newPos
        print "new newFood : ",newFood
        print "new newGhostStates : ",newGhostStates
        print "new newScaredTimes : ",newScaredTimes
        print "ghost Pos :",successorGameState.getGhostPositions()'''

        score=0
        minDF = float("infinity")
        FoodList=newFood.asList()
        for food in FoodList:
            if newFood[food[0]][food[1]]==True:
                if minDF>abs(newPos[0]-food[0])+abs(newPos[1]-food[1]):
                    minDF=abs(newPos[0]-food[0])+abs(newPos[1]-food[1])
        if minDF == float("infinity"):
            score=float("infinity")
        else:
            score-=minDF*5
            
        CuFood=currentGameState.getNumFood()
        SuFood=successorGameState.getNumFood()
        if SuFood<CuFood:
            score+=100
        if len(currentGameState.getCapsules()) > len(successorGameState.getCapsules()):
            score+=130

        DG=0
        for ghostState in newGhostStates:
            if ghostState.scaredTimer==0:
                gPos=ghostState.getPosition()
                DG=abs(newPos[0]-gPos[0])+abs(newPos[1]-gPos[1])
                if DG==3:
                    score-=100
                elif DG==2:
                    score-=125
                elif DG==1:
                    score-=150
                else:
                    score+=DG       
        successorGameState.data.score=score     
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    
    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        return self.pacmanMax(gameState,1)
        util.raiseNotDefined()

    def pacmanMax(self,gameState,depth):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        maxV=float("-infinity")
        for a in gameState.getLegalActions(0):
            v=self.ghostMin(gameState.generateSuccessor(0, a), depth, 1)
            if maxV<v:
                maxV=v
                maxA=a
        if depth==1:
            'print "maxV is:",maxV'
            return maxA
        else:
            return maxV
            
    def ghostMin(self,gameState,depth,gIndex):
        if gameState.isWin() or gameState.isLose():
              return self.evaluationFunction(gameState)
        nextAgent=(gIndex+1)%gameState.getNumAgents()
        minV = float("infinity")
        v=minV
        for a in gameState.getLegalActions(gIndex):
            if nextAgent>0:
                v=self.ghostMin(gameState.generateSuccessor(gIndex, a), depth, nextAgent)
            else:
                if depth==self.depth:
                    v=self.evaluationFunction(gameState.generateSuccessor(gIndex, a))
                else:
                     v=self.pacmanMax(gameState.generateSuccessor(gIndex, a), depth + 1)
            if v<minV:
                minV=v
        return minV

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        al=float("-infinity")
        be=float("infinity")
        return self.pacmanMax(gameState,1,al,be)
        util.raiseNotDefined()

    def pacmanMax(self,gameState,depth,al,be):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        maxV=float("-infinity")
        for a in gameState.getLegalActions(0):
            v=self.ghostMin(gameState.generateSuccessor(0, a), depth, 1,al,be)
            if maxV<v:
                maxV=v
                maxA=a
            if v>be:
                return v
            al=max(al,v)  
        if depth==1:
            'print "maxV is:",maxV'
            return maxA
        else:
            return maxV
            
    def ghostMin(self,gameState,depth,gIndex,al,be):
        if gameState.isWin() or gameState.isLose():
              return self.evaluationFunction(gameState)
        nextAgent=(gIndex+1)%gameState.getNumAgents()
        minV = float("infinity")
        v=minV
        for a in gameState.getLegalActions(gIndex):
            if nextAgent>0:
                v=self.ghostMin(gameState.generateSuccessor(gIndex,a),depth,nextAgent,al,be)
            else:
                if depth==self.depth:
                    v=self.evaluationFunction(gameState.generateSuccessor(gIndex,a))
                else:
                     v=self.pacmanMax(gameState.generateSuccessor(gIndex,a),depth+1,al,be)
            if v<minV:
                minV=v
            if v<al:
                return v
            be=min(be,v)
        return minV

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.pacmanMax(gameState,1)
        util.raiseNotDefined()

    def pacmanMax(self,gameState,depth):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        maxV=float("-infinity")
        for a in gameState.getLegalActions(0):
            v=self.ghostAvg(gameState.generateSuccessor(0, a), depth, 1)
            if maxV<v:
                maxV=v
                maxA=a
        if depth==1:
            'print "maxV is:",maxV'
            return maxA
        else:
            return maxV
            
    def ghostAvg(self,gameState,depth,gIndex):
        if gameState.isWin() or gameState.isLose():
              return self.evaluationFunction(gameState)
        nextAgent=(gIndex+1)%gameState.getNumAgents()
        sumV=0.0
        avg=0.0
        v=0.0
        actions=gameState.getLegalActions(gIndex)
        if nextAgent>0:
            for a in actions:
                sumV+=self.ghostAvg(gameState.generateSuccessor(gIndex, a), depth, nextAgent)
        else:
            if depth==self.depth:
                for a in actions:
                    sumV+=self.evaluationFunction(gameState.generateSuccessor(gIndex, a))
            else:
                for a in actions:
                    sumV+=self.pacmanMax(gameState.generateSuccessor(gIndex, a), depth + 1)
        num=len(actions)
        v=sumV/float(num)
        return v

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
      Adjust the evaluation base on
      the distance to cloest food,
      the distance to all the food,
      the remaining number of food,
      the remaining time of the ghost being scared,
      the distance to the ghost,
    """
    "*** YOUR CODE HERE ***" 
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()

    score=0
    'closest food'
    minDF = float("infinity")
    FoodList=newFood.asList()
    for food in FoodList:
        if newFood[food[0]][food[1]]==True:
            if minDF>util.manhattanDistance(food,newPos):
                minDF=util.manhattanDistance(food,newPos)
    if minDF == float("infinity"):
        score=float("infinity")
    else:
        score-=minDF*10

    'all food'
    sumDF=0
    for food in FoodList:
        if newFood[food[0]][food[1]]==True:
            sumDF+=util.manhattanDistance(food,newPos)
    numOfFood=len(FoodList)
    if numOfFood>0:
        score -= sumDF*3/float(numOfFood)
    else:
        score-=sumDF

    'eating food'
    CuFood=currentGameState.getNumFood()
    score-=CuFood*35
    
    'ghost'
    DG=0
    scoreG=0
    GhostStates = currentGameState.getGhostStates()
    ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
    
    for ghostState in GhostStates:
        score+=ghostState.scaredTimer*3
        
        gPos=ghostState.getPosition()
        DG=util.manhattanDistance(gPos,newPos)
        if ghostState.scaredTimer==0:
            if DG==3:
                score-=200
            elif DG==2:
                score-=300
            elif DG==1:
                score-=450
            else:
                score+=DG  
             
    currentGameState.data.score=score     
    return currentGameState.getScore()
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

