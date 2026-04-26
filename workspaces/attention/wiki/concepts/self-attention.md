---
title: Self-Attention
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- Attention Mechanism
- Transformer Architecture
- Multi-Head Attention
tags:
- neural networks
- deep learning
- sequence transduction
---

[[Self-Attention]], also known as intra-attention, is a specific type of [[Attention Mechanism]] that relates different positions of a single sequence to compute a representation of that same sequence. Unlike traditional attention mechanisms that might attend from a decoder to an encoder, self-attention allows a position in a sequence to "look" at all other positions in the *same* sequence to gather context. In the [[Transformer Architecture]], self-attention layers are crucial components of both the encoder and decoder stacks. Encoder Self-Attention: Each position in the encoder can attend to all positions in the previous layer of the encoder. Decoder Self-Attention: Each position in the decoder can attend to all positions in the decoder up to and including that position. Masking is applied to prevent attending to future positions, preserving the auto-regressive property. This mechanism helps in capturing long-range dependencies within the sequence efficiently.
