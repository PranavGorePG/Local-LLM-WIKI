---
title: Quadratic complexity
type: computational complexity
source_documents:
- self_attention_and_rnns.pdf
related_pages: []
tags:
- complexity
- computation
---

[[Quadratic complexity]] refers to a computational or space complexity that scales with the square of the input size. In [[Self-attention]], the computation of attention scores involves comparing every token pair, resulting in a quadratic complexity ($O(n^2)$) with respect to the [[sequence length]] ($n$). This can make self-attention computationally expensive for very long sequences.
