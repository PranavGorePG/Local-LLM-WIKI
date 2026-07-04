---
title: Parallel Computation
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- transformer
- computational-complexity
- self-attention
tags:
- efficiency
- deep learning
- training
---

Parallel computation is a type of computation in which many calculations are carried out simultaneously, operating on the principle that large problems can often be divided into smaller ones, which are then solved concurrently.

## Overview
In the context of deep learning and neural networks, parallel computation is crucial for reducing training time and enabling the training of larger, more complex models. Architectures that can be parallelized more effectively can leverage multi-core processors and GPUs more efficiently. The Transformer architecture, by dispensing with recurrence and relying on self-attention, offers significant advantages in parallelizability compared to traditional recurrent models.

## Key Properties
- **Reduced Training Time**: Parallel computation allows many operations to be performed at the same time, leading to faster model training.
- **Scalability**: Enables the training of larger models and the processing of longer sequences by distributing the workload.
- **Hardware Utilization**: Maximizes the use of parallel processing capabilities of modern hardware like GPUs.

## Role in Context
The Transformer model's design, based solely on attention mechanisms, fundamentally enhances parallel computation. Unlike recurrent neural networks, which process sequences sequentially, self-attention layers can compute representations for all positions in parallel. This inherent parallelizability is a key reason for the Transformer's significantly faster training times and its ability to achieve state-of-the-art results on tasks like machine translation with reduced computational cost compared to previous sequential models.
