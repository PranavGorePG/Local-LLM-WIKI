---
title: Additive Attention
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- attention-mechanism
- scaled-dot-product-attention
tags:
- attention
- deep learning
confidence: high
updated: '2023-10-27'
---

Additive Attention is an alternative mechanism for computing the compatibility function between a query and keys in an attention system. Unlike dot-product attention, which directly computes the similarity as a dot product, additive attention uses a feed-forward network with a single hidden layer to compute this compatibility. Specifically, it concatenates the query and key, passes them through a feed-forward network with a tanh activation, and then projects the result to a scalar value. While both additive and dot-product attention have similar theoretical complexities, dot-product attention is often preferred in practice due to its efficiency, especially when implemented with optimized matrix multiplication. The paper notes that for small dimensions of $d_k$, the two mechanisms perform similarly, but additive attention can outperform dot product attention without scaling for larger values of $d_k$, as the dot products can become very large and push the softmax into low-gradient regions.
