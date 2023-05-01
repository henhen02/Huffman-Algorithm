import timeit

class Node:
    def __init__(self, prob, symbol, left=None, right=None):
        self.prob = prob
        self.symbol = symbol
        self.left = left
        self.right = right
        self.code = ''

codes = dict()

def Calculate_Codes(node, val=''):
    # huffman code for current node
    newVal = val + str(node.code)

    if(node.left):
        Calculate_Codes(node.left, newVal)
    if(node.right):
        Calculate_Codes(node.right, newVal)

    if(not node.left and not node.right):
        codes[node.symbol] = newVal
         
    return codes        

# Kalkulasi frekuensi kemunculan karakter
def Calculate_Probability(data):
    symbols = dict()
    for element in data:
        if symbols.get(element) == None:
            symbols[element] = 1
        else: 
            symbols[element] += 1     
    return symbols

# Encoding teks
def Output_Encoded(data, coding):
    encoding_output = []
    for c in data:
        encoding_output.append(coding[c])
        
    string = ''.join([str(item) for item in encoding_output])
    return string

# Rasio perbandingan persentase
def Ratio_Calc(before, after):
    return (1-after/before)*100

# Kalkulasi ukuran teks (satuan bit)
def Total_Gain(data, coding):
    # Rumus (panjang data * 8)
    before_compression = len(data) * 8
    after_compression = 0
    symbols = coding.keys()
    for symbol in symbols:
        count = data.count(symbol)
        # Rumus (panjang karakter * 8)
        after_compression += count * len(coding[symbol]) #calculate how many bit is required for that symbol in total
    print("Space usage before compression (in bits):", before_compression)    
    print("Space usage after compression (in bits):",  after_compression)  
    print("Ratio:", Ratio_Calc(before_compression, after_compression), "%")        

# Encoding
def Huffman_Encoding(data):
    # Memulai runtime
    start = timeit.default_timer()

    symbol_with_probs = Calculate_Probability(data)
    symbols = symbol_with_probs.keys()
    probabilities = symbol_with_probs.values()
    print("symbols: ", symbols)
    print("probabilities: ", probabilities)
    
    nodes = []
    
    for symbol in symbols:
        nodes.append(Node(symbol_with_probs.get(symbol), symbol))
    
    while len(nodes) > 1:
        nodes = sorted(nodes, key=lambda x: x.prob)
        # Cabang pohon
        # Kiri = 1, kanan = 0 
        left = nodes[1]
        right = nodes[0]
    
        left.code = 0
        right.code = 1

        newNode = Node(left.prob+right.prob, left.symbol+right.symbol, left, right)
    
        nodes.remove(left)
        nodes.remove(right)
        nodes.append(newNode)
            
    huffman_encoding = Calculate_Codes(nodes[0])
    stop = timeit.default_timer()
    encode_runtime = stop - start
    print("symbols with codes", huffman_encoding)
    Total_Gain(data, huffman_encoding)
    encoded_output = Output_Encoded(data,huffman_encoding)
    output = open('EncodeBinaryFiles/test4.txt', 'w')
    output.write(encoded_output)
    return encoded_output, nodes[0], encode_runtime 
    
# Decoding
def Huffman_Decoding(encoded_data, huffman_tree):
    # Memulai runtime
    start = timeit.default_timer()

    tree_head = huffman_tree
    decoded_output = []
    for x in encoded_data:
        if x == '1':
            huffman_tree = huffman_tree.right   
        elif x == '0':
            huffman_tree = huffman_tree.left
        try:
            if huffman_tree.left.symbol == None and huffman_tree.right.symbol == None:
                pass
        except AttributeError:
            decoded_output.append(huffman_tree.symbol)
            huffman_tree = tree_head
        
    string = ''.join([str(item) for item in decoded_output])
    stop = timeit.default_timer()
    decode_runtime = stop - start
    return string, decode_runtime        

teks = open("test4.txt")
outputBinary = open("BinaryFiles/test4.txt", 'w')
data = teks.read()

# Convert file asli kedalam biner
data_bin = " ".join(format(ord(x), 'b') for x in data)
outputBinary.write(data_bin)

encoding, tree, encode_runtime = Huffman_Encoding(data)
decoding, decode_runtime = Huffman_Decoding(encoding, tree)

print(f'String: {data}')
print(f'Encode Output:\n{encoding}')
print(f'Decode Output:\n{decoding}')
print(f'Encode Runtime: {encode_runtime}\nDecode Runtime: {decode_runtime}')
teks.close()