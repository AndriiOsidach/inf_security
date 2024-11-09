from lab1.lcg import LCG
from lab2.md5 import MD5
from lab3 import config


def key_expansion(key):
    b = len(key)
    u = config.RC5_WORD_BYTES
    c = (b + u - 1) // u  # ceil(b/u)
    L = [0] * c

    for i in range(b - 1, -1, -1):
        L[i // u] = (L[i // u] << 8) + key[i]

    t = 2 * (config.RC5_ROUNDS + 1)
    S = [0] * t
    S[0] = config.RC5_P[config.RC5_WORD_SIZE]

    for i in range(1, t):
        S[i] = (S[i - 1] + config.RC5_Q[config.RC5_WORD_SIZE]) & config.RC5_MASK

    i = j = 0
    A = B = 0
    for k in range(3 * max(t, c)):
        A = S[i] = left_rotate((S[i] + A + B) & config.RC5_MASK, 3)
        B = L[j] = left_rotate((L[j] + A + B) & config.RC5_MASK, (A + B) % config.RC5_WORD_SIZE)
        i = (i + 1) % t
        j = (j + 1) % c

    return S


def left_rotate(val, n):
    n %= config.RC5_WORD_SIZE
    return ((val << n) | (val >> (config.RC5_WORD_SIZE - n))) & config.RC5_MASK


def right_rotate(val, n):
    n %= config.RC5_WORD_SIZE
    return ((val >> n) | (val << (config.RC5_WORD_SIZE - n))) & config.RC5_MASK


def rc5_encrypt_block(data, S):
    A = int.from_bytes(data[:config.RC5_WORD_BYTES], 'little')
    B = int.from_bytes(data[config.RC5_WORD_BYTES:], 'little')

    A = (A + S[0]) & config.RC5_MASK
    B = (B + S[1]) & config.RC5_MASK

    for i in range(1, config.RC5_ROUNDS + 1):
        A = (left_rotate((A ^ B), B % config.RC5_WORD_SIZE) + S[2 * i]) & config.RC5_MASK
        B = (left_rotate((B ^ A), A % config.RC5_WORD_SIZE) + S[2 * i + 1]) & config.RC5_MASK

    return A.to_bytes(config.RC5_WORD_BYTES, 'little') + B.to_bytes(config.RC5_WORD_BYTES, 'little')


def rc5_decrypt_block(data, S):
    A = int.from_bytes(data[:config.RC5_WORD_BYTES], 'little')
    B = int.from_bytes(data[config.RC5_WORD_BYTES:], 'little')

    for i in range(config.RC5_ROUNDS, 0, -1):
        B = right_rotate((B - S[2 * i + 1]) & config.RC5_MASK, A % config.RC5_WORD_SIZE) ^ A
        A = right_rotate((A - S[2 * i]) & config.RC5_MASK, B % config.RC5_WORD_SIZE) ^ B

    B = (B - S[1]) & config.RC5_MASK
    A = (A - S[0]) & config.RC5_MASK

    return A.to_bytes(config.RC5_WORD_BYTES, 'little') + B.to_bytes(config.RC5_WORD_BYTES, 'little')


def pad(data):
    padding_len = config.RC5_BLOCK_SIZE - (len(data) % config.RC5_BLOCK_SIZE)
    return data + bytes([padding_len] * padding_len)


def unpad(data):
    padding_len = data[-1]
    return data[:-padding_len]


def process_file(file_path, password_phrase, output_file, progress_callback, encrypt=True):
    md5 = MD5()
    key = md5.hash(password_phrase).encode('utf-8')[:config.RC5_KEY_LENGTH]
    S = key_expansion(key)

    lcg = LCG()
    IV = lcg.next().to_bytes(config.RC5_BLOCK_SIZE, 'little')

    processed_size = 0

    with open(file_path, 'rb') as in_file:
        file_size = len(in_file.read())
        in_file.seek(0)

        with open(output_file, 'wb') as out_file:
            if encrypt:
                out_file.write(rc5_encrypt_block(IV, S))
                previous_block = IV
            else:
                encrypted_iv = in_file.read(config.RC5_BLOCK_SIZE)
                IV = rc5_decrypt_block(encrypted_iv, S)
                previous_block = IV

            while True:
                chunk = in_file.read(1024 * 1024)  # Read 1MB at a time
                if not chunk:
                    break

                if encrypt:
                    chunk = pad(chunk)

                result = bytearray()
                for i in range(0, len(chunk), config.RC5_BLOCK_SIZE):
                    block = chunk[i:i + config.RC5_BLOCK_SIZE]
                    if encrypt:
                        block = bytes(a ^ b for a, b in zip(block, previous_block))
                        encrypted_block = rc5_encrypt_block(block, S)
                        result.extend(encrypted_block)
                        previous_block = encrypted_block
                    else:
                        decrypted_block = rc5_decrypt_block(block, S)
                        plain_block = bytes(a ^ b for a, b in zip(decrypted_block, previous_block))
                        result.extend(plain_block)
                        previous_block = block

                if not encrypt:
                    result = unpad(result)

                out_file.write(result)
                processed_size += len(chunk)
                progress = (processed_size / file_size) * 100
                progress_callback(progress)

    return f"File {'encrypted' if encrypt else 'decrypted'} successfully: {output_file}"


def process_file_(file_path, password_phrase, output_file, encrypt=True):
    md5 = MD5()
    key = md5.hash(password_phrase).encode('utf-8')[:config.RC5_KEY_LENGTH]
    S = key_expansion(key)

    lcg = LCG()
    IV = lcg.next().to_bytes(config.RC5_BLOCK_SIZE, 'little')

    processed_size = 0

    with open(file_path, 'rb') as in_file:
        file_size = len(in_file.read())
        in_file.seek(0)

        with open(output_file, 'wb') as out_file:
            if encrypt:
                out_file.write(rc5_encrypt_block(IV, S))
                previous_block = IV
            else:
                encrypted_iv = in_file.read(config.RC5_BLOCK_SIZE)
                IV = rc5_decrypt_block(encrypted_iv, S)
                previous_block = IV

            while True:
                chunk = in_file.read(1024 * 1024)  # Read 1MB at a time
                if not chunk:
                    break

                if encrypt:
                    chunk = pad(chunk)

                result = bytearray()
                for i in range(0, len(chunk), config.RC5_BLOCK_SIZE):
                    block = chunk[i:i + config.RC5_BLOCK_SIZE]
                    if encrypt:
                        block = bytes(a ^ b for a, b in zip(block, previous_block))
                        encrypted_block = rc5_encrypt_block(block, S)
                        result.extend(encrypted_block)
                        previous_block = encrypted_block
                    else:
                        decrypted_block = rc5_decrypt_block(block, S)
                        plain_block = bytes(a ^ b for a, b in zip(decrypted_block, previous_block))
                        result.extend(plain_block)
                        previous_block = block

                if not encrypt:
                    result = unpad(result)

                out_file.write(result)
                processed_size += len(chunk)
                progress = (processed_size / file_size) * 100

    return f"File {'encrypted' if encrypt else 'decrypted'} successfully: {output_file}"


def encrypt_file_rc5(file_path, password_phrase, output_file, progress_callback):
    return process_file(file_path, password_phrase, output_file, progress_callback, encrypt=True)


def decrypt_file_rc5(file_path, password_phrase, output_file, progress_callback):
    return process_file(file_path, password_phrase, output_file, progress_callback, encrypt=False)


def encrypt_file_rc5_(file_path, password_phrase, output_file):
    return process_file_(file_path, password_phrase, output_file, encrypt=True)


def decrypt_file_rc5_(file_path, password_phrase, output_file):
    return process_file_(file_path, password_phrase, output_file, encrypt=False)
