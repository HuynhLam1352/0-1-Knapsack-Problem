from typing import List

MAX_ITEMS = 1e3

class GreedyProgram:
    @staticmethod
    def findSolution(C : int, W : List[int], P : List[int]) -> List[int]:
        '''
        Find a solution of knapsack problem using Greedy algorithms

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

        if n > MAX_ITEMS:
            raise('Maximum count of items are {}'.format(MAX_ITEMS))

        indexes = [x for x in range(n)]
        indexes.sort(key = lambda i : P[i]/W[i], reverse=True)

        usedCapacity = 0
        totalValue = 0
        result = []
        for i in range(0, n):
            if usedCapacity + W[indexes[i]] <= C:
                usedCapacity += W[indexes[i]]
                totalValue += P[indexes[i]]
                result.append(indexes[i])

        return result

