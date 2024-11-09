import os
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock, patch

import pytest

from lab4.rsa import RSA


@pytest.fixture
def rsa_crypto():
    crypto = RSA()
    crypto.generate_keys()
    return crypto


@pytest.fixture
def test_dir():
    with TemporaryDirectory() as tmp_dir:
        yield tmp_dir


def test_key_generation(rsa_crypto):
    assert rsa_crypto.private_key is not None
    assert rsa_crypto.public_key is not None


def test_key_save_load(rsa_crypto, test_dir):
    private_key_path = os.path.join(test_dir, 'private.pem')
    public_key_path = os.path.join(test_dir, 'public.pem')

    # Save keys
    rsa_crypto.save_keys(private_key_path, public_key_path)

    # Verify files exist
    assert os.path.exists(private_key_path)
    assert os.path.exists(public_key_path)

    # Load keys into new instance
    new_rsa = RSA()
    new_rsa.load_keys(private_key_path, public_key_path)

    assert new_rsa.private_key is not None
    assert new_rsa.public_key is not None


def test_encryption_decryption(rsa_crypto, test_dir):
    test_data = b"Test message for encryption"
    input_file = os.path.join(test_dir, 'input.txt')
    encrypted_file = os.path.join(test_dir, 'encrypted.bin')
    decrypted_file = os.path.join(test_dir, 'decrypted.txt')

    # Write test data
    with open(input_file, 'wb') as f:
        f.write(test_data)

    # Perform encryption and decryption
    rsa_crypto.encrypt_file(input_file, encrypted_file)
    rsa_crypto.decrypt_file(encrypted_file, decrypted_file)

    # Verify decrypted content
    with open(decrypted_file, 'rb') as f:
        decrypted_data = f.read()

    assert test_data == decrypted_data


def test_large_file_handling(rsa_crypto, test_dir):
    large_data = os.urandom(1024 * 1024)  # 1 MB
    input_file = os.path.join(test_dir, 'large_input.bin')
    encrypted_file = os.path.join(test_dir, 'large_encrypted.bin')
    decrypted_file = os.path.join(test_dir, 'large_decrypted.bin')

    # Write test data
    with open(input_file, 'wb') as f:
        f.write(large_data)

    # Perform encryption and decryption
    rsa_crypto.encrypt_file(input_file, encrypted_file)
    rsa_crypto.decrypt_file(encrypted_file, decrypted_file)

    # Verify decrypted content
    with open(decrypted_file, 'rb') as f:
        decrypted_data = f.read()

    assert large_data == decrypted_data


def test_encryption_with_invalid_input(rsa_crypto, test_dir):
    non_existent_file = os.path.join(test_dir, 'nonexistent.txt')
    output_file = os.path.join(test_dir, 'output.bin')

    with pytest.raises(FileNotFoundError):
        rsa_crypto.encrypt_file(non_existent_file, output_file)


def test_decryption_with_invalid_input(rsa_crypto, test_dir):
    non_existent_file = os.path.join(test_dir, 'nonexistent.bin')
    output_file = os.path.join(test_dir, 'output.txt')

    with pytest.raises(FileNotFoundError):
        rsa_crypto.decrypt_file(non_existent_file, output_file)


def test_measure_performance():
    # Arrange
    rsa_instance = RSA()
    rsa_instance.generate_keys()  # Ensure keys are generated to avoid NoneType errors

    mock_encrypt_file = MagicMock()
    mock_decrypt_file = MagicMock()

    # Patch dependencies
    with patch("os.urandom", return_value=b'0' * 1024 * 1024), \
            patch("builtins.open", new_callable=MagicMock), \
            patch("time.time", side_effect=[1, 2, 3, 4, 5, 6, 7, 8]), \
            patch("os.remove"), \
            patch.object(rsa_instance, "encrypt_file", mock_encrypt_file), \
            patch.object(rsa_instance, "decrypt_file", mock_decrypt_file), \
            patch("lab3.rc5.encrypt_file_rc5_", MagicMock()), \
            patch("lab3.rc5.decrypt_file_rc5_", MagicMock()):
        # Act
        encryption_time, decryption_time, rca5_enc_time, rca5_dec_time = rsa_instance.measure_performance()
