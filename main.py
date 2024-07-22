import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from views.main_window import MainWindow
from presenters.encryption_presenter import EncryptionPresenter
from models.encryption_model import EncryptionModel


def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('assets/psyduck.png'))
    mainWindow = MainWindow()

    encryption_data_model = EncryptionModel()
    encryption_presenter = EncryptionPresenter(encryption_data_model,
                                               mainWindow.get_encryption_tab())
    encryption_presenter.error_occurred.connect(mainWindow.display_error)

    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
