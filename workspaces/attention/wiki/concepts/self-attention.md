---
title: Self-Attention
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- multi-head-attention
- attention-mechanism
- transformer
- positional-encoding
- computational-complexity
- gradient-flow
tags:
- attention
- neural networks
- deep learning
- transformer
confidence: high
updated: '2023-10-27'
---

Self-attention, also known as intra-attention, is an attention mechanism that relates different positions of a single sequence to compute a representation of that sequence. It allows the model to weigh the importance of different words (or tokens) within the same sequence when processing each word. This enables the model to capture dependencies regardless of their distance in the sequence, which is a significant advantage over traditional recurrent models where long-range dependencies can be hard to learn.

The "Attention Is All You Need" paper heavily features self-attention, proposing it as the core component of the Transformer architecture. In the Transformer, self-attention layers are used in both the encoder and decoder. The encoder uses self-attention to allow each position to attend to all positions in the previous layer of the encoder. Similarly, the decoder uses masked self-attention to attend to positions up to and including the current position, preserving the auto-regressive property.
