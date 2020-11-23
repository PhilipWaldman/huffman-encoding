# Huffman Encoding
Creates a Huffman encoding for the given message.

## What does the program do?
1. Get the message to encode from the user. If no message is provided, `hot-diggity-dog` will be used.
2. A frequency table is made with the frequencies of each character. This list is sorted in order of most to least common.
3. The Huffman encoding tree is made. It works by...
4. A code book is made from the tree. The code book is a dictionary with the character as a key and the bitstring to encode it into as the value. This makes encoding and decoding easier.
5. The message is encoded using the code book. Every character is replaced with its corresponding encoding.
6. The encoded message is decoded again using the code book.
7. The entropy of the message is calculated. For the list of frequencies `F = f_1, ..., f_n`, the entropy is `H(F) = - \sum_{i=0}^{n} (f_i * log2(f_i))`. This is the theoretical average amount of information in the message.
8. The actual average amount of information is calculated taking the sum of the length of the encoding of each character multiplied by its frequency.
9. The compression ratio is calculated by dividing the length of the input message by the length of the encoded message.