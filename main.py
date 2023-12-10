import argparse
import sys
import subprocess
import pyrcrack
import asyncio
import multiprocessing

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from gui.form_main import Ui_MainWindow
from gui.form_clients import Ui_Dialog

from time import sleep
from queue import Queue

SCAN_FREQ = 0.5  # hz


async def scan(args, q: Queue):
    async for result in pyrcrack.AirodumpNg()(*args):
        if not q.full():
            q.put(result)
    await asyncio.sleep(1/SCAN_FREQ)


def scanWorker(args, q: Queue):
    asyncio.run(scan(args, q))


class ClientsWindow(QDialog):

    __bssid = ""
    __channel = ""
    __iface = ""

    __scan_worker: multiprocessing.Process = None

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.tableWidgetClients.setSortingEnabled(True)
        self.ui.tableWidgetClients.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableWidgetClients.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tableWidgetClients.cellDoubleClicked.connect(self.__onTableWidgetClientsCellClick)
        self.__scan_result = multiprocessing.Manager().Queue(1)

        self.timer_grid = QTimer()
        self.timer_grid.timeout.connect(self.__updateGrid)

    def setClient(self, bssid, channel, iface):
        self.__bssid = bssid
        self.__channel = channel
        self.__iface = iface

    def showEvent(self, a0):
        self.setWindowTitle(f'BSSID - {self.__bssid} Channel - {self.__channel}')
        self.__scanStart()
        return super().showEvent(a0)

    def closeEvent(self, event):
        self.__scanStop()

    def __scan_result_clear(self):
        if not self.__scan_result.empty():
            self.__scan_result.get_nowait()

    def __scanStart(self):
        self.timer_grid.start(1000/SCAN_FREQ)

        self.__scan_result_clear()
        self.__scan_worker = multiprocessing.Process(
            args=(
                (
                    '--bssid', self.__bssid,
                    '-c', self.__channel,
                    # '-w' + 'file',
                    self.__iface,
                ),
                self.__scan_result),
            target=scanWorker)
        self.__scan_worker.start()

    def __scanStop(self):
        self.timer_grid.stop()
        if not self.__scan_worker is None:
            try:
                self.__scan_worker.kill()
            finally:
                self.__scan_worker = None

    def __setGridItem(self, row, col, value):
        item = self.ui.tableWidgetClients.item(row, col)
        if item is None:
            item = QTableWidgetItem(value)
            self.ui.tableWidgetClients.setItem(row, col, item)
        else:
            item.setText(value)

    def __updateGrid(self):
        if self.__scan_result.empty():
            return

        scan = self.__scan_result.get_nowait()
        if len(scan) == 0:
            return

        for c in scan[0].clients:
            mathing_items = self.ui.tableWidgetClients.findItems(c.bssid, Qt.MatchContains)
            if len(mathing_items) == 0:
                row = self.ui.tableWidgetClients.rowCount()
                self.ui.tableWidgetClients.insertRow(row)
            else:
                row = mathing_items[0].row()

            self.__setGridItem(row, 0, c.bssid)
            self.__setGridItem(row, 1, c.dbm)
            self.__setGridItem(row, 4, c.packets)

        self.ui.tableWidgetClients.resizeColumnsToContents()

    def __onTableWidgetClientsCellClick(self, row, col):
        pass

class MainWindow(QMainWindow):

    __scan_worker: multiprocessing.Process = None

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.client_window = ClientsWindow()

        self.__scan_result = multiprocessing.Manager().Queue(1)
        self.airmon = pyrcrack.AirmonNg()

        self.__preconfigure_ui()
        self.timer_grid = QTimer()
        self.timer_grid.timeout.connect(self.__updateGrid)

    def __onStopButton(self):
        self.__scanStop()
        self.ui.checkBoxScan.setChecked(False)
        self.ui.pushButtonStop.setEnabled(False)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.airmon.run('stop', self.ui.ComboBoxDev.itemText(0)))
        sleep(3)
        self.__fill_iwlist()

    def __onStartButton(self):
        self.ui.pushButtonStart.setEnabled(False)
        self.__clearGrid(self.ui.tableWidgetAP)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.airmon.run('start', self.ui.ComboBoxDev.itemText(0)))
        sleep(3)
        self.__fill_iwlist()

    def __clearGrid(self, grid):
        for i in range(0, grid.rowCount()):
            grid.removeRow(0)

    def __setGridItem(self, row, col, value):
        item = self.ui.tableWidgetAP.item(row, col)
        if item is None:
            item = QTableWidgetItem(value)
            self.ui.tableWidgetAP.setItem(row, col, item)
        else:
            item.setText(value)

    def __updateGrid(self):
        if self.__scan_result.empty():
            return

        scan = self.__scan_result.get_nowait()
        for s in scan:
            mathing_items = self.ui.tableWidgetAP.findItems(s['bssid'], Qt.MatchContains)
            if len(mathing_items) == 0:
                row = self.ui.tableWidgetAP.rowCount()
                self.ui.tableWidgetAP.insertRow(row)
            else:
                row = mathing_items[0].row()

            self.__setGridItem(row, 0, s['essid'])
            self.__setGridItem(row, 1, s['bssid'])
            self.__setGridItem(row, 2, s['channel'])
            self.__setGridItem(row, 3, s['dbm'])
            self.__setGridItem(row, 4, s['encryption'])
            self.__setGridItem(row, 5, (len(s.clients)).__str__())

        self.ui.tableWidgetAP.resizeColumnsToContents()

    def __scan_result_clear(self):
        if not self.__scan_result.empty():
            self.__scan_result.get_nowait()

    def __scanStart(self):
        self.timer_grid.start(1000/SCAN_FREQ)

        self.__scan_result_clear()
        self.__scan_worker = multiprocessing.Process(
            args=((self.ui.ComboBoxDev.itemText(0)), self.__scan_result,),
            target=scanWorker)
        self.__scan_worker.start()

    def __scanStop(self):
        self.timer_grid.stop()
        if not self.__scan_worker is None:
            try:
                self.__scan_worker.kill()
            finally:
                self.__scan_worker = None

    def __onScanClick(self):
        self.client_window.setClient("D8:AF:81:C1:57:AE", 4, self.ui.ComboBoxDev.itemText(0))
        self.__clearGrid(self.client_window.ui.tableWidgetClients)
        self.client_window.exec_()

        # if self.ui.checkBoxScan.isChecked():
        #    self.__scanStart()
        # else:
        #    self.__scanStop()

    def __onTableWidgetAPCellClick(self, row, col):
        self.__scanStop()
        self.ui.checkBoxScan.setChecked(False)

        self.client_window.setClient(
            self.ui.tableWidgetAP.item(row, 1).text(),
            self.ui.tableWidgetAP.item(row, 2).text(),
            self.ui.ComboBoxDev.itemText(0)
        )
        self.__clearGrid(self.client_window.ui.tableWidgetClients)
        self.client_window.exec_()

    def __preconfigure_ui(self):
        self.ui.tableWidgetAP.setSortingEnabled(True)
        self.ui.tableWidgetAP.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableWidgetAP.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.pushButtonStart.clicked.connect(self.__onStartButton)
        self.ui.pushButtonStop.clicked.connect(self.__onStopButton)
        self.ui.checkBoxScan.clicked.connect(self.__onScanClick)
        self.ui.tableWidgetAP.cellDoubleClicked.connect(self.__onTableWidgetAPCellClick)
        self.__fill_iwlist()

    def __fill_iwlist(self):
        self.ui.ComboBoxDev.clear()
        result = subprocess.run(['iwconfig'], capture_output=True, text=True).stdout.split('\n')
        if len(result) > 0:
            iwline = result[0]
            if iwline.find('IEEE 802.11') > 0:
                iface = result[0].split(' ')[0]
                self.ui.ComboBoxDev.addItem(iface)
                isMon = iface.find('mon') > 0
                self.ui.pushButtonStart.setEnabled(not isMon)
                self.ui.pushButtonStop.setEnabled(isMon)
                self.ui.checkBoxScan.setEnabled(isMon)

    def closeEvent(self, event):
        self.__scanStop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
