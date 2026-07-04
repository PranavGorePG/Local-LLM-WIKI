---
title: ReLU Activation
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- position-wise-feed-forward-networks
- transformer
tags:
- activation function
- neural networks
- feed-forward
---

ReLU (Rectified Linear Unit) is a common activation function used in neural networks, particularly within feed-forward layers. It introduces non-linearity into the model, enabling it to learn complex patterns.

## Definition
The ReLU activation function is mathematically defined as f(x) = max(0, x). This means that for any input value, if the value is positive, it is passed through unchanged; if it is negative, it is replaced by zero. This simple operation is computationally efficient and has been found to be effective in training deep neural networks.

## Role in Context
In the Transformer architecture, ReLU activation is used within the position-wise feed-forward networks. Each layer in both the encoder and decoder contains such a network, which consists of two linear transformations with a ReLU activation in between. This allows the model to process information at each position independently and learn feature representations that are crucial for sequence transduction tasks.
