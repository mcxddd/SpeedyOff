from models.encryption_model import EncryptionModel
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSignal

from views.tabs.encryption_tab import EncryptionTab


class EncryptionPresenter(QObject):
    error_occurred = pyqtSignal(str)

    def __init__(self, model: EncryptionModel, view: EncryptionTab):
        super().__init__()
        self.view = view
        self.model = model
        self.algorithm = None
        self.sm4_key = None
        self._connect_signals()

    def _connect_signals(self):
        self.view.file_upload_requested.connect(self.handle_file_upload)
        self.view.encrypt_decrypt_requested.connect(
            self.handle_encrypt_decrypt_request)

    def handle_file_upload(self, file_path: str):
        try:
            self.model.load_file(file_path)

            # Update the view's text area with the file content
            self.view.update_file_info(self.model.get_file_name())

            # Update the view's file info label with the file name
        except Exception as e:
            self.error_occurred.emit(
                f"导入文件出错了: {str(e)}")

    def handle_encrypt_decrypt_request(self, file_info: dict):
        try:
            if self.model.get_file_name() is None:
                self.error_occurred.emit(
                    "先上传文件啦.")

            self.model.encrypt_decrypt(file_info)

        except Exception as e:
            self.error_occurred.emit(
                f"加密/解密时发生错误: {str(e)}")
