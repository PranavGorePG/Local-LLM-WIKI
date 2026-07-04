---
title: Recurrent Neural Network
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- long-short-term-memory
- gated-recurrent-neural-network
- sequence-modeling
- gradient-flow
- long-range-dependencies
tags:
- neural networks
- sequence modeling
confidence: high
updated: '2023-10-27'
---

Recurrent Neural Networks (RNNs) are a class of artificial neural networks designed to process sequential data. Unlike feedforward networks, RNNs have connections that form directed cycles, allowing them to maintain an internal state or 'memory' of previous inputs. This recurrent nature enables them to capture temporal dependencies in data, making them suitable for tasks like language modeling and machine translation.

Traditionally, RNNs have been the dominant architecture for sequence modeling tasks. However, their inherent sequential computation limits parallelization during training, which becomes a significant bottleneck for long sequences. The "Attention Is All You Need" paper notes that RNNs factor computation along symbol positions, generating hidden states sequentially. This characteristic makes them less efficient compared to models that can process sequences in parallel.
