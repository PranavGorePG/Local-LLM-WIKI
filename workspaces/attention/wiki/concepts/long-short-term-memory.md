---
title: Long Short-Term Memory
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- recurrent-neural-network
- gated-recurrent-neural-network
- sequence-modeling
tags:
- neural networks
- sequence modeling
- recurrent networks
confidence: high
updated: '2023-10-27'
---

Long Short-Term Memory (LSTM) networks are a specialized type of Recurrent Neural Network (RNN) designed to address the vanishing gradient problem, which hinders the ability of standard RNNs to learn long-range dependencies. LSTMs achieve this through a more complex internal structure involving gates (input, forget, and output gates) and a cell state, which allow for more controlled information flow and selective memory updates.

LSTMs have been a prominent architecture in sequence modeling and transduction problems, including language modeling and machine translation, before the advent of purely attention-based models. The "Attention Is All You Need" paper references LSTMs as a state-of-the-art approach in sequence modeling prior to their proposed Transformer model, which aims to surpass LSTMs by dispensing with recurrence entirely.
