---
title: Gated Recurrent Unit (GRU)
type: model architecture
source_documents:
- self_attention_and_rnns.pdf
related_pages: []
tags:
- RNN
- deep learning
---

The [[Gated Recurrent Unit (GRU)]] is a simplified variant of the [[Long Short-Term Memory (LSTM)]] architecture, also designed to handle [[sequential data]] and mitigate the [[vanishing gradient problem]]. GRUs combine the [[cell state]] and [[hidden state]] into a single [[hidden state vector]] and use only two gates: a [[reset gate]] and an [[update gate]]. This reduction in parameters can lead to faster training and comparable performance to LSTMs on many tasks.
