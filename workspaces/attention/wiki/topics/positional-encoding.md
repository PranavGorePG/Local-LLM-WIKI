---
title: Positional Encoding
type: Concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- Transformer Architecture
- Attention Mechanism
tags:
- Neural Networks
- Deep Learning
- NLP
---

[[Positional Encoding]] is a technique used in the [[Transformer Architecture]] to inject information about the relative or absolute position of tokens in a sequence. Since the Transformer model contains no recurrence or convolution, it inherently lacks a mechanism to process sequence order. Positional encodings, which have the same dimension as the input embeddings, are added to the embeddings at the input of the encoder and decoder stacks. This allows the model to learn to make use of the order of the sequence. The original Transformer paper ("[[Attention Is All You Need]]" by Vaswani et al., 2017) proposes using sine and cosine functions of different frequencies for fixed positional encodings. This formulation is hypothesized to allow the model to easily learn to attend by relative positions and potentially extrapolate to longer sequence lengths. Learned positional embeddings are an alternative, but fixed sinusoidal encodings yielded nearly identical results in the original work.
