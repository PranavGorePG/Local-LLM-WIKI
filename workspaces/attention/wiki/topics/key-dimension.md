---
title: Key dimension
type: mathematical property
source_documents:
- self_attention_and_rnns.pdf
related_pages: []
tags:
- self-attention
- mathematics
---

The [[key dimension]] is a hyperparameter in [[Self-attention]] mechanisms that defines the dimensionality of the [[Key (K)|Key]] vectors (and often the [[Query (Q)|Query]] vectors as well). Scaling the [[dot product]] of Query and Key vectors by the square root of the key dimension is a common practice to stabilize gradients during training.
