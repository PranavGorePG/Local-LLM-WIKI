---
title: Long-range dependency
type: data characteristic
source_documents:
- self_attention_and_rnns.pdf
related_pages: []
tags:
- sequence modeling
- data characteristic
---

A [[long-range dependency]] refers to the relationship between elements in a sequence that are far apart from each other. [[Self-attention]] mechanisms are particularly effective at capturing these dependencies due to their direct access to all tokens in the sequence. [[Recurrent Neural Network (RNN)|RNN]]s, especially standard ones, struggle with long-range dependencies due to issues like the [[vanishing gradient problem]].
