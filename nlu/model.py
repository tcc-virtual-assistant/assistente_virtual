import yaml
import numpy as np
import tensorflow
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding
from tensorflow.keras.utils import to_categorical


data = yaml.safe_load(open('nlu\\train.yml', 'r', encoding='utf-8').read())

inputs, outputs = [], []

for command  in data['commands']:
    inputs.append(command['input'].lower())
    outputs.append(f"{command['entity']}\{command['action']}")

# Processar texto: palavras, caracteres, bytes, sub-palavras


max_seq = max([len(bytes(x.encode('utf-8'))) for x in inputs])

print('Maior seq: ', max_seq)

# Criar dataset one-hot (número de exemplos, tamanho da seq, num caracteres)
# Criar dataset disperso (número de exemplos, tamanho da seq)

# Input Data one-hot encoding
input_data = np.zeros((len(inputs), max_seq, 256), dtype='float32')
for i, inp in enumerate(inputs):
    for k, ch in enumerate(bytes(inp.encode('utf-8'))):
        input_data[i, k, int(ch)] = 1.0

#input Data Sparse
'''
input_data = np.zeros((len(inputs), max_seq, len(chars)), dtype='int32')

for i, input in enumerate(inputs):
    for k, ch in enumerate(input):
        input_data[i, k] = chr2idx[ch]
'''

#Output Data
labels = set(outputs)

label2idx = {}
idx2label = {}

for idx, label in enumerate(labels):
    label2idx[label] = idx
    idx2label[idx] = label

output_data = []

for output in outputs:
    output_data.append(label2idx[output])

output_data = to_categorical(output_data, len(output_data))

print(output_data[0])

model = Sequential()
model.add(LSTM(128))
model.add(Dense(len(output_data), activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['acc'])
model.fit(input_data, output_data, epochs=16)

# Criar o dataset
