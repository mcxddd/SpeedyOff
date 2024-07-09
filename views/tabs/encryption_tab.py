from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFileDialog, QSizePolicy, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from controllers.encryption_controller import EncryptionController
from controllers.data_controller import DataController


class Encryption(QWidget):
    def __init__(self):
        super().__init__()
        self.dataController = DataController(self.model)
        self.encryptionController = EncryptionController(
            self.dataController.get_data(), 'SM4')
        self.initUI()

    def initUI(self):
        mainVLayout = QVBoxLayout()

        importRowLayout = QHBoxLayout()

        welcomeLabel = QLabel('Import your file.')
        welcomeLabel.setAlignment(Qt.AlignCenter)
        self.importButton = QPushButton("Choose")
        # importButton.setAlignment(Qt.AlignRight)
        self.importButton.clicked.connect(self.upload_file)

        importRowLayout.addWidget(welcomeLabel)
        importRowLayout.addWidget(self.importButton)

        mainVLayout.addLayout(importRowLayout)
        mainVLayout.addStretch(1)

        self.setLayout(mainVLayout)

    def upload_file(self):
        file_path = self.file_path_edit.text()
        if file_path:
            try:
                self.DataController.load_csv(file_path)
                data = self.data_controller.get_data()
                if not data.empty:
                    self.displayData(data)
                    self.column_select.addItems(data.columns)
            except ValueError as e:
                self.showError(str(e))
