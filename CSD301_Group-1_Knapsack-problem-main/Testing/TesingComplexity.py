from random import randint
from time import time
import sys
import os
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from Algorithms.BranchAndBound import BranchAndBound
from Algorithms.BruteForce import BruteForce
from Algorithms.BruteForceMemorization import BruteForceMemorization
from Algorithms.DynamicPrograming import DynamicPrograming
from Algorithms.Greedy import GreedyProgram
from Algorithms.MeetInTheMiddle import MeetInTheMiddle


ls_C = [10, 100, 1000, 10000, 100000, 1000000]
ls_N = [5, 10, 20, 40, 100, 500, 1000]

def generateRandomInput(C, N):
    W = [randint(1, 2 * C // 5) for x in range(N)]
    P = [randint(1, C) for x in range(N)]
    return (C, W, P)

def calcTime(algorithm, C, W, P) -> float | str:
    '''
    Calculate execution time of an algorithm
    '''
    try:
        t1 = time()
        algorithm.findSolution(C, W, P)
        t2 = time()
        return (t2 - t1) * 1000
    except:
        return 'NaN'

algorithm_names = ['Brute Force', 'Meet in the middle', 'Brute Force with Memorization', 'Greedy', 'Branch and Bound', 'Dynamic Programing']
algorithms = [BruteForce, MeetInTheMiddle, BruteForceMemorization, GreedyProgram, BranchAndBound, DynamicPrograming]

def test(C, N):
    (C, W, P) = generateRandomInput(C, N)
    return [calcTime(algorithm, C, W, P) for algorithm in algorithms]

N = 20
result = []
for C in ls_C:
    result.append([C] + test(C, N))
df = pd.DataFrame(result, columns=['Maximum weight (with N = {})'.format(N)] + algorithm_names)
df.to_csv('./Testing/Test_N={}.csv'.format(N))

N = 40
result = []
for C in ls_C:
    result.append([C] + test(C, N))
df = pd.DataFrame(result, columns=['Maximum weight (with N = {})'.format(N)] + algorithm_names)
df.to_csv('./Testing/Test_N={}.csv'.format(N))

C = 1000
result = []
for N in ls_N:
    result.append([N] + test(C, N))
df = pd.DataFrame(result, columns=['Number of items (with C = {})'.format(C)] + algorithm_names)
df.to_csv('./Testing/Test_C={}.csv'.format(N))