from cryptography.fernet import Fernet
import pandas as pd
import io

class EncryptionModule:
    def _generate_key(self, key):
        return Fernet(Fernet.generate_key())

    def _encrypt_data(self, data, key):
        fernet = self._generate_key(key)
        data_bytes = data.to_csv(index=False).encode('utf-8')
        encrypted_data = fernet.encrypt(data_bytes)
        return encrypted_data

    def _decrypt_data(self, encrypted_data, key):
        fernet = self._generate_key(key)
        decrypted_data = fernet.decrypt(encrypted_data)
        data = pd.read_csv(io.StringIO(decrypted_data.decode('utf-8')))
        return data

    def encrypt_file(self, data, file_path, key):
        encrypted_data = self._encrypt_data(data, key)
        with open(file_path, 'wb') as file:
            file.write(encrypted_data)

    def decrypt_file(self, file_path, key):
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()
        data = self._decrypt_data(encrypted_data, key)
        return data
