---
title: Gated Recurrent Neural Network
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- recurrent-neural-network
- long-short-term-memory
- sequence-modeling
tags:
- neural networks
- sequence modeling
- recurrent networks
confidence: high
updated: '2023-10-27'
---

Gated Recurrent Neural Networks (GRNNs) are a variation of Recurrent Neural Networks (RNNs) that incorporate gating mechanisms to better control the flow of information and mitigate the vanishing gradient problem. Similar to LSTMs, GRNNs use gates to decide what information to keep or forget from previous states, allowing them to capture longer-term dependencies more effectively than basic RNNs.

The "Attention Is All You Need" paper mentions gated recurrent networks as one of the established state-of-the-art approaches in sequence modeling and transduction tasks, such as language modeling and machine translation, prior to the introduction of the Transformer architecture. These models, like LSTMs, relied on sequential processing, which limited their parallelizability during training.
