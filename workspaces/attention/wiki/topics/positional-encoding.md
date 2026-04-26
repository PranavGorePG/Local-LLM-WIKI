---
title: Positional encoding
type: data representation
source_documents:
- self_attention_and_rnns.pdf
related_pages: []
tags:
- Transformer
- representation learning
---

[[Positional encoding]] is a technique used to inject information about the relative or absolute position of tokens in an [[input sequence]] into models that, like [[Self-attention]], do not inherently process order. In the [[Transformer architecture]], positional encodings are typically added to the input [[embedding]]s before they are fed into the self-attention layers, allowing the model to utilize sequence order.
