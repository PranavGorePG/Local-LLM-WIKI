---
title: Transformer Architecture
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- Attention Mechanism
- Self-Attention
- Multi-Head Attention
- Positional Encoding
- Encoder-Decoder Architecture
- Machine Translation
tags:
- neural networks
- deep learning
- sequence transduction
- natural language processing
---

The Transformer is a novel neural network architecture proposed in the paper "[[NIPS 2017 Attention Is All You Need Paper]]" that dispenses with recurrence and convolutions, relying solely on [[Attention Mechanism]]s. It was introduced to address the limitations of traditional [[Recurrent Neural Networks (RNNs)]] and [[Convolutional Neural Networks (CNNs) in Sequence Models]] in handling long-range dependencies and parallelization. Key Features: Attention-only: Replaces sequential computation with parallelizable attention mechanisms. [[Self-Attention]]: Allows the model to weigh the importance of different words in the input sequence when processing a word. [[Multi-Head Attention]]: Enhances the model's ability to focus on different parts of the input/output at different positions, operating with multiple "heads" in parallel. [[Encoder-Decoder Architecture]]: Follows the standard structure but uses stacked self-attention and point-wise fully connected layers. [[Positional Encoding]]: Injects information about the relative or absolute position of tokens, as the model lacks inherent sequence order processing. Advantages: Parallelization: Significantly faster training times due to reduced sequential computation. Quality: Achieved state-of-the-art results on [[Machine Translation]] tasks (e.g., WMT 2014 English-to-German and English-to-French). Long-range Dependencies: Connects all positions with a constant number of sequential operations, making it easier to learn long-range dependencies compared to RNNs and some CNNs.
