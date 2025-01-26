## decoder-only Transformer model
## Is the model that needs to be made

import torch 
import torch.nn as nn
import math


# The Concept of a Transformer Model is that it utilizes two embeddings to do computations:
# 
# They use the embedding to assign values to any input
# The use an additional embedding  to assign values position as well
# This creates a double embedding system per word which allows context to be added in
# 

# The following embedding is for the words
class InputEmbeddings(nn.Module):

    def __init__(self, d_model: int, vocab_size: int):
        super().__init__()
        self.d_model =  d_model
        self.vocab_size = vocab_size
        self.embedding = nn.Emdedding(vocab_size, d_model)
        print("Test")

    def forward(self, x):
        return self.embedding(x) * math.sqrt(self.d_model)


age = 3
print(f'tim is the age: {age}')