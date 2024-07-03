from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy, QHBoxLayout
from PyQt5.QtCore import Qt


class Encryption(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout()

        welcomeLabel = QLabel('Welcome to SpeedyOff')
        welcomeLabel.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(welcomeLabel)

        infoLabel = QLabel('Please select a function from the tabs above.')
        infoLabel.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(infoLabel)

        # 添加一个伸缩项，使版权信息和联系人方式靠近底部
        mainLayout.addSpacerItem(QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(mainLayout)
