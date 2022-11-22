from typing import *
import math

class Preprocessing:
    '''
    Preprocessing
    ---------------

    Preprocessing for reducing size of the Knapsack problem
    '''
    @staticmethod
    def removeLargeWeight(C : int, W : List[int], P : List[int]) -> Tuple[List[int]]:
        '''
        Remove all items that its weight greater than the capacity of knapsack

        Return
        --------
        A tuple contain weight and price of rest items
        '''
        n = len(W)

        W_, P_ = list(), list()

        for i in range(n):
            if W[i] <= C:
                P_.append(P[i])
                W_.append(W[i])
        return (W_, P_)

    
    @staticmethod
    def removeSmallPrice(C : int, W : List[int], P : List[int]) -> Tuple[List[int]]:
        '''
        With each type of items W[i], select at most floor(C / W[i]) items have maximum price and remove others. 

        Return
        --------
        A tuple contain weight and price of selected items
        '''
        n = len(W)

        maxP = max(P) + 1
        indexes = [x for x in range(n)]
        indexes.sort(key= lambda x: W[x] - P[x] / maxP + 1)

        lastW = -1
        count = 0
        maxCount = 0
        W_, P_ = list(), list()

        for i in range(n):
            if lastW != W[indexes[i]]:
                lastW = W[indexes[i]]
                maxCount = math.floor(C / W[indexes[i]])
                count = 0
            if count < maxCount:
                count += 1
                P_.append(P[indexes[i]])
                W_.append(W[indexes[i]])

        return (W_, P_)
        
    @staticmethod
    def removeSmallRangePrice(C : int, W : List[int], P : List[int]) -> Tuple[List[int]]:
        '''
        With each type of items W[i] or W[j]: floor(C / W[i]) == floor(C / W[j]), select at most floor(C / W[i]) items have maximum price and remove others. 

        Return
        --------
        A tuple contain weight and price of selected items
        '''
        n = len(W)

        maxP = max(P) + 1
        indexes = [x for x in range(n)]
        indexes.sort(key= lambda x: W[x] - P[x] / maxP + 1)

        count = 0
        maxCount = 0
        W_, P_ = list(), list()

        for i in range(n):
            if math.floor(C / W[indexes[i]]) != maxCount:
                maxCount = math.floor(C / W[indexes[i]])
                count = 0
            if count < maxCount:
                count += 1
                P_.append(P[indexes[i]])
                W_.append(W[indexes[i]])
        return (W_, P_)
