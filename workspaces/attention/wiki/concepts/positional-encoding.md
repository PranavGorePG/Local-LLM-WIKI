---
title: Positional Encoding
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- transformer
- self-attention
tags:
- transformer
- neural networks
- embeddings
confidence: high
updated: '2023-10-27'
---

Positional Encoding is a mechanism used in sequence processing models, particularly in architectures like the Transformer that do not inherently process data sequentially (e.g., eschewing recurrence and convolutions). Since the model needs to understand the order of tokens in a sequence, positional encodings are added to the input embeddings to inject information about the relative or absolute position of each token.

In the "Attention Is All You Need" paper, a specific sinusoidal function is proposed for positional encoding. The formula uses sine and cosine functions of different frequencies based on the position and dimension of the encoding. This choice was motivated by the hypothesis that it would allow the model to easily learn to attend by relative positions. The paper also experimented with learned positional embeddings, finding similar performance, but opted for the sinusoidal version due to its potential to extrapolate to sequence lengths longer than those seen during training.
