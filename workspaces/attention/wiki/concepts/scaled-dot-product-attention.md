---
title: Scaled Dot-Product Attention
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- attention-mechanism
- query
- key
- value
- softmax
tags:
- attention
- deep learning
- model architecture
confidence: high
updated: '2023-10-27'
---

Scaled Dot-Product Attention is a specific type of attention mechanism used in the Transformer model. It computes the attention output as a weighted sum of values, where the weights are determined by the compatibility between a query and a set of keys. The process involves taking the dot product of the query with all keys, scaling the result by the square root of the key dimension (${\sqrt{d_k}}$), and then applying a softmax function to obtain the attention weights. These weights are subsequently used to compute a weighted average of the values. The formula for Scaled Dot-Product Attention is: ${\text{Attention}}(Q, K, V) = \text{softmax}(\frac{QK^T}{\sqrt{d_k}})V$. The scaling factor $1/{\sqrt{d_k}}$ is crucial for preventing the dot products from becoming too large, which could push the softmax function into regions with very small gradients, thereby hindering learning. This mechanism is a core component of the Transformer, used in both self-attention and encoder-decoder attention layers.
