import torch
import torch.nn as nn

from Janex import *

import numpy as np
import nltk
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()

import numpy as np
import random
import json

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader


def stem(word):
    return stemmer.stem(word.lower())

def bag_of_words(tokenized_sentence, words):
    # stem each word
    sentence_words = [stem(word) for word in tokenized_sentence]
    # initialize bag with 0 for each word
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in sentence_words:
            bag[idx] = 1

    return bag

class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size)
        self.l2 = nn.Linear(hidden_size, hidden_size)
        self.l3 = nn.Linear(hidden_size, num_classes)
        self.relu = nn.ReLU()

    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)
        # no activation and no softmax at the end
        return out

class ChatDataset(Dataset):

    def __init__(self, X_train, y_train):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = y_train

    # support indexing such that dataset[i] can be used to get i-th sample
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    # we can call len(dataset) to return the size
    def __len__(self):
        return self.n_samples

class JanexPT:
    def __init__(self, intents_file_path, thesaurus_file_path, UIName):
        self.intents_file_path = intents_file_path
        self.thesaurus_file_path = thesaurus_file_path
        self.FILE = "data.pth"
        self.data = torch.load(self.FILE)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.input_size = self.data["input_size"]
        self.hidden_size = self.data["hidden_size"]
        self.output_size = self.data["output_size"]
        self.all_words = self.data['all_words']
        self.tags = self.data['tags']
        self.model_state = self.data["model_state"]
        self.model = NeuralNet(self.input_size, self.hidden_size, self.output_size).to(self.device)
        self.UIName = UIName
        self.IntentMatcher = IntentMatcher(intents_file_path, thesaurus_file_path)
        self.intents = self.IntentMatcher.train()

    def SayToAI(self, input_string, user):
        self.model.load_state_dict(self.model_state)
        self.model.eval()
        sentence = input_string

        sentence = self.IntentMatcher.tokenize(sentence)

        X = bag_of_words(sentence, self.all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(self.device)

        output = self.model(X)
        _, predicted = torch.max(output, dim=1)

        tag = self.tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        probs = probs[0][predicted.item()]

        for intent in self.intents['intents']:
            if tag == intent["tag"]:
                print(tag)
                BestResponse = self.IntentMatcher.response_compare(input_string, intent)
                return BestResponse

    def trainpt(self):
        try:
            open("train.py", "r")
            os.system("python3 train.py")
        except:
            print("Janex-PyTorch: Train program not detected, downloading from Github.")
            os.system(f"curl -o train.py https://raw.githubusercontent.com/Cipher58/Janex-PyTorch/main/Stock/train.py")
            os.system("python3 train.py")