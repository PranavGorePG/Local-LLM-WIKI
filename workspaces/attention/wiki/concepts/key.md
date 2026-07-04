---
title: Key
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- scaled-dot-product-attention
- query
- value
- attention-mechanism
tags:
- attention
- deep learning
confidence: high
updated: '2023-10-27'
---

In attention mechanisms, a 'key' is paired with a 'value' and is used to determine the attention weights. It represents a descriptor for the information contained in the associated value. During the attention calculation, the 'query' is compared with each 'key' to compute a compatibility score. In Scaled Dot-Product Attention, these keys have a dimension of $d_k$. The set of keys, along with their corresponding values, forms the memory or context that the query can attend to. The comparison between the query and keys is fundamental to how the attention mechanism focuses on relevant parts of the input.
