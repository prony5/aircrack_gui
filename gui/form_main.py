# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './gui/form_main.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(811, 815)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.settingsLayout = QtWidgets.QVBoxLayout()
        self.settingsLayout.setContentsMargins(-1, -1, -1, 6)
        self.settingsLayout.setObjectName("settingsLayout")
        self.settingsGrid = QtWidgets.QGridLayout()
        self.settingsGrid.setContentsMargins(-1, -1, -1, 6)
        self.settingsGrid.setHorizontalSpacing(6)
        self.settingsGrid.setVerticalSpacing(12)
        self.settingsGrid.setObjectName("settingsGrid")
        self.ComboBoxDev = QtWidgets.QComboBox(self.centralwidget)
        self.ComboBoxDev.setObjectName("ComboBoxDev")
        self.settingsGrid.addWidget(self.ComboBoxDev, 0, 3, 1, 3)
        self.pushButtonStop = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonStop.setObjectName("pushButtonStop")
        self.settingsGrid.addWidget(self.pushButtonStop, 0, 7, 1, 1)
        self.pushButtonStart = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonStart.setObjectName("pushButtonStart")
        self.settingsGrid.addWidget(self.pushButtonStart, 0, 6, 1, 1)
        self.checkBoxScan = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxScan.setObjectName("checkBoxScan")
        self.settingsGrid.addWidget(self.checkBoxScan, 0, 8, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.settingsGrid.addWidget(self.label_4, 0, 1, 1, 1)
        self.settingsLayout.addLayout(self.settingsGrid)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tableWidgetAP = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidgetAP.setObjectName("tableWidgetAP")
        self.tableWidgetAP.setColumnCount(6)
        self.tableWidgetAP.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetAP.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetAP.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetAP.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetAP.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetAP.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetAP.setHorizontalHeaderItem(5, item)
        self.horizontalLayout_2.addWidget(self.tableWidgetAP)
        self.settingsLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.settingsLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButtonStop.setText(_translate("MainWindow", "Stop"))
        self.pushButtonStart.setText(_translate("MainWindow", "Start"))
        self.checkBoxScan.setText(_translate("MainWindow", "Scan"))
        self.label_4.setText(_translate("MainWindow", "Interface"))
        item = self.tableWidgetAP.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ESSID"))
        item = self.tableWidgetAP.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "BSSID"))
        item = self.tableWidgetAP.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "channel"))
        item = self.tableWidgetAP.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "dbm"))
        item = self.tableWidgetAP.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "encryption"))
        item = self.tableWidgetAP.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "clients"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())