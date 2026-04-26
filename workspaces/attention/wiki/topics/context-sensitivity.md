---
title: Context-sensitivity
type: data characteristic
source_documents:
- self_attention_and_rnns.pdf
related_pages: []
tags:
- NLP
- representation learning
---

[[Context-sensitivity]] is the property where the representation or meaning of an element (like a word) depends on its surrounding elements in a sequence. [[Self-attention]] inherently provides context-sensitive representations because each token's output is influenced by a [[weighted sum]] of all other tokens' [[Value (V)|Value]] vectors, based on calculated [[attention score]]s.
