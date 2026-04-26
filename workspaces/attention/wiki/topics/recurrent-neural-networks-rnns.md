---
title: Recurrent Neural Networks (RNNs)
type: Concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- Machine Translation
- Encoder-Decoder Architecture
- Transformer Architecture
- Attention Mechanism
- NIPS 2017 Attention Is All You Need Paper
tags:
- Neural Networks
- Deep Learning
- Sequence Models
---

[[Recurrent Neural Networks (RNNs)]] are a class of neural networks particularly well-suited for processing sequential data. Unlike traditional feed-forward networks, RNNs have connections that loop back on themselves, allowing them to maintain a "memory" of previous inputs in a sequence. At each time step, an RNN processes the current input and updates its hidden state, which then influences the processing of the next input. This inherent sequential nature makes them suitable for tasks like language modeling and [[Machine Translation]]. However, their sequential computation—where hidden state `ht` is a function of `ht-1` and input `t`—precludes parallelization within training examples, becoming a critical limitation at longer sequence lengths.Variants like Long Short-Term Memory (LSTM) and Gated Recurrent Units (GRUs) address issues like vanishing gradients and improve the ability to learn long-range dependencies. Despite their historical dominance, the [[Transformer Architecture]], introduced in "[[Attention Is All You Need]]" (Vaswani et al., 2017), notably eschewed RNNs entirely in favor of [[Attention Mechanism]]s, demonstrating superior parallelization and performance.
