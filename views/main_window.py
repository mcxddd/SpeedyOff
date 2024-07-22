from PyQt5.QtWidgets import QMainWindow, QWidget, QTabWidget, QVBoxLayout, QMessageBox
from views.tabs.home_tab import HomeTab
from views.tabs.encryption_tab import EncryptionTab


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
        self.tabWidget = QTabWidget()

        # 创建标签页
        self.home_tab = HomeTab()
        self.encryption_tab = EncryptionTab()
        self.tabWidget.addTab(self.home_tab, "主页")
        self.tabWidget.addTab(self.encryption_tab, "加密/解密")

        # 创建主布局
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.tabWidget)
        centralWidget.setLayout(mainLayout)

        self.show()

    def get_home_tab(self):
        return self.home_tab

    def get_encryption_tab(self):
        return self.encryption_tab

    def display_error(self, message):
        QMessageBox.critical(self, "Error", message)
