from PyQt5.QtWidgets import QMainWindow, QWidget, QTabWidget, QVBoxLayout
from ui.tabs.home_tab import HomeTab
from ui.tabs.encryption_tab import Encryption


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('SpeedyOff')

        # 设置默认大小和最小大小
        self.resize(800, 600)  # 设置默认大小
        self.setMinimumSize(600, 400)  # 设置最小大小

        # 创建中心部件和标签页部件
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        tabWidget = QTabWidget()

        # 创建标签页
        tabWidget.addTab(HomeTab(), "主页")
        tabWidget.addTab(Encryption(), "加密/解密")

        # 创建主布局
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(tabWidget)
        centralWidget.setLayout(mainLayout)

        self.show()
