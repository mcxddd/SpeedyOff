from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

class ProcessTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        processButton = QPushButton('Process')
        processButton.clicked.connect(self.showProcessingDialog)
        layout.addWidget(processButton)

        # 可以在这里添加更多处理相关的控件
        
        print("ProcessTab OK")
        
        self.setLayout(layout)

    def showProcessingDialog(self):
            print("No data to process")
