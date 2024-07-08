from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt


class Encryption(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        mainVLayout = QVBoxLayout()

        importRowLayout = QHBoxLayout()

        welcomeLabel = QLabel('Import your file.')
        welcomeLabel.setAlignment(Qt.AlignCenter)
        self.importButton = QPushButton("Choose")
        # importButton.setAlignment(Qt.AlignRight)

        importRowLayout.addWidget(welcomeLabel)
        importRowLayout.addWidget(self.importButton)

        mainVLayout.addLayout(importRowLayout)
        mainVLayout.addStretch(1)

        self.setLayout(mainVLayout)

    def import_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            None, "Import File", "", "CSV Files (*.csv);;Excel Files (*.xlsx)", options=options)
        if file_path:
            data = self.load_data(file_path)
            self.analyze_data(data)
