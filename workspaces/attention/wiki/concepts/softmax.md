---
title: Softmax
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages: []
tags:
- mathematics
- machine learning
confidence: high
updated: '2023-10-27'
---

The softmax function is a mathematical function that converts a vector of real numbers into a probability distribution. It is commonly used in the output layer of a neural network for classification tasks, where it outputs probabilities for each class. In the context of attention mechanisms, softmax is applied to the scaled dot products of queries and keys to obtain attention weights. These weights are then used to compute a weighted sum of the values. The formula for softmax applied to a set of scores $z_i$ is: $P(i) = \frac{e^{z_i}}{\sum_{j} e^{z_j}}$. In the Transformer model, the softmax function is used in the Scaled Dot-Product Attention to determine the weights assigned to values, based on the compatibility between queries and keys. It is also used in the final layer to convert the decoder's output vectors into probabilities for the next token.
