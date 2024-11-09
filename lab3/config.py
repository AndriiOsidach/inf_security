# RC5 Configuration
RC5_WORD_SIZE = 32  # w (16, 32, or 64)
RC5_ROUNDS = 16     # r (0 to 255)
RC5_KEY_LENGTH = 8  # b (0 to 255 bytes)

# Derived constants
RC5_WORD_BYTES = RC5_WORD_SIZE // 8
RC5_BLOCK_SIZE = 2 * RC5_WORD_BYTES
RC5_MASK = (1 << RC5_WORD_SIZE) - 1

# Magic constants
RC5_P = {
    16: 0xB7E1,
    32: 0xB7E15163,
    64: 0xB7E151628AED2A6B
}

RC5_Q = {
    16: 0x9E37,
    32: 0x9E3779B9,
    64: 0x9E3779B97F4A7C15
}