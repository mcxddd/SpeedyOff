from PyQt5.QtWidgets import QMainWindow, QAction
from ui.import_dialog import ImportDialog
from ui.processing_dialog import ProcessingDialog
from ui.chart_dialog import ChartDialog
from ui.export_dialog import ExportDialog
from ui.encryption_dialog import EncryptionDialog
from modules.import_module import DataManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data_manager = DataManager()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('SpeedyOff')
        self.setGeometry(100, 100, 800, 600)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        importAction = QAction('Import', self)
        importAction.triggered.connect(self.showImportDialog)
        fileMenu.addAction(importAction)

        processAction = QAction('Process', self)
        processAction.triggered.connect(self.showProcessingDialog)
        fileMenu.addAction(processAction)

        chartAction = QAction('Generate Chart', self)
        chartAction.triggered.connect(self.showChartDialog)
        fileMenu.addAction(chartAction)

        exportAction = QAction('Export', self)
        exportAction.triggered.connect(self.showExportDialog)
        fileMenu.addAction(exportAction)

        encryptAction = QAction('Encrypt/Decrypt', self)
        encryptAction.triggered.connect(self.showEncryptionDialog)
        fileMenu.addAction(encryptAction)

        self.show()

    def showImportDialog(self):
        dialog = ImportDialog(self.data_manager, self)
        dialog.exec_()

    def showProcessingDialog(self):
        data = self.data_manager.get_data()
        if data is not None:
            dialog = ProcessingDialog(data, self)
            dialog.exec_()
        else:
            print("No data to process")

    def showChartDialog(self):
        data = self.data_manager.get_data()
        if data is not None:
            dialog = ChartDialog(data, self)
            dialog.exec_()
        else:
            print("No data to generate chart")

    def showExportDialog(self):
        data = self.data_manager.get_data()
        if data is not None:
            dialog = ExportDialog(self.data_manager, self)
            dialog.exec_()
        else:
            print("No data to export")

    def showEncryptionDialog(self):
        dialog = EncryptionDialog(self.data_manager, self)
        dialog.exec_()
