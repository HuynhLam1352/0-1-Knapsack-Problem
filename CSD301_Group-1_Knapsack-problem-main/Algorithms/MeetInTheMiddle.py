from math import log2
from typing import List
import bisect

MAX_RECURSION = 1e7

class MeetInTheMiddle:
    
    @staticmethod
    def __calcSubArray(n: int, c: int) -> List[List[int]]:
        '''
        Return all possible subsets of an array
        '''
        x = []
        for i in range(2 ** n):
            s = []
            for j in range(n):
                if i & 2 ** j:
                    s.append(j + c)
            x.append(s)
        return x

    @staticmethod
    def findSolution(C : int, W : List[int], P : List[int]) -> int:
        '''
        Find a solution of knapsack problem using Meet-in-the-middle algorithms

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

        if (2**(n // 2) > MAX_RECURSION):
            raise Exception('The number of items must be less than {}!'.format(int(2 * log2(MAX_RECURSION))))

        # Compute all subset of first and second
        X = MeetInTheMiddle.__calcSubArray(n // 2, 0)
        Y = MeetInTheMiddle.__calcSubArray(n - n // 2, n // 2)
        size_X = len(X)
        size_Y = len(Y)

        # Only sort the second part
        Y.sort(key = lambda y : sum(W[x] for x in y))

        # Calculate all sum of weights and profits 
        Y_W = [sum(W[x] for x in y) for y in Y]
        X_W = [sum(W[x] for x in y) for y in X]
        Y_P = [sum(P[x] for x in y) for y in Y]
        X_P = [sum(P[x] for x in y) for y in X]

        # Save subset make maximum profit items
        maxP = 0
        maxX = []

        # Traverse all elements of X and do Binary Search for a pair in Y with maximum sum less than S.
        for i in range(size_X):

            if (X_W[i] <= C):

                # Lower_bound() returns the first address which has value greater than or equal to C - X_W[i].
                p = bisect.bisect_left(Y_W, C - X_W[i])

                # If C - X_W[i] was not in array Y then decrease p by 1
                if (p == size_Y or (p < size_Y and Y_W[p] != (C - X_W[i]))):
                    p -= 1
 
                if (X_P[i] + Y_P[p] > maxP):
                    maxX = Y[p] + X[i]
                    maxP = Y_P[p] + X_P[i]
        return maxX