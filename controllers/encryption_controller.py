from PyQt5.QtWidgets import QFileDialog
import pandas as pd
import hashlib
from gmssl import sm4
from models.data_model import DataModel


class EncryptionController:
    def __init__(self, data_model: DataModel, algorithm: str, sm4_key: str = None):
        self.data_model = data_model
        self.algorithm = algorithm
        self.sm4_key = sm4_key
        if algorithm == 'SM4' and sm4_key is None:
            raise ValueError(
                "SM4 key must be provided for SM4 encryption/decryption")
        if algorithm == 'SM4':
            self.sm4_crypt = sm4.CryptSM4()
            self.sm4_crypt.set_key(sm4_key.encode(), sm4.SM4_ENCRYPT)

    def _encrypt_value(self, value: str):
        if self.algorithm == 'MD5':
            return hashlib.md5(value.encode()).hexdigest()
        elif self.algorithm == 'SHA256':
            return hashlib.sha256(value.encode()).hexdigest()
        elif self.algorithm == 'SM4':
            return self.sm4_crypt.crypt_ecb(value.encode()).hex()

    def _decrypt_value(self, value: str):
        if self.algorithm == 'SM4':
            self.sm4_crypt.set_key(self.sm4_key.encode(), sm4.SM4_DECRYPT)
            return bytes.fromhex(value).decode()
        else:
            raise ValueError(
                f"Decryption not supported for algorithm: {self.algorithm}")

    def encrypt_dataframe(self):
        encrypted_df = self.data_model.data.copy()
        for col in encrypted_df.columns:
            encrypted_df[col] = encrypted_df[col].apply(
                lambda x: self._encrypt_value(str(x)))
        return encrypted_df

    def decrypt_dataframe(self):
        if self.algorithm != 'SM4':
            raise ValueError("Decryption is only supported for SM4 algorithm")
        decrypted_df = self.data_model.data.copy()
        for col in decrypted_df.columns:
            decrypted_df[col] = decrypted_df[col].apply(
                lambda x: self._decrypt_value(x))
        return decrypted_df
