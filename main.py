import sys
import subprocess
import pyrcrack
import asyncio
import multiprocessing

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtCore import Qt, QTimer
from gui.gui import Ui_MainWindow

from time import sleep
from queue import Queue

SCAN_FREQ = 0.5  # hz


async def scan(iface, q: Queue):
    async for result in pyrcrack.AirodumpNg()(iface):
        if not q.full():
            q.put(result)
    await asyncio.sleep(1/SCAN_FREQ)


def scanWorker(iface, q: Queue):
    asyncio.run(scan(iface, q))


class MyMainWindow(QMainWindow):

    __scan_worker: multiprocessing.Process = None

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

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
        self.__clearGrid()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.airmon.run('start', self.ui.ComboBoxDev.itemText(0)))
        sleep(3)
        self.__fill_iwlist()

    def __clearGrid(self):
        for i in range(0, self.ui.tableWidgetAP.rowCount()):
            self.ui.tableWidgetAP.removeRow(0)

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
            self.__setGridItem(row, 5, (len(s.clients)-1).__str__())

        self.ui.tableWidgetAP.resizeColumnsToContents()

    def __scan_result_clear(self):
        if not self.__scan_result.empty():
            self.__scan_result.get_nowait()

    def __scanStart(self):
        self.timer_grid.start(1000/SCAN_FREQ)

        self.__scan_result_clear()
        self.__scan_worker = multiprocessing.Process(
            args=(self.ui.ComboBoxDev.itemText(0), self.__scan_result,),
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
        if self.ui.checkBoxScan.isChecked():
            self.__scanStart()
        else:
            self.__scanStop()

    def __preconfigure_ui(self):
        self.ui.pushButtonStart.clicked.connect(self.__onStartButton)
        self.ui.pushButtonStop.clicked.connect(self.__onStopButton)
        self.ui.checkBoxScan.clicked.connect(self.__onScanClick)
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
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
