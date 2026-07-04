---
title: Computational Complexity
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- parallel-computation
- transformer
- self-attention
- computational-complexity
tags:
- efficiency
- neural networks
- performance
updated: '2023-10-27'
---

Computational complexity refers to the amount of computational resources (such as time and memory) required by an algorithm or model to perform its task. In the context of deep learning, it often relates to the number of operations needed for training and inference, and how these operations scale with input size.

## Overview
When comparing different neural network architectures, computational complexity is a key metric. For sequence modeling, it's important to consider how complexity scales with sequence length (n) and representation dimension (d). Different layer types (e.g., self-attention, recurrent, convolutional) have varying computational complexities. For instance, self-attention layers have a quadratic complexity with respect to sequence length (O(n^2 * d)), while recurrent layers have a linear complexity (O(n * d^2)).

## Key Properties
- **Scaling**: How the computational cost grows with input size (e.g., sequence length).
- **Parallelizability**: The degree to which computations can be performed simultaneously, impacting training time.
- **Resource Requirements**: Memory and processing power needed for training and inference.

## Role in Context
Computational complexity is a significant consideration when designing and choosing neural network architectures. The Transformer's self-attention mechanism, while powerful, has a higher computational complexity (O(n^2)) compared to RNNs (O(n)) for very long sequences. However, its high degree of parallelizability often leads to faster training times in practice, especially on modern hardware. Understanding these trade-offs is crucial for optimizing model performance and efficiency.
