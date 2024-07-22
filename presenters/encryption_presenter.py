from PyQt5.QtWidgets import QFileDialog
import pandas as pd
import hashlib
from gmssl import sm4
from models.encryption_model import EncryptionModel
from PyQt5.QtCore import QObject, pyqtSignal, Qt, pyqtSignal, pyqtSlot

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
                f"upper layer Error loading file: {str(e)}")

    def handle_encrypt_decrypt_request(self, data: dict):
        try:
            self.file_path = data.get('file_path')
            self.column_indices = data.get('column_indices')
            self.include_all = data.get('include_all')
            self.selected_algorithm = data.get('selected_algorithm')
            self.selected_mode = data.get('selected_mode')

            if self.algorithm is None:
                self.error_occurred.emit("No algorithm selected")

            if self.selected_algorithm == 'SM4' and self.sm4_key is None:
                self.error_occurred.emit(
                    "SM4 key must be provided for SM4 encryption/decryption")

            if self.selected_algorithm == 'SM4':
                self.sm4_crypt = sm4.CryptSM4()
                self.sm4_crypt.set_key(self.sm4_key.encode(), sm4.SM4_ENCRYPT)

            if self.selected_mode == 'Encrypt':
                encrypted_data = self.encrypt_dataframe()
                self.view.update_text_area(encrypted_data.to_string())
            elif self.selected_mode == 'Decrypt':
                decrypted_data = self.decrypt_dataframe()
                self.view.update_text_area(decrypted_data.to_string())
            else:
                self.error_occurred.emit(
                    f"Unknown action: {data.get('selected_mode')}")
        except Exception as e:
            self.error_occurred.emit(
                f"Error in encryption/decryption: {str(e)}")
