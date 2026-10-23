import tiktoken

encoder = tiktoken.encoding_for_model('gpt-4o')

print("print vocab size:", encoder.n_vocab) #200019

text = "The cat sat on the mat"

tokens =  encoder.encode(text)


print ("tokens:", tokens) # [464, 257, 293, 286, 257, 286]

my_tokens = [976, 9059, 10139, 402, 290, 2450]

decoded = encoder.decode(my_tokens)

print ("Decoded Text:", decoded)