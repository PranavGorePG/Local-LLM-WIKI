---
title: Value
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- scaled-dot-product-attention
- query
- key
- attention-mechanism
tags:
- attention
- deep learning
confidence: high
updated: '2023-10-27'
---

In attention mechanisms, 'values' represent the actual information content that is retrieved. Each value is associated with a key, and it is these values that are aggregated, weighted by the attention scores, to produce the final output of the attention layer. In Scaled Dot-Product Attention, the values have a dimension of $d_v$. When a query matches a key (or set of keys), the corresponding value(s) are weighted and combined to form the output representation. The values are what the attention mechanism ultimately learns to extract and combine based on the query-key interactions.
