---
title: Recurrence
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- transformer
- rnn
tags:
- neural networks
- sequence modeling
---

Recurrence, in the context of neural networks, refers to architectures that process sequential data by maintaining a hidden state that is updated at each step based on the current input and the previous hidden state. Recurrent Neural Networks (RNNs), including variants like Long Short-Term Memory (LSTM) and Gated Recurrent Units (GRU), are the most prominent examples. This sequential computation, while powerful for modeling dependencies in sequences, inherently limits parallelization during training.

Historically, recurrence has been the dominant approach for sequence modeling tasks like machine translation. However, the Transformer architecture, which relies solely on attention mechanisms, has demonstrated that it is possible to achieve superior performance and significantly faster training times by completely dispensing with recurrence. This shift represents a major paradigm change in sequence modeling.
