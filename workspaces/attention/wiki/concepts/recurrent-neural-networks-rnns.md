---
title: Recurrent Neural Networks (RNNs)
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- Transformer Architecture
- Attention Mechanism
- Convolutional Neural Networks (CNNs) in Sequence Models
tags:
- neural networks
- deep learning
- sequence modeling
---

[[Recurrent Neural Networks (RNNs)]] are a class of neural networks well-suited for processing sequential data, such as text, speech, and time series. They are characterized by their "memory," where the output from one step is fed back as input to the next step, allowing them to capture dependencies across sequence positions. Long Short-Term Memory (LSTM) and Gated Recurrent Units (GRU) are popular variants that address the vanishing gradient problem in vanilla RNNs. Traditional Role: Before the advent of the [[Transformer Architecture]], RNNs (especially LSTMs and GRUs) were the dominant models for sequence modeling and transduction problems like language modeling and [[Machine Translation]]. Limitations Addressed by Transformer: Sequential Computation: RNNs inherently process data sequentially, which limits parallelization and becomes a bottleneck for long sequences. Long-range Dependencies: While LSTMs and GRUs improved this, learning dependencies between very distant positions in a sequence remained a challenge due to the length of paths forward and backward signals had to traverse. The [[Transformer Architecture]] was specifically designed to overcome these limitations by dispensing with recurrence entirely, relying instead on [[Self-Attention]] mechanisms to process all parts of a sequence in parallel.
