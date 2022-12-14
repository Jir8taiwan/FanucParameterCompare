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
from PyQt5 import QtWidgets
from CtrlBG import MainWindow

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
