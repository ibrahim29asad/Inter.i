import torch 
import torch.nn as nn
import math

## Transformer model
## Is the model that needs to be made

# For Apple Use
# CUDA is not supported on Mac and supports Nvidia
# Therefore will need to use Apples: Metal Performance Model (MPS)
# conda activate env_pytorch
# conda install pytorch torchvision torchaudio -c pytorch
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

        #Creates a batch of items or sentances for practicle use since you will have multiple sentances 
        pe.unsqueeze(0) # (1, seq_len, d_model)

        #Save the tensor with the Buffer and along with the sate of the model
        self.register_buffer('pe', pe)
    

    def forward(self, x):
        #Postional encoding for every word in the sentance
        x = x + (self.pe[:, :x.shape[1], :]).requires_grad_(False) # Model doesnt need to keep the position embedding so will not need to be saved after the state is done
        return self.dropout(x)

#Layer Normalization 
# add and Norm 
# 

#Equation for normailization 
# <x j = gamm/beta
#gamma= xj - Uj
#alpha = ((Oj)^2   +    e )^.5 , e is epsilon
class LayerNormalizaiton(nn.Module):

# need epsilon since we need to make sure the denominatior isnt too small and 
# allows for numerical stability as we have a limit on the actual funciton 

    def __init__(self, eps: float = 10**-6) -> None:
        super().__init__()
        self.eps = eps
        self.alpha = nn.Parameter(torch.ones(1)) # Multiply - gamma
        self.bias = nn.Parameter(torch.zeros(1)) # added - beta


    def forward(self, x):
        mean = x.mean(dim = -1, keepdim=True)
        std = x.std(dim = -1, keepdim=True)
        return self.alpha * (x - mean) / (std + self.eps) + self.bias


class FeedForwardBlock(nn.Module):

    def __init__(self, d_model: int, d_ff: int, dropout: float) -> None:
        super().__init__()
        self.linear_1 = nn.Linear(d_model, d_ff) # W1 and B1 - it already defines the bias as true
        self.dropout = nn.Dropout(dropout)
        self.linear_2 = nn.Linear(d_ff, d_model) # W2 and B2

    def forward(self, x):
        # (Batch, Seq_Len, d_model) --> (Batch, Seq_Len, d_ff) --> (Batch, Seq_Len, d_model)
        return self.linear_2(self.dropout(self.dropout(torch.relu(self.linear_1(x)))))

#Multi-Head Attention
# 3 inputs Query, Key, Value  so it takes 1 input turn it into 3 inputs which then will get multiplied to turn into multiple heads "blocks"
# then turning into the overal d_models heads and uses all the inputs heads and will turn into my output
class MultiHeadAttentionBlock(nn.Module):

    def __init__(self, d_model: int, h: int, dropout: float) -> None:
        super().__init__()
        self.d_model = d_model
        self.h = h
        assert d_model % h == 0, "d_model is not divisible by h" # this creates the heads for each input so dk

        self.d_k = d_model // h
        self.w_q = nn.Linear(d_model, d_model) #Wq
        self.w_k = nn.Linear(d_model, d_model) #Wk
        self.w_v = nn.Linear(d_model, d_model) #Wv

        self.w_o = nn.Linear(d_model, d_model) #Wo
        self.dropout = nn.Dropout(dropout) 

    @staticmethod
    def attention(query, key, value, mask, dropout: nn.Dropout):
        d_k = query.shape[-1]
        
        #matrix multiplication
        attention_scores = (query @ key.transpose(-2, -1)) / math.sqrt(d_k)
        if mask is not None:
            # Write a very low value (indicating -inf) to the positions where mask == 0
            attention_scores.masked_fill_(mask == 0, -1e9)
        attention_scores = attention_scores.softmax(dim=-1) # (batch, h, seq_len, seq_len) # Apply softmax
        if dropout is not None:
            attention_scores = dropout(attention_scores)
        # (batch, h, seq_len, seq_len) --> (batch, h, seq_len, d_k)
        # return attention scores which can be used for visualization
        return (attention_scores @ value), attention_scores

    
    def forward(self, q, k, v, mask):
        query = self.w_q(q) # (Batch, Seq_len, d_model) --> (Batch, Seq_len, d_model)
        key = self.w_k(k)   # (Batch, Seq_len, d_model) --> (Batch, Seq_len, d_model)
        value = self.w_v(v) # (Batch, Seq_len, d_model) --> (Batch, Seq_len, d_model)
        
        # (Batch, Seq_len, d_model) --> (Batch, Seq_len, h, d_k) --> (Batch, h, seq_len, d_k)
        query = query.view(query.shape[0], query.shape[1], self.h, self.d_k).transpose(1, 2)

        key = key.view(key.shape[0], key.shape[1], self.h, self.d_k).transpose(1, 2)
        value = value.view(value.shape[0], value.shape[1], self.h, self.d_k).transpose(1, 2)

        #Calculates the Attention
        x, self.attention_scores = MultiHeadAttentionBlock.attention(query, key, value, mask, self.dropout)
        
        # Combine all the heads together
        # (batch, h, seq_len, d_k) --> (batch, seq_len, h, d_k) --> (batch, seq_len, d_model)
        x = x.transpose(1, 2).contiguous().view(x.shape[0], -1, self.h * self.d_k)

        # Multiply by Wo
        # (batch, seq_len, d_model) --> (batch, seq_len, d_model)  
        return self.w_o(x)




age = 3
print(f'tim is the age: {age}')