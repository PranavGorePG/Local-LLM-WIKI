---
title: Positional Representation
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- transformer
- positional-encoding
- learned-positional-embeddings
tags:
- positional encoding
- transformer
---

Positional representation refers to the method by which the order of tokens in a sequence is encoded and supplied to a model, especially when the model architecture itself, like the Transformer, does not inherently process sequential information through recurrence or convolution.

## Overview
Since the Transformer model dispenses with recurrence and convolutions, it requires a mechanism to inject information about the relative or absolute positions of tokens within a sequence. This is achieved by adding "positional encodings" to the input embeddings. These encodings have the same dimension as the embeddings, allowing them to be summed. The choice of positional encoding can influence the model's ability to learn dependencies based on token order.

## Key Properties
Two primary approaches to positional representation are discussed:
- **Sinusoidal Positional Encodings**: These use sine and cosine functions of different frequencies, applied to each dimension of the positional encoding. The hypothesis is that this formulation allows the model to more easily learn to attend by relative positions, as PE(pos+k) can be represented as a linear function of PE(pos) for any fixed offset k.
- **Learned Positional Embeddings**: An alternative approach where positional embeddings are learned during training, similar to learned word embeddings. Experiments show that this method yields results comparable to sinusoidal encodings.

## Role in Context
Positional representation is critical for models like the Transformer that process sequences in a non-sequential manner. It allows the model to understand the grammatical structure and meaning derived from word order, which is fundamental to natural language processing tasks.
