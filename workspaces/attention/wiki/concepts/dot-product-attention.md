---
title: Dot-Product Attention
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- attention-mechanism
- scaled-dot-product-attention
- additive-attention
tags:
- attention
- deep learning
confidence: high
updated: '2023-10-27'
---

Dot-Product Attention is a type of attention mechanism that computes the compatibility between a query and keys using the dot product of their vectors. This is a fundamental component that is often used in sequence-to-sequence models. In the paper "Attention Is All You Need," this method is referred to as Scaled Dot-Product Attention when a scaling factor of $1/{\sqrt{d_k}}$ is applied, where $d_k$ is the dimension of the keys. The scaling is introduced to counteract the issue where large dot products can push the softmax function into regions with very small gradients. While similar to additive attention in theoretical complexity, dot-product attention is generally more computationally efficient in practice due to optimized matrix multiplication routines. It is a key building block for the Transformer's self-attention and encoder-decoder attention mechanisms.
