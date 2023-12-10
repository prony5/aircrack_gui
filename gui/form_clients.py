# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './gui/form_clients.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(821, 553)
        Dialog.setModal(True)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 821, 551))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidgetClients = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidgetClients.sizePolicy().hasHeightForWidth())
        self.tableWidgetClients.setSizePolicy(sizePolicy)
        self.tableWidgetClients.setMaximumSize(QtCore.QSize(819, 500))
        self.tableWidgetClients.setObjectName("tableWidgetClients")
        self.tableWidgetClients.setColumnCount(5)
        self.tableWidgetClients.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetClients.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetClients.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetClients.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetClients.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetClients.setHorizontalHeaderItem(4, item)
        self.tableWidgetClients.horizontalHeader().setHighlightSections(True)
        self.tableWidgetClients.verticalHeader().setHighlightSections(True)
        self.verticalLayout.addWidget(self.tableWidgetClients)
        self.listViewInfo = QtWidgets.QListView(self.verticalLayoutWidget)
        self.listViewInfo.setMaximumSize(QtCore.QSize(16777215, 400))
        self.listViewInfo.setObjectName("listViewInfo")
        self.verticalLayout.addWidget(self.listViewInfo)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        item = self.tableWidgetClients.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "client"))
        item = self.tableWidgetClients.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "dbm"))
        item = self.tableWidgetClients.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "rate"))
        item = self.tableWidgetClients.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "lost"))
        item = self.tableWidgetClients.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "frames"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
