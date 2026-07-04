---
title: Attention Mechanism
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- transformer
- scaled-dot-product-attention
- multi-head-attention
tags:
- deep learning
- sequence modeling
---

An attention mechanism is a technique used in neural networks to allow the model to focus on specific parts of the input when processing sequential data. It maps a query and a set of key-value pairs to an output, where the output is a weighted sum of the values, with weights determined by the compatibility between the query and the keys. This allows the model to dynamically weigh the importance of different input elements for a given task.

In the context of sequence transduction, attention mechanisms have become integral, enabling models to capture dependencies regardless of their distance in the input or output sequences. The Transformer model, however, leverages attention mechanisms exclusively, dispensing with recurrence and convolutions entirely. This is achieved through scaled dot-product attention and its multi-head variant, which collectively allow the model to attend to information from different representation subspaces at different positions.
