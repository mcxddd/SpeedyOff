from PyQt5.QtWidgets import QDialog, QFileDialog, QVBoxLayout, QPushButton, QLabel, QLineEdit
from modules.encryption_module import EncryptionModule

class EncryptionDialog(QDialog):
    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.encryption_module = EncryptionModule()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Encrypt/Decrypt File')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel('Enter Encryption Key', self)
        layout.addWidget(self.label)

        self.keyInput = QLineEdit(self)
        layout.addWidget(self.keyInput)

        encryptButton = QPushButton('Encrypt File', self)
        encryptButton.clicked.connect(self.encryptFile)
        layout.addWidget(encryptButton)

        decryptButton = QPushButton('Decrypt File', self)
        decryptButton.clicked.connect(self.decryptFile)
        layout.addWidget(decryptButton)

        self.setLayout(layout)

    def encryptFile(self):
        key = self.keyInput.text()
        if key:
            fileName, _ = QFileDialog.getSaveFileName(self, "Save Encrypted File", "", "CSV Files (*.csv);;Excel Files (*.xlsx)")
            if fileName:
                try:
                    data = self.data_manager.get_data()
                    self.encryption_module.encrypt_file(data, fileName, key)
                    self.label.setText(f"File encrypted: {fileName}")
                except Exception as e:
                    self.label.setText(f"Error: {e}")
        else:
            self.label.setText("Please enter an encryption key")

    def decryptFile(self):
        key = self.keyInput.text()
        if key:
            fileName, _ = QFileDialog.getOpenFileName(self, "Open Encrypted File", "", "CSV Files (*.csv);;Excel Files (*.xlsx)")
            if fileName:
                try:
                    data = self.encryption_module.decrypt_file(fileName, key)
                    self.data_manager.store_data(data)
                    self.label.setText(f"File decrypted: {fileName}")
                except Exception as e:
                    self.label.setText(f"Error: {e}")
        else:
            self.label.setText("Please enter a decryption key")
