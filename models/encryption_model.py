import pandas as pd
import hashlib
from gmssl import sm4


class EncryptionModel:
    def __init__(self):
        self.data = None
        self.file_name = None
        self.folder_path = None
        self.algorithm = None
        self.sm4_key = None
        self.sm4_crypto = None

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

    def load_file(self, file_path):
        if file_path.endswith('.csv'):
            self.data = pd.read_csv(file_path)
        else:
            self.data = pd.read_excel(file_path)
            # Update the model with the file content
            self.file_name = file_path.split("/")[-1]
            self.folder_path = '/'.join(file_path.split('/')[:-1])

    def set_algorithm(self, algorithm, sm4_key=None):
        self.algorithm = algorithm
        self.sm4_key = sm4_key
        if algorithm == 'SM4' and sm4_key is not None:
            self.sm4_crypto = sm4.CryptSM4()
            self.sm4_crypto.set_key(sm4_key.encode(), sm4.SM4_ENCRYPT)

    def encrypt_dataframe(self):
        encrypted_df = self.data.copy()
        for col in encrypted_df.columns:
            encrypted_df[col] = encrypted_df[col].apply(
                lambda x: self._encrypt_value(str(x)))
        return encrypted_df

    def decrypt_dataframe(self):
        if self.algorithm != 'SM4':
            raise ValueError("Decryption is only supported for SM4 algorithm")
        decrypted_df = self.data.copy()
        for col in decrypted_df.columns:
            decrypted_df[col] = decrypted_df[col].apply(
                lambda x: self._decrypt_value(x))
        return decrypted_df

    def _encrypt_value(self, value):
        if self.algorithm == 'sha256':
            return hashlib.sha256(value.encode()).hexdigest()
        elif self.algorithm == 'md5':
            return hashlib.md5(value.encode()).hexdigest()
        elif self.algorithm == 'SM4':
            return self.sm4_crypto.crypt_ecb(value.encode()).hex()
        else:
            raise ValueError(f"Unknown algorithm: {self.algorithm}")

    def _decrypt_value(self, value):
        if self.algorithm == 'SM4':
            self.sm4_crypto.set_key(self.sm4_key.encode(), sm4.SM4_DECRYPT)
            return bytes.fromhex(value).decode()
        else:
            raise ValueError(
                f"Decryption not supported for algorithm: {self.algorithm}")
