---
title: Hidden state
type: model state
source_documents:
- self_attention_and_rnns.pdf
related_pages: []
tags:
- RNN
- model state
---

The [[hidden state]] is an internal memory component in [[Recurrent Neural Network (RNN)|RNN]]s that accumulates information from previous [[time step|time steps]] in a sequence. It is updated at each time step based on the current input and the previous hidden state, allowing the RNN to maintain context. In variants like [[Long Short-Term Memory (LSTM)]] and [[Gated Recurrent Unit (GRU)]], the hidden state is augmented or managed by additional gating mechanisms.
