---
title: Scaled Dot-Product Attention
type: Concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- Attention Mechanism
- Multi-Head Attention
- Transformer Architecture
tags:
- Attention
- Neural Networks
- Deep Learning
---

[[Scaled Dot-Product Attention]] is a fundamental component of the [[Transformer Architecture]] and a specific implementation of the [[Attention Mechanism]], as described in "[[Attention Is All You Need]]" (Vaswani et al., 2017). It takes a query (Q) and a set of key-value pairs (K, V) as input. The attention weights are computed by taking the dot product of the query with all keys, dividing each by the square root of the dimension of the keys (√dk), and then applying a softmax function to obtain the weights on the values. This scaling factor (√dk) is crucial because for large values of dk, the dot products can grow large in magnitude, pushing the softmax function into regions with extremely small gradients, which hinders learning. The output is a weighted sum of the values. This method is computationally efficient, leveraging highly optimized matrix multiplication. It forms the basis for [[Multi-Head Attention]].
