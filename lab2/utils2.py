from lab2.md5 import MD5


def save_to_file(file_path, content):
    with open(file_path, 'w') as f:
        f.write(content)


def check_file_integrity(file_path, hash_file_path, progress_callback=None):
    md5 = MD5()
    calculated_hash = md5.hash_file(file_path, progress_callback)

    with open(hash_file_path, 'r') as f:
        expected_hash = f.read().strip()

    return calculated_hash.upper() == expected_hash.upper()


def run_md5_tests():
    md5 = MD5()
    test_cases = {
        "": "D41D8CD98F00B204E9800998ECF8427E".lower(),
        "a": "0CC175B9C0F1B6A831C399E269772661".lower(),
        "abc": "900150983CD24FB0D6963F7D28E17F72".lower(),
        "message digest": "F96B697D7CB7938D525A2F31AAF161D0".lower(),
        "abcdefghijklmnopqrstuvwxyz": "C3FCD3D76192E4007DFB496CCA67E13B".lower(),
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789": "D174AB98D277D9F5A5611C2C9F419D9F".lower(),
        "12345678901234567890123456789012345678901234567890123456789012345678901234567890": "57EDF4A22BE3C955AC49DA2E2107B67A".lower()
    }

    results = []
    for input_text, expected_hash in test_cases.items():
        calculated_hash = md5.hash(input_text)
        is_correct = calculated_hash == expected_hash
        results.append(
            f"Input: '{input_text}'\nExpected:   {expected_hash}\nCalculated: {calculated_hash}\nCorrect: {is_correct}\n")

    return "\n".join(results)