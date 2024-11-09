import math
import os
import struct


class MD5:
    def __init__(self):
        self.S = [7, 12, 17, 22] * 4 + [5, 9, 14, 20] * 4 + [4, 11, 16, 23] * 4 + [6, 10, 15, 21] * 4
        self.K = [int(abs(math.sin(i + 1)) * 2 ** 32) & 0xFFFFFFFF for i in range(64)]
        self.A = 0x67452301
        self.B = 0xEFCDAB89
        self.C = 0x98BADCFE
        self.D = 0x10325476

    def left_rotate(self, x, c):
        return ((x << c) | (x >> (32 - c))) & 0xFFFFFFFF

    def compress(self, buf, block):
        a, b, c, d = buf

        for i in range(64):
            if i < 16:
                f = (b & c) | ((~b) & d)
                g = i
            elif i < 32:
                f = (d & b) | ((~d) & c)
                g = (5 * i + 1) % 16
            elif i < 48:
                f = b ^ c ^ d
                g = (3 * i + 5) % 16
            else:
                f = c ^ (b | (~d))
                g = (7 * i) % 16

            temp = d
            d = c
            c = b
            b = (b + self.left_rotate((a + f + self.K[i] + block[g]) & 0xFFFFFFFF, self.S[i])) & 0xFFFFFFFF
            a = temp

        return [(buf[i] + x) & 0xFFFFFFFF for i, x in enumerate([a, b, c, d])]

    def hash(self, message):
        message = bytearray(message.encode('utf-8'))
        orig_len_in_bits = (8 * len(message)) & 0xFFFFFFFFFFFFFFFF
        message.append(0x80)
        while len(message) % 64 != 56:
            message.append(0)
        message += struct.pack('<Q', orig_len_in_bits)

        buf = [self.A, self.B, self.C, self.D]
        for offset in range(0, len(message), 64):
            block = struct.unpack('<16I', message[offset:offset + 64])
            buf = self.compress(buf, block)

        return ''.join(f'{x:02x}' for x in struct.pack('<4I', *buf))

    def hash_file(self, file_path, progress_callback=None):
        buf = [self.A, self.B, self.C, self.D]
        file_size = os.path.getsize(file_path)
        processed_size = 0
        chunk_size = 8192

        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break

                processed_size += len(chunk)
                chunk_len = len(chunk)

                for i in range(0, chunk_len, 64):
                    if i + 64 <= chunk_len:
                        block = struct.unpack('<16I', chunk[i:i + 64])
                        buf = self.compress(buf, block)
                    else:
                        remaining = chunk[i:]
                        break
                else:
                    remaining = b''

                if progress_callback:
                    progress = (processed_size / file_size) * 100
                    if not progress_callback(progress):
                        return None

            orig_len_in_bits = (8 * processed_size) & 0xFFFFFFFFFFFFFFFF
            remaining = bytearray(remaining)
            remaining.append(0x80)
            while len(remaining) % 64 != 56:
                remaining.append(0)
            remaining += struct.pack('<Q', orig_len_in_bits)

            for i in range(0, len(remaining), 64):
                block = struct.unpack('<16I', remaining[i:i + 64])
                buf = self.compress(buf, block)

        if progress_callback:
            progress_callback(100)

        return ''.join(f'{x:02x}' for x in struct.pack('<4I', *buf))
