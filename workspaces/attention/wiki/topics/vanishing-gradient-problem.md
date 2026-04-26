---
title: Vanishing gradient problem
type: training problem
source_documents:
- self_attention_and_rnns.pdf
related_pages: []
tags:
- training
- RNN
- deep learning
---

The [[vanishing gradient problem]] occurs during the training of deep neural networks, particularly [[Recurrent Neural Network (RNN)|RNN]]s, when gradients become extremely small as they are propagated backward through many layers or [[time step|time steps]]. This makes it difficult for the model to learn [[long-range dependency|long-range dependencies]] because the updates to the weights in earlier parts of the network become negligible. Variants like [[Long Short-Term Memory (LSTM)]] and [[Gated Recurrent Unit (GRU)]] were developed to mitigate this issue.
