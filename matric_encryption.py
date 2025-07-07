import numpy as np
from sympy import Matrix
from sympy.matrices.common import NonInvertibleMatrixError

char_encoding = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10,
    'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19,
    'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 26, ' ': 27
}
decode_char = {v: k for k, v in char_encoding.items()}


def create_matrix():
    matrix = []
    for i in range(3):
        row = []
        for j in range(3):
            entry = int(input(f"Enter element at position ({i + 1}, {j + 1}): "))
            row.append(entry)
        matrix.append(row)
    return matrix


def display_matrix(matrix):
    for row in matrix:
        print(row)


def message_to_numeric_blocks(message, block_size):
    message = message.upper()
    nums = [char_encoding.get(char, 27) for char in message]
    while len(nums) % block_size != 0:
        nums.append(27)
    blocks = [nums[i:i + block_size] for i in range(0, len(nums), block_size)]
    return blocks


def encode_message(matrix, blocks):
    result = []
    for block in blocks:
        vec = np.array(block).reshape(-1, 1)  # 3x1
        enc = np.dot(matrix, vec).flatten()
        result.extend(enc.astype(int))
    return result


def decode_message(enc_numbers, inverse_matrix):
    blocks = [enc_numbers[i:i + 3] for i in range(0, len(enc_numbers), 3)]
    decoded_chars = []

    for block in blocks:
        vec = np.array(block).reshape(3, 1)  # 3x1
        result = np.dot(inverse_matrix, vec)
        result = result.round().astype(int).flatten()

        for num in result:
            decoded_chars.append(decode_char.get(num, '?'))

    return ''.join(decoded_chars)


def calculate_inverse(matrix):
    try:
        sympy_matrix = Matrix(matrix)
        inv = sympy_matrix.inv()
        return np.array(inv).astype(np.float64)
    except NonInvertibleMatrixError:
        print("Matrix is not invertible.")
        return None


def main():
    while True:
        choice = input("\nPress 1 to encode a message, or press 2 to decode a message: ")

        if choice == "1":
            print("\n=== Encoding ===")
            matrix = create_matrix()
            print("\nEncoding Matrix:")
            display_matrix(matrix)

            message = input("\nEnter message to encode: ")
            blocks = message_to_numeric_blocks(message, 3)

            encoded = encode_message(np.array(matrix), blocks)
            print("\nEncoded Numeric Stream:")
            print(" ".join(map(str, encoded)))

        elif choice == "2":
            print("\n=== Decoding ===")
            matrix = create_matrix()
            inverse_matrix = calculate_inverse(matrix)
            if inverse_matrix is None:
                continue

            print("\nInverse Matrix:")
            display_matrix(inverse_matrix)

            enc_input = input("Enter the encoded numbers (space-separated): ")
            enc_numbers = list(map(int, enc_input.strip().split()))
            message = decode_message(enc_numbers, inverse_matrix)

            print("\nDecoded Message:")
            print(message)

        else:
            print("Invalid option. Please select 1 or 2.")


if __name__ == "__main__":
    main()
