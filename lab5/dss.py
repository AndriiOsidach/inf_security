from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import serialization
from lab5.config import KEY_SIZE


class DigitalSignatureLogic:
    def generate_keys(self):
        self.private_key = dsa.generate_private_key(key_size=KEY_SIZE)
        self.public_key = self.private_key.public_key()

        private_key_pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        public_key_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return private_key_pem, public_key_pem

    def load_keys(self, private_key_path, public_key_path):
        with open(private_key_path, "rb") as private_file:
            private_key_pem = private_file.read()
            self.private_key = serialization.load_pem_private_key(
                private_key_pem,
                password=None
            )

        with open(public_key_path, "rb") as public_file:
            public_key_pem = public_file.read()
            self.public_key = serialization.load_pem_public_key(public_key_pem)

    def sign_text(self, text):
        return self.private_key.sign(text.encode(), hashes.SHA256())

    def sign_file(self, file_content):
        return self.private_key.sign(file_content, hashes.SHA256())

    def verify_signature(self, public_key, data, signature):
        public_key.verify(signature, data, hashes.SHA256())
