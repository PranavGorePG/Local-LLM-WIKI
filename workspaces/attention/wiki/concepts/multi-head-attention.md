---
title: Multi-Head Attention
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- self-attention
- attention-mechanism
- transformer
tags:
- attention
- neural networks
- deep learning
confidence: high
updated: '2023-10-27'
---

Multi-Head Attention is an extension of the attention mechanism that allows a model to jointly attend to information from different representation subspaces at different positions. Instead of performing a single attention function, multi-head attention linearly projects the queries, keys, and values multiple times with different, learned projections. Attention is then applied in parallel to these projected versions, and the outputs are concatenated and projected again.

This approach, proposed in the "Attention Is All You Need" paper, enhances the model's ability to capture diverse types of relationships within the data. It prevents the averaging effect of a single attention head, which can inhibit learning. The Transformer model utilizes multi-head attention in three distinct ways: in encoder-decoder attention, in the encoder's self-attention layers, and in the decoder's masked self-attention layers. The paper found that using 8 parallel attention heads (h=8) with specific dimensionality for keys and values (dk=dv=64) yielded optimal results.
