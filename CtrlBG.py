# -*- coding: utf-8 -*-
#####################
# Author: https://github.com/Jir8taiwan/
# Version. 2022.11.02-1
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
#from pathlib import Path
import pandas as pd
import csv
import openpyxl
from tqdm import tqdm
#import re
from time import sleep

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
        GreetMsg = "Hello the world!! by JIR greeting.\n"
        UsageMsg = "Please select two similar .CSV files to compare difference.\n"
        print(GreetMsg)
        self.ui.File1lineEdit.setText('Please open and select File 1...')
        self.ui.File2lineEdit.setText('Please open and select File 2...')
        self.ui.Msg4textBrowser.setText(GreetMsg + UsageMsg)

        self.ui.File1pushButton.clicked.connect(self.open_file1)
        self.ui.File2pushButton.clicked.connect(self.open_file2)

        self.ui.GoCpmarepushButton.clicked.connect(self.checkFiles)
        
        self.ui.file1CSVpushButton.clicked.connect(self.File1CSV)
        self.ui.file2CSVpushButton.clicked.connect(self.File2CSV)
        
        self.ui.OpenResultpushButton.setText('')

    def open_file1(self):# start path
        file1name, filetype = QFileDialog.getOpenFileName(self,
                  "Select file 1",
                  "./", "CSV and TXT files (*.csv *.txt);;TEXT Files (*.txt);;CSV files (*.csv);;All Files (*)")
        print(file1name, filetype)
        self.ui.File1lineEdit.setText(file1name)
        file1msg = os.path.basename(file1name)
        self.ui.Msg4textBrowser.setText("FILE1 [ " + file1msg + " ] is set.")

    def open_file2(self):# start path
        file2name, filetype = QFileDialog.getOpenFileName(self,
                  "Select File 2",
                  "./", "CSV and TXT files (*.csv *.txt);;TEXT Files (*.txt);;CSV files (*.csv);;All Files (*)")
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

        #DEV confirm
        #print(os.path.basename(filename1).rsplit('.')[1])
        #print(os.path.basename(filename2).rsplit('.')[1])
        print(os.path.splitext(filename1)[1])
        print(os.path.splitext(filename2)[1])

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
            
        ## compare two files are same subname before go
        
        if not os.path.basename(filename1).rsplit('.')[1] == os.path.basename(filename2).rsplit('.')[1]:
            MsgError3 = "Is FILE 1 and FILE2 inputed different formated documents? \n"
            print(MsgError3, "\n")
            self.ui.Msg4textBrowser.setText(MsgError3)
            return
        
        if os.path.splitext(filename1)[1] == ".TXT" and os.path.splitext(filename2)[1] == ".TXT":
            MsgError4 = "Does FILE 1 or FILE2 document not convert to CSV yet? \n"
            print(MsgError4, "\n")
            self.ui.Msg4textBrowser.setText(MsgError4)
            return


        self.processCompare()

    def processCompare(self):   
        filename1 = self.ui.File1lineEdit.text()
        filename2 = self.ui.File2lineEdit.text()
        resultfile = "diff_result.csv"
                
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
        return        
        
    ## Open result file
    def open_resultFile(self, EXCELfile):
        import os, sys
        print("open result file", EXCELfile)
        self.ui.Msg4textBrowser.setText("Go opening the file : " + EXCELfile)
        os.startfile(EXCELfile)
        #sys.exit()
        return
        #pass
        #sys.exit(0)
        
    ## covert to CSV before compare        
    def File1CSV(self):
        TXTinputPATH =  self.ui.File1lineEdit.text() #filename1
        CSVoutputPATH = 'OutputTemp.CSV'
        CSVoutputPATH2 = '01_Output.CSV'
        CSVoutputPATH3 = "01_" + os.path.basename(TXTinputPATH).split('.')[0] + "_trimed.csv"
        XLSXoutputPATH = "01_" + os.path.basename(TXTinputPATH).split('.')[0] + "_trimed.xlsx"
        TEMPouputPATH = 'tempoutput.txt'
        
        if not os.path.exists(TXTinputPATH) or TXTinputPATH == "Please open and select File 1...":
            MsgError1 = "Is FILE1 inputed or existed together? \n"
            print(MsgError1, "\n")
            self.ui.Msg4textBrowser.setText(MsgError1)
            return
        if not os.path.splitext(TXTinputPATH)[1] == ".TXT":
            MsgError4 = "Is FILE 1 .TXT text document collect? \n"
            print(MsgError4, "\n")
            self.ui.Msg4textBrowser.setText(MsgError4)
            return

        ## Go Loop
        with open(TXTinputPATH, 'r') as checkfile:
            linecount = len(checkfile.readlines())
        #print(linecount)
        progress = tqdm(total=linecount)
        checkfile.close()
        
        print("Converting and processing!!")
        txt = ""
        with open(TXTinputPATH, 'r', encoding='UTF-8') as file:
            #while (line := file.readline().rstrip()):
            nonempty = filter(str.rstrip, file)
            for line in nonempty:
                
                if "%" in line.strip():
                    line = ""
                paramNUM = str(line[:6])
                #paramNUM = line.rsplit('Q1L1P', 1)[0]

                ##### for older bck format
                #line = re.sub(r"\s+", ",", line)
                line = line.replace(" ", "")
                if not len(line) == 0:
                    if not line[6:8] == "Q1":
                        #print(line[6:8])
                        line = line[:6] + "Q1" + line[6:]
                

                ##### for newer bck format                
                #line = line.replace("A11P", "\nA11")
                line = line.rsplit('A7', 1)[0]
                line = line.rsplit('S5', 1)[0]
                
                line = line.replace("Q1L1P", ",L1,")
                line = line.replace("L2P", "\n" + paramNUM + ",L2,")
                line = line.replace("L3P", "\n" + paramNUM + ",L3,")
                line = line.replace("L4P", "\n" + paramNUM + ",L4,")

                line = line.replace("Q1A1M", ",A1,")
                line = line.replace("A2M", "\n" + paramNUM + ",A2,")
                line = line.replace("A3M", "\n" + paramNUM + ",A3,")
                line = line.replace("A4M", "\n" + paramNUM + ",A4,")
                line = line.replace("A5M", "\n" + paramNUM + ",A5,")
                line = line.replace("A6M", "\n" + paramNUM + ",A6,")

                line = line.replace("Q1L1M", ",A1,")
                line = line.replace("L2M", "\n" + paramNUM + ",L2,")
                line = line.replace("L3M", "\n" + paramNUM + ",L3,")
                line = line.replace("L4M", "\n" + paramNUM + ",L4,")

                line = line.replace("Q1T1P", ",T1,")
                ine = line.replace("T2P", "\n" + paramNUM + ",T2,")
                line = line.replace("T3P", "\n" + paramNUM + ",T3,")
                line = line.replace("T4P", "\n" + paramNUM + ",T4,")

                line = line.replace("Q1M", ",M,")
                
                line = line.replace("Q1S1P", ",S1,")
                line = line.replace("S2P", "\n" + paramNUM + ",S2,")
                line = line.replace("S3P", "\n" + paramNUM + ",S3,")
                line = line.replace("S4P", "\n" + paramNUM + ",S4,")
                
                line = line.replace("Q1A1P", ",A1,")
                line = line.replace("A2P", "\n" + paramNUM + ",A2,")
                line = line.replace("A3P", "\n" + paramNUM + ",A3,")
                line = line.replace("A4P", "\n" + paramNUM + ",A4,")        
                line = line.replace("A5P", "\n" + paramNUM + ",A5,")
                line = line.replace("A6P", "\n" + paramNUM + ",A6,")
                line = line.replace("A7P", "\n" + paramNUM + ",A7,")
                line = line.replace("A8P", "\n" + paramNUM + ",A8,")
                line = line.replace("A9P", "\n" + paramNUM + ",A9,")
                line = line.replace("A10P", "\n" + paramNUM + ",A10,")
                line = line.replace("A11P", "\n,A11,")
                line = line.rsplit(',A11', 1)[0]

                line = line.replace("Q1P", ",,")
                #print("Formating:", line)
                txt += line + "\n"

        f = open(TEMPouputPATH,'w',encoding='utf-8')
        #txt = txt.strip()
        f.write(txt)
        f.close()

        file.close()        

        ## Output file
        print("Outputing new format CSV file")
        f = open(TEMPouputPATH,'w', encoding='utf-8')
        txt = txt.strip()
        f.write(txt)
        f.close()

        with open(TEMPouputPATH, 'r', encoding='utf8') as in_file:
            stripped = (line.strip() for line in in_file)
            lines = (line.split(",") for line in stripped if line)
            with open(CSVoutputPATH, 'w') as out_file:
                writer = csv.writer(out_file, dialect="excel")
                writer.writerow(['ParamNO', 'AxisName', 'Value'])
                writer.writerows(lines)
                out_file.close()
        with open(CSVoutputPATH, newline='', encoding='utf8') as in_file:
            with open(CSVoutputPATH2, 'w', newline='') as out_file:
                writer = csv.writer(out_file)
                for row in csv.reader(in_file):
                    if row:
                        writer.writerow(row)
                out_file.close()

        ## Make a CSV format file without 0 value of data
        print("Outputing CSV file without 0 value data")
        df = pd.read_csv(CSVoutputPATH2, encoding='utf8', dtype=str)
        if os.path.exists(CSVoutputPATH3):
            os.remove(CSVoutputPATH3)
            
        #new_df = lambda:self.filter_rows_by_values(df, "Value", ["0","00000000", "0.0"])
        new_df = df[~df["Value"].isin(["0","00000000", "0.0"])]
        
        print(new_df)
        new_df.to_csv(CSVoutputPATH3, index=False, encoding='utf8')

        ## Make a EXCEL format file with and without 0 value of data
        #print("Outputing EXCEL file from CSV data")
        #read_file = pd.read_csv(CSVoutputPATH3, encoding='utf8', dtype=str)
        #read_file.to_excel(XLSXoutputPATH, index=None, header=True)
        #read_file = pd.read_csv(CSVoutputPATH2, encoding='utf8', dtype=str)
        #read_file.to_excel(XLSXoutputPATH2, index=None, header=True)
        
        # check temp file and exited is to delete
        if os.path.exists(CSVoutputPATH):
            os.remove(CSVoutputPATH)
        if os.path.exists(CSVoutputPATH2):
            os.remove(CSVoutputPATH2)

        okMsg = "New CSV file is set : " + CSVoutputPATH3
        self.ui.Msg4textBrowser.setText(okMsg)
        self.ui.File1lineEdit.setText(CSVoutputPATH3)
            
    def File2CSV(self):
        TXTinputPATH =  self.ui.File2lineEdit.text() #filename2
        CSVoutputPATH = 'OutputTemp.CSV'
        CSVoutputPATH2 = '02_Output.CSV'
        CSVoutputPATH3 = "02_" + os.path.basename(TXTinputPATH).split('.')[0] + "_trimed.csv"
        XLSXoutputPATH = "02_" + os.path.basename(TXTinputPATH).split('.')[0] + "_trimed.xlsx"
        TEMPouputPATH = 'tempoutput.txt'
        
        if not os.path.exists(TXTinputPATH) or TXTinputPATH == "Please open and select File 1...":
            MsgError1 = "Is FILE1 inputed or existed together? \n"
            print(MsgError1, "\n")
            self.ui.Msg4textBrowser.setText(MsgError1)
            return
        if not os.path.splitext(TXTinputPATH)[1] == ".TXT":
            MsgError4 = "Is FILE 1 .TXT text document collect? \n"
            print(MsgError4, "\n")
            self.ui.Msg4textBrowser.setText(MsgError4)
            return

        ## Go Loop
        with open(TXTinputPATH, 'r') as checkfile:
            linecount = len(checkfile.readlines())
        #print(linecount)
        progress = tqdm(total=linecount)
        checkfile.close()
        
        print("Converting and processing!!")
        txt = ""
        with open(TXTinputPATH, 'r', encoding='UTF-8') as file:
            #while (line := file.readline().rstrip()):
            nonempty = filter(str.rstrip, file)
            for line in nonempty:
                ## DEV
                #print("before : ", line)
                
                if "%" in line.strip():
                    line = ""
                paramNUM = str(line[:6])
                #paramNUM = line.rsplit('Q1L1P', 1)[0]

                ##### for older bck format
                #line = re.sub(r"\s+", ",", line)
                line = line.replace(" ", "")
                if not len(line) == 0:
                    if not line[6:8] == "Q1":
                        #print(line[6:8])
                        line = line[:6] + "Q1" + line[6:]
                

                ##### for newer bck format                
                #line = line.replace("A11P", "\nA11")
                line = line.rsplit('A7', 1)[0]
                line = line.rsplit('S5', 1)[0]
                
                line = line.replace("Q1L1P", ",L1,")
                line = line.replace("L2P", "\n" + paramNUM + ",L2,")
                line = line.replace("L3P", "\n" + paramNUM + ",L3,")
                line = line.replace("L4P", "\n" + paramNUM + ",L4,")

                line = line.replace("Q1A1M", ",A1,")
                line = line.replace("A2M", "\n" + paramNUM + ",A2,")
                line = line.replace("A3M", "\n" + paramNUM + ",A3,")
                line = line.replace("A4M", "\n" + paramNUM + ",A4,")
                line = line.replace("A5M", "\n" + paramNUM + ",A5,")
                line = line.replace("A6M", "\n" + paramNUM + ",A6,")

                line = line.replace("Q1L1M", ",A1,")
                line = line.replace("L2M", "\n" + paramNUM + ",L2,")
                line = line.replace("L3M", "\n" + paramNUM + ",L3,")
                line = line.replace("L4M", "\n" + paramNUM + ",L4,")

                line = line.replace("Q1T1P", ",T1,")
                ine = line.replace("T2P", "\n" + paramNUM + ",T2,")
                line = line.replace("T3P", "\n" + paramNUM + ",T3,")
                line = line.replace("T4P", "\n" + paramNUM + ",T4,")

                line = line.replace("Q1M", ",M,")
                
                line = line.replace("Q1S1P", ",S1,")
                line = line.replace("S2P", "\n" + paramNUM + ",S2,")
                line = line.replace("S3P", "\n" + paramNUM + ",S3,")
                line = line.replace("S4P", "\n" + paramNUM + ",S4,")
                
                line = line.replace("Q1A1P", ",A1,")
                line = line.replace("A2P", "\n" + paramNUM + ",A2,")
                line = line.replace("A3P", "\n" + paramNUM + ",A3,")
                line = line.replace("A4P", "\n" + paramNUM + ",A4,")        
                line = line.replace("A5P", "\n" + paramNUM + ",A5,")
                line = line.replace("A6P", "\n" + paramNUM + ",A6,")
                line = line.replace("A7P", "\n" + paramNUM + ",A7,")
                line = line.replace("A8P", "\n" + paramNUM + ",A8,")
                line = line.replace("A9P", "\n" + paramNUM + ",A9,")
                line = line.replace("A10P", "\n" + paramNUM + ",A10,")
                line = line.replace("A11P", "\n,A11,")
                line = line.rsplit(',A11', 1)[0]

                line = line.replace("Q1P", ",,")
                #print("Formating:", line)
                txt += line + "\n"

        f = open(TEMPouputPATH,'w',encoding='utf-8')
        #txt = txt.strip()
        f.write(txt)
        f.close()

        file.close()        

        ## Output file
        print("Outputing new format CSV file")
        f = open(TEMPouputPATH,'w', encoding='utf-8')
        txt = txt.strip()
        f.write(txt)
        f.close()

        with open(TEMPouputPATH, 'r', encoding='utf8') as in_file:
            stripped = (line.strip() for line in in_file)
            lines = (line.split(",") for line in stripped if line)
            with open(CSVoutputPATH, 'w') as out_file:
                writer = csv.writer(out_file, dialect="excel")
                writer.writerow(['ParamNO', 'AxisName', 'Value'])
                writer.writerows(lines)
                out_file.close()
        with open(CSVoutputPATH, newline='', encoding='utf8') as in_file:
            with open(CSVoutputPATH2, 'w', newline='') as out_file:
                writer = csv.writer(out_file)
                for row in csv.reader(in_file):
                    if row:
                        writer.writerow(row)
                out_file.close()

        ## Make a CSV format file without 0 value of data
        print("Outputing CSV file without 0 value data")
        df = pd.read_csv(CSVoutputPATH2, encoding='utf8', dtype=str)
        if os.path.exists(CSVoutputPATH3):
            os.remove(CSVoutputPATH3)
            
        #new_df = lambda:self.filter_rows_by_values(df, "Value", ["0","00000000", "0.0"])
        new_df = df[~df["Value"].isin(["0","00000000", "0.0"])]
        
        print(new_df)
        new_df.to_csv(CSVoutputPATH3, index=False, encoding='utf8')

        ## Make a EXCEL format file with and without 0 value of data
        #print("Outputing EXCEL file from CSV data")
        #read_file = pd.read_csv(CSVoutputPATH3, encoding='utf8', dtype=str)
        #read_file.to_excel(XLSXoutputPATH, index=None, header=True)
        #read_file = pd.read_csv(CSVoutputPATH2, encoding='utf8', dtype=str)
        #read_file.to_excel(XLSXoutputPATH2, index=None, header=True)
        
        # check temp file and exited is to delete
        if os.path.exists(CSVoutputPATH):
            os.remove(CSVoutputPATH)
        if os.path.exists(CSVoutputPATH2):
            os.remove(CSVoutputPATH2)

        okMsg = "New CSV file is set : " + CSVoutputPATH3
        self.ui.Msg4textBrowser.setText(okMsg)
        self.ui.File2lineEdit.setText(CSVoutputPATH3)

        
    def filter_rows_by_values(self, df, col, values):
        return df[~df[col].isin(values)]

        
