---
title: Parallelizable
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- transformer
- convolutions
- recurrence
tags:
- deep learning
- training efficiency
---

Parallelizable refers to the ability of a computational process or algorithm to be divided into smaller parts that can be executed simultaneously on multiple processors or computing units. In the context of neural network training, parallelization is crucial for reducing training time, especially for large models and datasets.

Traditional sequence modeling architectures like recurrent neural networks (RNNs) are inherently sequential, meaning computations must be performed in order, which limits their parallelizability. Convolutional Neural Networks (CNNs) offer more opportunities for parallelization within a layer. However, the Transformer architecture, by relying solely on attention mechanisms, achieves a high degree of parallelization. This is because attention calculations can be performed independently for different parts of the sequence, leading to significantly faster training times compared to recurrent or even convolutional models, particularly for longer sequences.
