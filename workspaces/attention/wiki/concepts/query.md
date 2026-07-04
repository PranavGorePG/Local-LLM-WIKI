---
title: Query
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- scaled-dot-product-attention
- key
- value
- attention-mechanism
tags:
- attention
- deep learning
confidence: high
updated: '2023-10-27'
---

In the context of attention mechanisms, a 'query' represents a request for information. It is a vector that is compared against a set of 'keys' to determine how much attention should be paid to corresponding 'values'. In Scaled Dot-Product Attention, the query vector is used to calculate similarity scores with each key vector. These scores, after scaling and applying a softmax function, become the weights that determine how the 'values' are aggregated to produce the attention output. The query's dimension is denoted as $d_k$.
