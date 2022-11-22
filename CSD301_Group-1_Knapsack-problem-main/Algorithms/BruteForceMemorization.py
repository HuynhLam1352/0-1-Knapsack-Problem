from typing import List
import sys

# Maximum count of recursion call
MAX_RECURSION = 1e7

class BruteForceMemorization:
    __maxRecursion = MAX_RECURSION
    __KP = {}

    @staticmethod
    def findSolution(C : int, W : List[int], P : List[int]) -> List[int]:
        '''
        Find a solution of knapsack problem using Brute Force with Memorization algorithms

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
        BruteForceMemorization.__maxRecursion = MAX_RECURSION
        BruteForceMemorization.__KP = {}
        sys.setrecursionlimit(1500)
        result = BruteForceMemorization.__knapSack(C, W, P, n)
        return result[1]

    @staticmethod
    def __knapSack(mW: int, w : List[int], v : List[int], n : int) -> List[int | List[int]]:
        '''
        Recursive function for solving knapsack problem
        '''
        BruteForceMemorization.__maxRecursion -= 1
        if (BruteForceMemorization.__maxRecursion < 0):
            raise Exception('Max recursion error!')

        if (mW == 0 or n == 0):
            BruteForceMemorization.__KP[(mW, n)] = [0, []]
            return [0, []]

        if (w[n-1] > mW):
            return BruteForceMemorization.__knapSack(mW, w, v, n-1)

        if BruteForceMemorization.__KP.get((mW, n), None) != None:
            set_ = BruteForceMemorization.__KP[(mW, n)]
            return [set_[0], set_[1].copy()]

        set1 = BruteForceMemorization.__knapSack(mW-w[n-1], w, v, n-1)
        set2 = BruteForceMemorization.__knapSack(mW, w, v, n-1)

        if (set1[0]+v[n-1] > set2[0]):
            set1[1].append(n-1)
            set1[0] += v[n-1]
            BruteForceMemorization.__KP[(mW, n)] = [set1[0], set1[1].copy()]
            return set1
        else:
            BruteForceMemorization.__KP[(mW, n)] = [set2[0], set2[1].copy()]
            return set2