import os
import time

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

from lab3 import rc5


class RSA:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def generate_keys(self, key_size=2048):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size
        )
        self.public_key = self.private_key.public_key()

    def save_keys(self, private_key_path, public_key_path):
        private_pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        public_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        with open(private_key_path, 'wb') as f:
            f.write(private_pem)
        with open(public_key_path, 'wb') as f:
            f.write(public_pem)

    def load_keys(self, private_key_path, public_key_path):
        with open(private_key_path, 'rb') as f:
            self.private_key = serialization.load_pem_private_key(
                f.read(),
                password=None
            )

        with open(public_key_path, 'rb') as f:
            self.public_key = serialization.load_pem_public_key(
                f.read()
            )

    def encrypt_file(self, input_path, output_path):
        chunk_size = 190  # Максимальний розмір блоку для RSA-2048

        with open(input_path, 'rb') as in_file, open(output_path, 'wb') as out_file:
            while True:
                chunk = in_file.read(chunk_size)
                if not chunk:
                    break

                encrypted = self.public_key.encrypt(
                    chunk,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                out_file.write(len(encrypted).to_bytes(4, byteorder='big'))
                out_file.write(encrypted)

    def decrypt_file(self, input_path, output_path):
        with open(input_path, 'rb') as in_file, open(output_path, 'wb') as out_file:
            while True:
                size_bytes = in_file.read(4)
                if not size_bytes:
                    break

                chunk_size = int.from_bytes(size_bytes, byteorder='big')
                encrypted_chunk = in_file.read(chunk_size)

                decrypted = self.private_key.decrypt(
                    encrypted_chunk,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                out_file.write(decrypted)

    def measure_performance(self, file_size_mb=1):
        test_file = "test_data.bin"
        encrypted_file = "encrypted.bin"
        decrypted_file = "decrypted.bin"

        with open(test_file, 'wb') as f:
            f.write(os.urandom(file_size_mb * 1024 * 1024))

        start_time = time.time()
        self.encrypt_file(test_file, encrypted_file)
        encryption_time = time.time() - start_time

        start_time = time.time()
        self.decrypt_file(encrypted_file, decrypted_file)
        decryption_time = time.time() - start_time

        start_time = time.time()
        rc5.encrypt_file_rc5_(test_file, 'abc', encrypted_file)
        rca5_enc_time = time.time() - start_time

        start_time = time.time()
        rc5.decrypt_file_rc5_(encrypted_file, 'abc', decrypted_file)
        rca5_dec_time = time.time() - start_time

        os.remove(test_file)
        os.remove(encrypted_file)
        os.remove(decrypted_file)

        return encryption_time, decryption_time, rca5_enc_time, rca5_dec_time

