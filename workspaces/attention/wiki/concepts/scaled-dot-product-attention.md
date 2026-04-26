---
title: Scaled Dot-Product Attention
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- Attention Mechanism
- Multi-Head Attention
- Transformer Architecture
tags:
- neural networks
- deep learning
- sequence transduction
---

[[Scaled Dot-Product Attention]] is the specific attention function employed within the [[Transformer Architecture]]. It is a more efficient variant of dot-product (multiplicative) attention. Mechanism: 1. Inputs consist of queries (Q) and keys (K) of dimension `dk`, and values (V) of dimension `dv`. 2. Dot products are computed between the query and all keys. 3. Each result is divided by `√dk` (the scaling factor). 4. A softmax function is applied to these scaled dot products to obtain the weights. 5. The output is a weighted sum of the values (V). Formula: `Attention(Q, K, V) = softmax(QKT / √dk)V` Comparison to Additive Attention: While theoretically similar in complexity, dot-product attention is faster and more space-efficient in practice due to optimized matrix multiplication. The scaling factor `1/√dk` is crucial for larger values of `dk` to counteract the large magnitudes of dot products, which can push the softmax function into regions with extremely small gradients.
