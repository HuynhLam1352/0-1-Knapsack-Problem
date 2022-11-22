import queue
from time import time
from typing import List

MAX_NODES = 1e7

class Node:
    def __init__(self, level : int, profit : float, weight : int, index : int, parent) -> None:
        self.level = level # The level within the tree (depth)
        self.profit = profit # The total profit
        self.weight = weight # The total weight
        self.parent = parent # The previous node
        self.index = index # Index of weight and profit

class BranchAndBound:

    @staticmethod
    def getBound(u : Node, numItems : int, knapsackSize : int, weight : List[int], profit : List[int], indexes : List[int]) -> float:
        '''
        Return upper bound of given weight and profit
        '''
        if u.weight >= knapsackSize: return 0
        else:
            upperBound = u.profit
            totalWeight = u.weight
            j = u.level + 1
            while j < numItems and totalWeight + weight[indexes[j]] <= knapsackSize:
                upperBound += profit[indexes[j]]
                totalWeight += weight[indexes[j]]
                j += 1

            if j < numItems:
                upperBound += ((knapsackSize - totalWeight) * (profit[indexes[j]]/weight[indexes[j]]))
            return upperBound 

    @staticmethod
    def findSolution(C : int, W : List[int], P : List[int]) -> List[int]:
        '''
        Find a solution of knapsack problem using Branch and Bound algorithms

        @Parameters:
        ----------
            - C : weight of knapsack
            - W : list weight of items
            - P : list price of items

        @Return
        ----------
        List indexes of selected items
        '''

        # Number of items
        n = len(W)
        indexes = [x for x in range(n)]
        indexes.sort(key = lambda i : P[i]/W[i], reverse=True)
        
        q = queue.Queue()
        root = Node(-1, 0, 0, -1, None)    
        q.put(root)

        maxProfit = 0
        maxU : Node | None = None
        bound = 0
        countNode = 0
        while not q.empty():
            countNode += 1
            if countNode > MAX_NODES:
                raise Exception('Maximum nodes of queue!')
                
            v : Node = q.get() # Get the next item on the queue
            uLevel = v.level + 1
            u = Node(uLevel, v.profit + P[indexes[uLevel]], v.weight + W[indexes[uLevel]], uLevel, v)
            bound = BranchAndBound.getBound(u, n, C, W, P, indexes)

            if u.weight <= C and u.profit > maxProfit:
                maxProfit = u.profit
                maxU = u
                
            if bound > maxProfit:
                q.put(u)

            u = Node(uLevel, v.profit, v.weight, v.index, v.parent)
            bound = BranchAndBound.getBound(u, n, C, W, P, indexes)

            if bound > maxProfit:
                q.put(u)

        # Find items to give optimal result
        curNode = maxU
        result = []
        while curNode and curNode.index != -1:
            result.append(indexes[curNode.index])
            curNode = curNode.parent
        return result
