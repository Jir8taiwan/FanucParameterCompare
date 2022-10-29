# -*- coding: utf-8 -*-
#####################
# Author: https://github.com/Jir8taiwan/
# Version. 2022.10.28
#
# Using PYTHON3 language to open the two converted CSV files at
# FANUC controller system of parameter backup for difference.
# Please prepare two any ".CSV" documents in somewhere.
# It will output CSV and EXCEL files for studying in a formatted
# data about difference line for reference.
#
# ****************************************************************
# If this small code is helping any needed case, it can donate
# to me for encourage as following address:
# 1. BTC - 3M4wWghm4MxmrSfXmHMEeCFNwP8Lxxqjzk
# 2. BCH - bitcoincash:qq6ghvdmyusnse9735rd5q09ensacl8z8qzrlwf49q
# 3. LTC - MR6HaFkfkmsfifX3jWu7xz33dULGotVUWB
# 4. DOGE- DGEFd3AAfJrBuaUwc4P6R2ZT754Jon9fQ7
#
#####################
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFileDialog
import os, sys
import pandas as pd
import csv
import openpyxl
## UI layout flie input
from mainUI import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        # in python3, super(Class, self).xxx = super().xxx
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_control()
        #self.statusBar().showMessage('Message in statusbar.')
        self.repaint()

    def setup_control(self):
        # TODO
        #self.ui.textEdit.setText('Happy World!')
        print("Hello the world!! by JIR greeting.")
        self.ui.File1lineEdit.setText('Please open and select File 1...')
        self.ui.File2lineEdit.setText('Please open and select File 2...')
        self.ui.Msg4textBrowser.setText('Hello the world!! by JIR greeting.')

        self.ui.File1pushButton.clicked.connect(self.open_file1)
        self.ui.File2pushButton.clicked.connect(self.open_file2)

        self.ui.GoCpmarepushButton.clicked.connect(self.checkFiles)
        
        self.ui.OpenResultpushButton.setText('')

    def open_file1(self):
        file1name, filetype = QFileDialog.getOpenFileName(self,
                  "Select file 1",
                  "./", "CSV files (*.csv)")                 # start path
        print(file1name, filetype)
        self.ui.File1lineEdit.setText(file1name)
        file1msg = os.path.basename(file1name)
        self.ui.Msg4textBrowser.setText("FILE1 [ " + file1msg + " ] is set.")

    def open_file2(self):
        file2name, filetype = QFileDialog.getOpenFileName(self,
                  "Select File 2",
                  "./", "CSV files (*.csv)")                 # start path
        print(file2name, filetype)
        self.ui.File2lineEdit.setText(file2name)
        file2msg = os.path.basename(file2name)
        self.ui.Msg4textBrowser.setText("FILE2 [ " + file2msg + " ] is set.")

    def checkFiles(self):

        
        filename1 = self.ui.File1lineEdit.text()
        filename2 = self.ui.File2lineEdit.text()
        resultfile = "diff_result.csv"
        
        msgFile = filename1 + "\n" + filename2
        print(msgFile)        
        self.ui.Msg4textBrowser.setText(msgFile)

        ## check file status        
        if not os.path.exists(filename1) or filename1 == "Please open and select File 1...":
            MsgError1 = "Is FILE1 inputed or both existed together? \n"
            print(MsgError1, "\n")
            self.ui.Msg4textBrowser.setText(MsgError1)
            return
        
        if not os.path.exists(filename2) or filename2 == "Please open and select File 2...":
            MsgError2 = "Is FILE2 inputed or both existed together? \n"
            print(MsgError2, "\n")
            self.ui.Msg4textBrowser.setText(MsgError2)
            return
        
        ## Processing compare function and output
        MsgResult = "Run compare and prepare for result file ... \n"
        print(MsgResult)
        self.ui.Msg4textBrowser.setText(MsgResult)

        df1 = pd.read_csv(filename1, encoding='utf8', dtype=str)
        df2 = pd.read_csv(filename2, encoding='utf8', dtype=str)
        df1['flag'] = '01_' + filename1 
        df2['flag'] = '02_' + filename2
        df = pd.concat([df1, df2])
        #print(df)
        dups_dropped = df.drop_duplicates(df.columns.difference(['flag']), keep=False)
        print(dups_dropped)
        dups_dropped.to_csv(resultfile, index=False)

        ## Save to EXCEL formate
        print("Outputing EXCEL file from CSV data ... \n")
        XLSXoutput = os.path.basename(resultfile).split('.')[0] + ".xlsx"
        print(XLSXoutput)
        open_csvfile = pd.read_csv(resultfile, encoding='utf8', dtype=str)
        open_csvfile.to_excel(XLSXoutput, index=None, header=True)

        ## Finish
        MsgResult = MsgResult + "DONE!! Please read and check :\n" + XLSXoutput
        print(MsgResult)
        self.ui.Msg4textBrowser.setText(MsgResult)
        
        #print(XLSXoutput)
        self.ui.OpenResultpushButton.setText('Open Result')
        self.ui.OpenResultpushButton.clicked.connect(lambda:self.open_resultFile(XLSXoutput))        
        
    ## Open result file
    def open_resultFile(self, EXCELfile):
        import os, sys
        print("open result file", EXCELfile)
        self.ui.Msg4textBrowser.setText("Go opening the file : " + EXCELfile)
        os.startfile(EXCELfile)
        
        

