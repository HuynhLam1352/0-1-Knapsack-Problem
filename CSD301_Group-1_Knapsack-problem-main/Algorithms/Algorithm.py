import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from Algorithms.BranchAndBound import BranchAndBound
from Algorithms.BruteForce import BruteForce
from Algorithms.BruteForceMemorization import BruteForceMemorization
from Algorithms.MeetInTheMiddle import MeetInTheMiddle
from Algorithms.DynamicPrograming import DynamicPrograming
from Algorithms.Greedy import GreedyProgram

# Define some algorithm classes
DynamicPrograming = DynamicPrograming
GreedyProgram = GreedyProgram
BranchAndBound = BranchAndBound
BruteForceMemorization = BruteForceMemorization
BruteForce = BruteForce
MeetInTheMiddle = MeetInTheMiddle