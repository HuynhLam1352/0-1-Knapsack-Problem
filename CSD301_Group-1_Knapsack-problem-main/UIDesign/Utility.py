
'''
---- Utilities functions ----
'''

import json
from typing import Callable
from UIDesign.UI_mainwindow import Ui_mainwindow
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QWidget, QTableWidgetItem, QMessageBox


def getColumnIndex(UIWindow : Ui_mainwindow) -> dict:
    '''
    Get column index from column name of table
    '''
    result = dict()
    for i in range(UIWindow.tb_input.columnCount()):
        result[UIWindow.tb_input.horizontalHeaderItem(i).text()] = i
    return result

def openFileNameDialog() -> str:
    '''
    Show open file dialog and return full path of selected file
    '''
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog  # type: ignore
    fileName, _ = QFileDialog.getOpenFileName(modalWidget(), "Import Data", "", "JSON Files (*.json);;Input Files (*.inp);;All Files (*)", options=options)
    return fileName

def saveFileDialog()  -> str:
    '''
    Show save file dialog and return full path of saved file
    '''
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog  # type: ignore
    fileName, _ = QFileDialog.getSaveFileName(modalWidget(), "Export Data", "", "JSON Files (*.json);;Input Files (*.inp);;All Files (*)", options=options)
    return fileName

def readData(fileName: str) -> dict:
    '''
    Read JSON data from given file name
    '''
    import json
    with open(fileName, "r") as f:
        data: dict = json.load(f)

    if data:
        return data
    return dict()

def saveData(fileName: str, jsonData: dict) -> None:
    '''
    Save data to file with given file name and JSON data
    '''
    with open(fileName, 'w') as f:
        json.dump(jsonData, f)

def exportInputToJson(UIWindow : Ui_mainwindow)  -> dict:
    '''
    Convert data from combobox algorithm, spinbox maximum weight and input table to JSON string
    '''
    columns = getColumnIndex(UIWindow)
    jsonData = dict()
    jsonData["algorithm"] = UIWindow.cbb_algorithm.currentText()
    jsonData["maximum weight"] = UIWindow.spb_maximumWeight.value()
    for key in columns:
        columns[key] = [int(UIWindow.tb_input.item(i, columns[key]).text())
                        for i in range(UIWindow.tb_input.rowCount())]
    jsonData["table"] = columns
    return jsonData

def exportOutputToJson(UIWindow : Ui_mainwindow)  -> dict:
    '''
    Convert data from combobox algorithm, spinbox maximum weight and input table to JSON string
    '''
    jsonData = dict()
    jsonData["algorithm"] = UIWindow.cbb_algorithm.currentText()
    jsonData["maximum weight"] = UIWindow.spb_maximumWeight.value()
    
    columns = getColumnIndex(UIWindow)
    for key in columns:
        columns[key] = [int(UIWindow.tb_input.item(i, columns[key]).text())
                        for i in range(UIWindow.tb_input.rowCount())]
    jsonData["input"] = columns.copy()

    columns = getColumnIndex(UIWindow)
    for key in columns:
        columns[key] = [int(UIWindow.tb_output.item(i, columns[key]).text())
                        for i in range(UIWindow.tb_output.rowCount() - 1)]
    jsonData["output"] = columns.copy()
    return jsonData

def addDataToInputTable(UIWindow : Ui_mainwindow, jsonData: dict) -> None:
    '''
    Add data to combobox algorithm, spinbox maximum weight and input table
    '''
    # Set algorithm
    algorithm = jsonData.get("algorithm", UIWindow.cbb_algorithm.currentText())
    UIWindow.cbb_algorithm.setCurrentText(algorithm)

    # Set maximum weight
    maxWeight = jsonData.get(
        "maximum weight", UIWindow.spb_maximumWeight.value())
    UIWindow.spb_maximumWeight.setValue(maxWeight)
    
    # Add data to table
    table: dict = jsonData.get("table", {})
    weights: list = table.get("Weight", [])
    values: list = table.get("Price", [])
    
    columns: dict = getColumnIndex(UIWindow)
    tableRow = UIWindow.tb_input.rowCount()
    UIWindow.tb_input.setRowCount(
        tableRow + len(weights))
    for i in range(len(weights)):
        UIWindow.tb_input.setItem(
            tableRow + i, columns["Weight"], QtWidgets.QTableWidgetItem(str(weights[i])))
    for i in range(len(values)):
        UIWindow.tb_input.setItem(
            tableRow + i, columns["Price"], QtWidgets.QTableWidgetItem(str(values[i])))

def addDataToOutputTable(UIWindow : Ui_mainwindow, jsonData: dict) -> None:
    '''
    Add data to output table
    '''
    table: dict = jsonData.get("table", {})
    weights: list = table.get("Weight", [])
    values: list = table.get("Price", [])
    columns: dict = getColumnIndex(UIWindow)

    UIWindow.tb_output.setRowCount(
        max(len(weights), len(values)) + 1)
    for i in range(len(weights)):
        UIWindow.tb_output.setItem(
            i, columns["Weight"], QtWidgets.QTableWidgetItem(str(weights[i])))
    for i in range(len(values)):
        UIWindow.tb_output.setItem(
            i, columns["Price"], QtWidgets.QTableWidgetItem(str(values[i])))

    UIWindow.tb_output.setVerticalHeaderLabels(
        [str(x + 1) for x in range(UIWindow.tb_output.rowCount())])
    UIWindow.tb_output.setVerticalHeaderItem(
        UIWindow.tb_output.rowCount() - 1, QtWidgets.QTableWidgetItem("Total"))
    UIWindow.tb_output.setItem(UIWindow.tb_output.rowCount(
    ) - 1, columns["Weight"], QtWidgets.QTableWidgetItem(str(sum(weights))))
    UIWindow.tb_output.setItem(UIWindow.tb_output.rowCount(
    ) - 1, columns["Price"], QtWidgets.QTableWidgetItem(str(sum(values))))
    

def modalWidget(x : int = 960, y : int = 540, width: int = 400, height: int = 100) -> QWidget:
    '''
    Create dialog or message Widget
    '''
    wget = QWidget()
    wget.setFixedSize(width, height)
    wget.move(x - width // 2, y - height // 2)
    return wget

def showMessageBox(title: str = "Notification", boxType: Callable = QMessageBox.information, message: str = "") -> None:
    '''
    Show messagebox that only display message and OK button
    '''
    boxType(modalWidget(), title, message, QMessageBox.Ok)  # type: ignore

def showConfirmBox(title: str = "Confirm", message: str = "") -> QMessageBox.StandardButton:
    '''
    Show confirm box that return Yes or No
    '''
    reply = QMessageBox.question(modalWidget(), title, message, QMessageBox.No | QMessageBox.Yes)  # type: ignore
    return reply