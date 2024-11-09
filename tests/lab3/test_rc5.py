import os
from tempfile import NamedTemporaryFile

import pytest

from lab3 import config
from lab3.rc5 import (
    key_expansion, left_rotate, right_rotate, rc5_encrypt_block,
    rc5_decrypt_block, pad, unpad, process_file_
)


@pytest.fixture
def test_key():
    return b'TestKey123'


@pytest.fixture
def test_data():
    return b'Hello, World!'


def test_key_expansion(test_key):
    S = key_expansion(test_key)
    assert len(S) == 2 * (config.RC5_ROUNDS + 1)
    assert all(isinstance(x, int) for x in S)


def test_rotations():
    value = 0x12345678
    bits = 4
    # Test left rotation
    left = left_rotate(value, bits)
    # Test right rotation
    right = right_rotate(left, bits)
    assert right == value & config.RC5_MASK


def test_encrypt_decrypt_block():
    key = b'TestKey123'
    S = key_expansion(key)
    plaintext = b'Hello, World!'
    padded = pad(plaintext)

    # Test encryption
    encrypted = rc5_encrypt_block(padded[:config.RC5_BLOCK_SIZE], S)
    assert len(encrypted) == config.RC5_BLOCK_SIZE

    # Test decryption
    decrypted = rc5_decrypt_block(encrypted, S)
    assert len(decrypted) == config.RC5_BLOCK_SIZE
    assert decrypted == padded[:config.RC5_BLOCK_SIZE]


def test_padding():
    data = b'Test'
    padded = pad(data)
    assert len(padded) % config.RC5_BLOCK_SIZE == 0
    unpadded = unpad(padded)
    assert unpadded == data


def test_file_encryption_decryption():
    # Create temporary files for testing
    with NamedTemporaryFile(delete=False) as input_file, \
            NamedTemporaryFile(delete=False) as encrypted_file, \
            NamedTemporaryFile(delete=False) as decrypted_file:
        # Write test data
        test_data = b'Hello, World! This is a test file.'
        input_file.write(test_data)
        input_file.flush()

        password = "test_password"

        # Test encryption
        encrypt_result = process_file_(
            input_file.name, password, encrypted_file.name, encrypt=True
        )
        assert "encrypted successfully" in encrypt_result

        # Test decryption
        decrypt_result = process_file_(
            encrypted_file.name, password, decrypted_file.name, encrypt=False
        )
        assert "decrypted successfully" in decrypt_result

        # Verify decrypted content matches original
        with open(decrypted_file.name, 'rb') as f:
            decrypted_data = f.read()
        assert decrypted_data == test_data

        # Cleanup
        os.unlink(input_file.name)
        os.unlink(encrypted_file.name)
        os.unlink(decrypted_file.name)