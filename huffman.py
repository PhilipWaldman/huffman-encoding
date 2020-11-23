import math
from typing import Tuple, List, Dict, Any


def main():
    message = get_message()
    freqs = sort_freqs(get_frequency(message))
    tree = make_tree(freqs)
    code_book = make_code_book(tree)
    encoded_message = encode_message(message, code_book)
    decoded_message = decode_message(encoded_message, code_book)
    entropy = calc_entropy(freqs)
    ave_info = calc_ave_info(freqs, code_book)
    compress_ratio = len(message) / len(encoded_message)

    print('\nMessage: {}'.format(message))
    print('Frequencies: {}'.format(printable_freqs(freqs)))
    print('Huffman tree: {}'.format(tree))
    print('Code book: {}'.format(code_book))
    print('Encoded message: {}'.format(encoded_message))
    print('Decoded message: {}'.format(decoded_message))
    print('Entropy: {}'.format(round(entropy, 3)))
    print('Average info: {}'.format(round(ave_info, 3)))
    print('Compression ratio: {}'.format(round(compress_ratio, 3)))
    print_tree(tree)


def get_message() -> str:
    """
    Prompts the user to enter a message. if no message is entered 'hot-diggity-dog' is returned.

    :return: The message
    """
    message = input('Enter a message to be encoded: ')
    if len(message) == 0:
        return 'hot-diggity-dog'
    return message


def get_frequency(message: str) -> List[Tuple[str, float]]:
    """
    Calculates the frequencies of every character in message.

    :param message: The message to find the frequencies of.
    :return: A list with the frequency of every character.
    """
    freqs_dict = {}
    for let in message:
        if let in freqs_dict:
            freqs_dict[let] += 1
        else:
            freqs_dict[let] = 1

    freqs = []
    for key, val in freqs_dict.items():
        freqs.append((key, val / len(message)))
    return freqs


def sort_freqs(freqs: List[Tuple[Any, float]]) -> List[Tuple[Any, float]]:
    """
    Sorts the character-frequency pairs in descending order of frequency.

    :param freqs: The frequencies list to be sorted.
    :return: The same list but sorted.
    """
    for i in range(1, len(freqs)):
        j = i - 1
        key = freqs[i]
        while (freqs[j][1] > key[1]) and (j >= 0):
            freqs[j + 1] = freqs[j]
            j -= 1
        freqs[j + 1] = key
    freqs.reverse()
    return freqs


def make_tree(freqs: List[Tuple[Any, float]]) -> list:
    """

    :param freqs: The list with the frequency of every character to make an encoding off.
    :return: A Huffman encoding tree made from the frequencies.
    """
    tree = []
    while len(freqs) > 1:
        tree = [freqs[len(freqs) - 2][0], freqs[len(freqs) - 1][0]]
        freq = freqs[len(freqs) - 2][1] + freqs[len(freqs) - 1][1]
        freqs = freqs[:-2]
        freqs.append((tree, freq))
        freqs = sort_freqs(freqs)
    return tree


def make_code_book(tree: list) -> Dict[str, str]:
    """

    :param tree: The Huffman encoding tree
    :return:
    """
    code_book = {}

    left_branch = tree[0]
    if type(left_branch) is str:
        code_book[left_branch] = '0'
    else:
        sub_tree = make_code_book(left_branch)
        for key in sub_tree.keys():
            sub_tree[key] = '0' + sub_tree[key]
        code_book.update(sub_tree)

    right_branch = tree[1]
    if type(right_branch) is str:
        code_book[right_branch] = '1'
    else:
        sub_tree = make_code_book(right_branch)
        for key in sub_tree.keys():
            sub_tree[key] = '1' + sub_tree[key]
        code_book.update(sub_tree)

    return code_book


def calc_entropy(freqs: List[Tuple[Any, float]]) -> float:
    """

    :param freqs:
    :return:
    """
    entropy = 0
    for key, freq in freqs:
        entropy += freq * math.log2(freq)
    return -entropy


def calc_ave_info(freqs: List[Tuple[str, float]], code_book: Dict[str, str]) -> float:
    """

    :param freqs:
    :param code_book:
    :return:
    """
    info = 0
    for key, freq in freqs:
        info += freq * len(code_book[key])
    return info


def encode_message(message: str, code_book: Dict[str, str]) -> str:
    """

    :param message:
    :param code_book:
    :return:
    """
    encoded_message = ''
    for let in message:
        encoded_message += code_book[let]
    return encoded_message


def decode_message(encoded_message: str, code_book: Dict[str, str]) -> str:
    """

    :param encoded_message:
    :param code_book:
    :return:
    """
    reverse_code_book = flip_dict(code_book)

    decoded_message = ''
    tally = ''
    for i in encoded_message:
        tally += i
        if tally in reverse_code_book:
            decoded_message += reverse_code_book[tally]
            tally = ''
    return decoded_message


def flip_dict(dictionary: dict) -> dict:
    """
    Swaps the key and values in the dictionary.

    :param dictionary: The dictionary to flip.
    :return: A similar dictionary but with the keys and values swapped.
    """
    return {value: key for key, value in dictionary.items()}


def print_tree(tree, layer=0):
    """
    Prints the tree in a more readable format.

    :param layer: The current layer. Only used for the recursion when printing.
    :param tree: The Huffman tree to print
    """
    if type(tree) != str:
        depth_lines = '  |' * (layer + 1)

        print('if 0:\n{}then '.format(depth_lines), end='')
        print_tree(tree[0], layer + 1)

        print('{}else '.format(depth_lines), end='')
        print_tree(tree[1], layer + 1)
    else:
        print(tree)

    if layer == 0:
        depth = calc_depth(tree)
        print('<{}>'.format('-' * (depth * 3 - 2)))
        print('Tree depth: {}'.format(depth))


def calc_depth(tree, depth=0, max_depth=0) -> int:
    """
    Calculates the depth of the tree.

    :param tree: The tree to calculate the depth of.
    :param depth: The current depth. Used for recursion.
    :param max_depth: The max depth. Used to keep track during recursion.
    :return: The depth of the tree.
    """
    if type(tree) != str:
        d0 = calc_depth(tree[0], depth + 1)
        if d0 > max_depth:
            max_depth = d0

        d1 = calc_depth(tree[1], depth + 1)
        if d1 > max_depth:
            max_depth = d1
    else:
        return depth
    return max_depth


def printable_freqs(freqs: List[Tuple[str, float]]) -> List[Tuple[str, float]]:
    """
    Rounds the frequencies to 5 decimal places.

    :param freqs: The list of character-frequency tuples
    where the frequencies may have many numbers after the decimal point.
    :return: The same list but with the frequencies rounded to 5 decimal places.
    """
    return [(key, round(freq, 5)) for key, freq in freqs]


if __name__ == '__main__':
    main()
