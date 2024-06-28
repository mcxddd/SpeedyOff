from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
#from ui.encryption_dialog import EncryptionDialog
#from ui.import_dialog import ImportDialog
class EncryptTab(QWidget):
    def __init__(self,):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        #importButton = QPushButton('Import')
        #importButton.clicked.connect(self.showImportDialog)
        #layout.addWidget(importButton)

        encryptButton = QPushButton('Encrypt/Decrypt')
        #encryptButton.clicked.connect(self.showEncryptionDialog)
        layout.addWidget(encryptButton)

        print("EncryptTab OK")
        
        self.setLayout(layout)

    '''    
    def showEncryptionDialog(self):
        dialog = EncryptionDialog(self.data_manager, self)
        dialog.exec_()
        
    def showImportDialog(self):
        dialog = ImportDialog(self.data_manager, self)
        dialog.exec_()
    '''
