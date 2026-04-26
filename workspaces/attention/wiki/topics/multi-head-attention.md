---
title: Multi-Head Attention
type: Concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- Self-Attention
- Attention Mechanism
- Transformer Architecture
- Scaled Dot-Product Attention
- Encoder-Decoder Architecture
tags:
- Attention
- Neural Networks
- Deep Learning
---

[[Multi-Head Attention]] is an extension of the [[Self-Attention]] mechanism, crucial for the [[Transformer Architecture]] and detailed in "[[Attention Is All You Need]]" (Vaswani et al., 2017). Instead of performing a single attention function, it projects the queries, keys, and values multiple times (h times) with different learned linear projections into lower-dimensional spaces. On each of these projected versions, the attention function is performed in parallel, yielding multiple "attention heads." The outputs from these heads are then concatenated and projected once again to form the final result.This parallel processing allows the model to jointly attend to information from different representation subspaces at different positions. This is particularly beneficial because a single attention head, by averaging, might inhibit the model's ability to capture diverse aspects of relationships. For instance, some heads might focus on local dependencies, while others capture long-range semantic or syntactic relationships. In the Transformer model, [[Multi-Head Attention]] is used in three ways: in encoder-decoder attention (queries from decoder, keys/values from encoder), in encoder self-attention, and in masked decoder self-attention (to prevent attending to future positions).
