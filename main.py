import torch 
import torch.nn as nn
import math

## Transformer model
## Is the model that needs to be made

# For Apple Use
# CUDA is not supported on Mac and supports Nvidia
# Therefore will need to use Apples: Metal Performance Model (MPS)
# conda activate env_pytorch
# conda install pytorch torchvision torchaudio -c pytorch-nightly
# /Users/{user-name}/anaconda3/envs/env_pytorch/bin/python /Users/{user-name}/Desktop/Inter.i/main.py
# #


#Setup and Run the Enviromet
# conda create -n env_pytorch python=3.10
# conda activate env_pytorch

# The Concept of a Transformer Model is that it utilizes two embeddings to do computations:
# 
# They use the embedding to assign values to any input
# The use an additional embedding  to assign values position as well
# This creates a double embedding system per word which allows context to be added in
# 

# INPUTS ONLY
# The following embedding is for the words - vector or list of size 512  ---------- can do 256 if machine cannot handle it
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
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0)/d_model))
        #Positioning Embedding with Sin and Cos formula, cosine is for odd position and sin is for even postions
        # Apply Sin   ------- Even
        # START STOP STEP 
        pe[:, 0::2]= torch.sin(position* div_term)
        # Apply Cos  -------- Odd
        # START STOP STEP 
        pe[:, 1::2]= torch.cos(position* div_term)

        pe.unsqueeze(0) # (1, seq_len, d_model)

        #Save the tensor with the Buffer
        self.register_buffer('pe', pe)
    
    def forward(self, x):
        x = x + (self.pe[:, :x.shape[1], :]).requires_grad_(False)
        return self.dropout(x)



print(torch.__version__)  # Check PyTorch version
print(torch.backends.mps.is_available())  # Check if MPS is available
age = 3
print(f'tim is the age: {age}')