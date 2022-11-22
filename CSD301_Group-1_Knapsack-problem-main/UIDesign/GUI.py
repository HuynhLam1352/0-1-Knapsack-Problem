import sys
import os

from UIDesign.random_dialog import Ui_dgRandom

from random import random
from time import time
from UIDesign.Utility import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
import Algorithms.Algorithm as algorithms
from DataPreprocessing.DataPreprocessing import Preprocessing


class GUI(Ui_mainwindow):
    '''
    GUI
    ----------

    GUI with actions and triggers
    '''
    
    def __init__(self) -> None:
        '''
        Init and setup window
        '''
        super().__init__()
        # Main window
        self.mainwindow = QtWidgets.QMainWindow()
        self.setupUi(self.mainwindow)

        # Random dialog
        self.dgRandom = QtWidgets.QDialog(self.mainwindow)
        self.ui_dgRandom = Ui_dgRandom()
        self.ui_dgRandom.setupUi(self.dgRandom)
        self.dgRandom.setWindowFlag(QtCore.Qt.Popup, True)

        self.setupSignal()

    def setupSignal(self) -> None:
        '''
        Add event to buttons and menu items
        '''
        # Buttons
        self.btn_solve.clicked.connect(self.btn_solve_clicked)
        self.btn_addInput.clicked.connect(self.btn_addInput_clicked)
        self.btn_deleteInput.clicked.connect(self.btn_deleteInput_clicked)
        self.btn_exportInput.clicked.connect(self.btn_exportInput_clicked)
        self.btn_exportOutput.clicked.connect(self.btn_exportOutput_clicked)
        self.btn_randomInput.clicked.connect(self.btn_randomInput_clicked)

        # Actions in Menu File
        self.actionImportDataToExist.triggered.connect(
            self.actionImportDataToExist_triggered)
        self.actionImportDataToNew.triggered.connect(
            self.actionImportDataToNew_triggered)
        self.actionExportInput.triggered.connect(
            self.btn_exportInput_clicked)
        self.actionExportOutput.triggered.connect(
            self.btn_exportOutput_clicked)
        self.actionExit.triggered.connect(self.actionExit_triggered)

        # Actions in Menu Edit
        self.actionAddInput.triggered.connect(self.btn_addInput_clicked)
        self.actionDeleteSelectedInput.triggered.connect(
            self.btn_deleteInput_clicked)
        self.actionSolve.triggered.connect(self.btn_solve_clicked)
        self.actionChangeMaximumWeight.triggered.connect(
            self.actionChangeMaximumWeight_triggered)
        self.actionChangeAlgorithm.triggered.connect(
            self.actionChangeAlgorithm_triggered)
        self.actionRandom.triggered.connect(self.btn_randomInput_clicked)

    def show(self) -> None:
        '''
        Show the main window
        '''
        self.mainwindow.show()

    '''
    ---- When buttons click ----
    '''

    def btn_solve_clicked(self, checked) -> None:
        '''
        Solve Knapsack Problem with the given algorithm and show output to table
        '''

        algorithm = None
        try:
            data = exportInputToJson(self)
            C = data["maximum weight"]
            W = data["table"]["Weight"]
            P = data["table"]["Price"]
            indexes = []
        except:
            showMessageBox("Error", QMessageBox.critical,
                                "Error when read input!")
            return
        try:
            match self.cbb_algorithm.currentText():
                case "Dynamic Programing":
                    algorithm = algorithms.DynamicPrograming
                case "Greedy":
                    algorithm = algorithms.GreedyProgram
                case "Branch and Bound":
                    algorithm = algorithms.BranchAndBound
                case "Brute Force":
                    algorithm = algorithms.BruteForce
                case "Brute Force with Memorization":
                    algorithm = algorithms.BruteForceMemorization
                case "Meet-in-the-middle":
                    algorithm = algorithms.MeetInTheMiddle
                case _:
                    raise Exception("Can not find the algorithm!")

            t1 = time()
            match self.cbb_preprocessing.currentText():
                case "Remove large weight items":
                    (W, P) = Preprocessing.removeLargeWeight(C, W, P)
                case "Remove low price items":
                    (W, P) = Preprocessing.removeSmallPrice(C, W, P)
                case "Remove range of low price items":
                    (W, P) = Preprocessing.removeSmallRangePrice(C, W, P)
                case _:
                    pass
            
            # Display new number of items
            self.lb_newSize.setText("New size: {}".format(len(W)))

            indexes = algorithm.findSolution(C, W, P)
            t2 = time()

            addDataToOutputTable(self, {
                "table": {
                    "Weight": [W[x] for x in indexes],
                    "Price": [P[x] for x in indexes],
                }
            })
            
            self.lb_time.setText("Time: {} s".format(t2 - t1))
            self.lb_status.setText("Status: completed!")
            showMessageBox("Information", QMessageBox.information, "Solved problem successfully!")

        except Exception as e:
            self.lb_status.setText("Status: error!")
            showMessageBox("Error", QMessageBox.critical, str(e))

            
    def btn_addInput_clicked(self, checked) -> None:
        '''
        Add new row to input table and focus last row
        '''
        self.tb_input.insertRow(self.tb_input.rowCount())
        self.tb_input.clearSelection()
        self.tb_input.selectRow(self.tb_input.rowCount()-1)
        self.tb_input.setFocus()

    def btn_deleteInput_clicked(self, checked) -> None:
        '''
        Delete selected rows in input table in descent order
        '''
        rows = list(set([index.row()
                    for index in self.tb_input.selectedIndexes()]))
        rows.reverse()
        for index in rows:
            self.tb_input.removeRow(index)

    def btn_exportInput_clicked(self, checked) -> None:
        '''
        Convert input data to JSON then save to file
        '''
        fileName = saveFileDialog()
        if fileName:
            try:
                jsonData = exportInputToJson(self)
                saveData(fileName, jsonData)
                showMessageBox( 
                    message="Export input data successfully!", boxType=QMessageBox.information)
            except:
                showMessageBox( 
                    message="Error when export input data!", boxType=QMessageBox.critical)

    def btn_exportOutput_clicked(self, checked) -> None:
        '''
        Convert input data to JSON then save to file
        '''
        fileName = saveFileDialog()
        if fileName:
            try:
                jsonData = exportOutputToJson(self)
                saveData(fileName, jsonData)
                showMessageBox( 
                    message="Export output data successfully!", boxType=QMessageBox.information)
            except:
                showMessageBox( 
                    message="Error when export output data!", boxType=QMessageBox.critical)

    def btn_randomInput_clicked(self, checked) -> None:
        '''
        Open new input popup for maximum weight, maximum price and count for random new inputs
        '''


        if self.dgRandom.exec_():
            max_weights = self.ui_dgRandom.spb_maximumWeight.value()
            max_prices = self.ui_dgRandom.spb_maximumPrice.value()
            is_reset = self.ui_dgRandom.cb_clearExisted.isChecked()
            is_weight_only = self.ui_dgRandom.cb_weightOnly.isChecked()
            count = self.ui_dgRandom.spb_count.value()
            weights = [int(random() * max_weights + 1) for i in range(count)]
            if not is_weight_only:
                price = [int(random() * max_prices + 1) for i in range(count)]
            else:
                price = weights.copy()
            if is_reset:
                self.tb_input.setRowCount(0)
            
            addDataToInputTable(self, {
                "table": {
                    "Weight": weights,
                    "Price": price,
                }
            })

    '''
    ---- Actions in File Menu ----
    '''

    def actionExit_triggered(self, checked) -> None:
        '''
        Close window
        '''
        if showConfirmBox(message="Do you sure to exit?") == QMessageBox.Yes:  # type: ignore
            self.mainwindow.close()

    def actionImportDataToExist_triggered(self, checked) -> None:
        '''
        Read and import data to input table
        '''
        fileName = openFileNameDialog()
        if fileName:
            try:
                data = readData(fileName)
                addDataToInputTable(self, data)
            except:
                showMessageBox( 
                    message="Error when import data!", boxType=QMessageBox.critical)

    def actionImportDataToNew_triggered(self, checked) -> None:
        '''
        Read data, then clear table and import data to input table
        '''
        fileName = openFileNameDialog()
        if fileName:
            try:
                self.tb_input.setRowCount(0)
                data = readData(fileName)
                addDataToInputTable(self, data)
            except:
                showMessageBox( 
                    message="Error when import data!", boxType=QMessageBox.critical)

    '''
    ---- Actions in Edit Menu ----
    '''

    def actionChangeMaximumWeight_triggered(self, checked) -> None:
        '''
        Focus to SpinBox Maximum Weight
        '''
        self.spb_maximumWeight.setFocus()

    def actionChangeAlgorithm_triggered(self, checked) -> None:
        '''
        Show combobox Algorithm and focus it
        '''
        self.cbb_algorithm.showPopup()
        self.cbb_algorithm.setFocus()