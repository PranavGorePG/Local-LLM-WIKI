---
title: Weighted sum
type: mathematical operation
source_documents:
- self_attention_and_rnns.pdf
related_pages: []
tags:
- mathematics
- linear algebra
---

A [[weighted sum]] is a calculation where elements are multiplied by predefined weights before being summed. In [[Self-attention]], the final output for a token is computed as a weighted sum of all [[Value (V)|Value]] vectors in the sequence, where the weights are determined by the [[attention score]]s (after softmax normalization).
