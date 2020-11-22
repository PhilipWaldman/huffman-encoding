import math


def main():
    message = get_message()
    freqs = sort_freqs(get_frequency(message))
    tree = make_tree(freqs)
    codebook = make_codebook(tree)
    entropy = calc_entropy(freqs)
    ave_info = calc_ave_info(freqs, codebook)
    encoded_message = encode_message(message, codebook)
    compress_ratio = len(message) / len(encoded_message)
    decoded_message = decode_message(encoded_message, codebook)

    print('\nMessage: {}'.format(message))
    print('Frequencies: {}'.format(printable_freqs(freqs)))
    print('Huffman tree: {}'.format(tree))
    print('Codebook: {}'.format(codebook))
    print('Entropy: {}'.format(round(entropy, 3)))
    print('Average info: {}'.format(round(ave_info, 3)))
    print('Encoded message: {}'.format(encoded_message))
    print('Compression ratio: {}'.format(round(compress_ratio, 3)))
    # print('Decoded message: {}'.format(decoded_message))


def get_message():
    message = input('Enter a message to be encoded: ')
    if len(message) == 0:
        return 'hot-diggity-dog'
    return message


def make_tree(freqs):
    tree = []
    while len(freqs) > 1:
        tree = [freqs[len(freqs) - 2][0], freqs[len(freqs) - 1][0]]
        freq = freqs[len(freqs) - 2][1] + freqs[len(freqs) - 1][1]
        freqs = freqs[:-2]
        freqs.append((tree, freq))
        freqs = sort_freqs(freqs)

    return tree


def print_tree(tree):
    pass


def sort_freqs(L):
    for i in range(1, len(L)):
        j = i - 1
        key = L[i]
        while (L[j][1] > key[1]) and (j >= 0):
            L[j + 1] = L[j]
            j -= 1
        L[j + 1] = key
    L.reverse()
    return L


def get_frequency(message: str):
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


def calc_entropy(freqs):
    entropy = 0
    for key, freq in freqs:
        entropy += freq * math.log2(freq)
    return -entropy


def calc_ave_info(freqs, codebook):
    info = 0
    for key, freq in freqs:
        info += freq * len(codebook[key])
    return info


def make_codebook(tree):
    codebook = {}

    left_branch = tree[0]
    if type(left_branch) is str:
        codebook[left_branch] = '0'
    else:
        sub_tree = make_codebook(left_branch)
        for key in sub_tree.keys():
            sub_tree[key] = '0' + sub_tree[key]
        codebook.update(sub_tree)

    right_branch = tree[1]
    if type(right_branch) is str:
        codebook[right_branch] = '1'
    else:
        sub_tree = make_codebook(right_branch)
        for key in sub_tree.keys():
            sub_tree[key] = '1' + sub_tree[key]
        codebook.update(sub_tree)

    return codebook


def encode_message(message: str, codebook):
    encoded_message = ''
    for let in message:
        encoded_message += codebook[let]
    return encoded_message


def decode_message(encoded_message: str, codebook):
    reverse_codebook = flip_dict(codebook)

    decoded_message = ''
    tally = ''
    for i in encoded_message:
        tally += i
        if tally in reverse_codebook:
            decoded_message += reverse_codebook[tally]
            tally = ''
    return decoded_message


def flip_dict(dictionary):
    flipped = {}
    for key, val in dictionary.items():
        flipped[val] = key
    return flipped


def printable_freqs(freqs):
    return [(key, round(freq, 5)) for key, freq in freqs]


if __name__ == '__main__':
    main()
