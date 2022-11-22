
from typing import List

MAX_COMPLEXITY = 1e9

class DynamicPrograming:
    @staticmethod
    def findSolution(C : int, W : List[int], P : List[int]) -> List[int]:
        '''
        Find a solution of knapsack problem using Dynamic Programing algorithms

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

        if n * C > MAX_COMPLEXITY:
            raise Exception('N x C must be less than {}'.format(MAX_COMPLEXITY))

        K = [[0 for x in range(C + 1)] for x in range(n + 1)]
 
        # Build table K[][] in bottom up manner
        for i in range(n + 1):
            for w in range(C + 1):
                if i == 0 or w == 0:
                    K[i][w] = 0
                elif W[i-1] <= w:
                    K[i][w] = max(P[i-1]
                            + K[i-1][w-W[i-1]], 
                                K[i-1][w])
                else:
                    K[i][w] = K[i-1][w]

        # Find items to give optimal result
        i = n
        w = C
        result = []
        while i > 0:
            if K[i][w] != K[i - 1][w]:
                result.append(i - 1)
                w -= W[i - 1]
                i -= 1
            else:
                i -= 1
        return result