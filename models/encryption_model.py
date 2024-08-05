import pandas as pd
import hashlib
from gmssl import sm4
import base64
import openpyxl


class EncryptionModel:
    def __init__(self):
        self.data = None
        self.file_name = None
        self.file_name_base = None
        self.folder_path = None
        self.selected_algorithm = None
        self.encryption_instance = None

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

    def get_file_name(self):
        return self.file_name

    def load_file(self, file_path):
        if file_path.endswith('.csv'):
            self.data = pd.read_csv(file_path)
        else:
            workbook = openpyxl.load_workbook(file_path)
            first_sheet_name = workbook.sheetnames[0]
            sheet = workbook[first_sheet_name]
            data = sheet.values
            columns = next(data)
            self.data = pd.DataFrame(data, columns=columns)

        self.file_name = file_path.split("/")[-1]
        self.file_name_base = self.file_name.rsplit('.', 1)[0]
        self.folder_path = '/'.join(file_path.split('/')[:-1])

    def encrypt_decrypt(self, file_info: dict):
        self.column_indices = file_info.get('column_indices')
        self.include_all = file_info.get('include_all')
        self.selected_algorithm = file_info.get('selected_algorithm')
        self.selected_mode = file_info.get('selected_mode')
        self.key_input = file_info.get('key_input')
        self.key_input = None if self.key_input == '' else self.key_input

        self.encryption_instance = EncryptionFactory.create(
            self.selected_algorithm, self.key_input)

        if self.selected_mode == 'Encrypt':
            encrypted_data = self._encrypt_dataframe()
        elif self.selected_mode == 'Decrypt':
            decrypted_data = self._decrypt_dataframe()

        self.save_data(encrypted_data if self.selected_mode ==
                       'Encrypt' else decrypted_data)

    def save_data(self, output_df: pd.DataFrame):
        if self.selected_mode == 'Encrypt':
            output_df.to_csv(
                f"{self.folder_path}/已加密_{self.file_name_base}.csv", index=False)
        elif self.selected_mode == 'Decrypt':
            output_df.to_csv(
                f"{self.folder_path}/已解密_{self.file_name_base}.csv", index=False)

    def _encrypt_dataframe(self):
        encrypted_df = self.data.copy()
        if self.include_all:
            for col in encrypted_df:
                encrypted_df[col] = encrypted_df[col].apply(
                    lambda x: self.encryption_instance.encrypt(str(x)))
        else:
            for index in self.column_indices:
                encrypted_df.iloc[:, index] = encrypted_df.iloc[:, index].apply(
                    lambda x: self.encryption_instance.encrypt(str(x)))
        return encrypted_df

    def _decrypt_dataframe(self):
        decrypted_df = self.data.copy()
        if self.include_all:
            for col in decrypted_df:
                decrypted_df[col] = decrypted_df[col].apply(
                    lambda x: self.encryption_instance.decrypt(str(x)))
        else:
            for index in self.column_indices:
                decrypted_df.iloc[:, index] = decrypted_df.iloc[:, index].apply(
                    lambda x: self.encryption_instance.decrypt(str(x)))
        return decrypted_df


class EncryptionFactory:
    @staticmethod
    def create(algorithm, key=None):
        if algorithm == 'SHA256':
            return SHA256Encryption()
        elif algorithm == 'MD5':
            return MD5Encryption()
        elif algorithm == 'SM4':
            return SM4Encryption(key)
        elif algorithm == 'BASE64':
            return Base64Encryption()
        else:
            raise ValueError(f"未知算法: {algorithm}")


class EncryptionAlgorithm:
    def encrypt(self, value):
        raise NotImplementedError

    def decrypt(self, value):
        raise NotImplementedError


class SHA256Encryption(EncryptionAlgorithm):
    def encrypt(self, value):
        return hashlib.sha256(value.encode()).hexdigest()

    def decrypt(self, value):
        raise ValueError("SHA256不支持解密")


class MD5Encryption(EncryptionAlgorithm):
    def encrypt(self, value):
        return hashlib.md5(value.encode()).hexdigest()

    def decrypt(self, value):
        raise ValueError("MD5不支持解密")


class SM4Encryption(EncryptionAlgorithm):
    def __init__(self, key):
        if not key:
            raise ValueError("SM4需要密钥")
        self.key = key.encode()
        self.sm4_crypto = sm4.CryptSM4()
        self.sm4_crypto.set_key(key.encode(), sm4.SM4_ENCRYPT)

    def encrypt(self, value):
        encrypt_value = self.sm4_crypto.crypt_ecb(value.encode())
        return base64.b64encode(encrypt_value).decode()

    def decrypt(self, value):
        self.sm4_crypto.set_key(self.key, sm4.SM4_DECRYPT)
        decrypt_value = self.sm4_crypto.crypt_ecb(base64.b64decode(value))
        return decrypt_value.decode()


class Base64Encryption(EncryptionAlgorithm):
    def encrypt(self, value):
        return base64.b64encode(value.encode()).decode()

    def decrypt(self, value):
        return base64.b64decode(value).decode()
