## Transformer model
## Is the model that needs to be made

import torch 
import torch.nn as nn
import math

#Setup and Run the Enviromet
# conda create -n env_pytorch python=3.10
# conda activate env_pytorch

# The Concept of a Transformer Model is that it utilizes two embeddings to do computations:
# 
# They use the embedding to assign values to any input
# The use an additional embedding  to assign values position as well
# This creates a double embedding system per word which allows context to be added in
# 

# The following embedding is for the words - vector or list of size 512
class InputEmbeddings(nn.Module):

    def __init__(self, d_model: int, vocab_size: int):  # the dimensions of the vector && how many words are in the vocabulary 
        super().__init__()
        self.d_model =  d_model
        self.vocab_size = vocab_size
        self.embedding = nn.Emdedding(vocab_size, d_model) ## creates the embedding now which is the mapping of vector(size 512) to number 

    def forward(self, x):   #as per the paper we multiply the layers of embdedding with the sqrt of the d_model
        return self.embedding(x) * math.sqrt(self.d_model)

# Positonal Encoding, Emdbedding is the same size of 512 for the vector
class PositionalEncoding(nn.Module): 
    
    ## the dimensions of the vector && how many words are in a sentence allowed &&  dropout is to prevent Overfitting a model so it doesnt take too much noise
    def __init__(self, d_model: int, seq_len: int, dropout: float) -> None: 
        super().__init__()
        self.d_model = d_model
        self.seq_len = seq_len
        self.dropout = nn.Dropout(dropout)
    
        # Create a matrix of shape (seq_len, d_model) this is essentially to match the 512 vectors and the sequence length or how many words there are placed
        pe = torch.zeros (seq_len, d_model)
        # create the vectors for the sequence length (Vector of Shape) so from seq_length to 1
        # this is the cosine and sin mathematical equations
        position = torch.arrange(0, seq_len, dtype = torch.flight).unsqueeze(1) 



age = 3
print(f'tim is the age: {age}')