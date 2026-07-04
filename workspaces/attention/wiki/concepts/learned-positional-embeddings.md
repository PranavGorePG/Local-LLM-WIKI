---
title: Learned Positional Embeddings
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- positional-encoding
- positional-representation
- transformer
tags:
- positional encoding
- transformer
- embeddings
---

Learned positional embeddings are an alternative method to fixed sinusoidal encodings for providing positional information to sequence models like the Transformer. Instead of using predefined mathematical functions, these embeddings are treated as parameters that are learned during the model's training process.

## Overview
In this approach, a separate embedding vector is learned for each possible position in the input sequence, up to a certain maximum length. These learned embeddings are then added to the corresponding token embeddings, similar to how fixed positional encodings are incorporated. The model adjusts these positional embeddings through backpropagation to best capture the positional nuances relevant to the task.

## Key Properties
- **Learnable Parameters**: Positional embeddings are parameters of the model that are optimized during training.
- **Task-Specific**: They can potentially adapt to capture positional relationships that are most important for the specific task.
- **Empirical Equivalence**: Experiments in the original Transformer paper showed that using learned positional embeddings produced nearly identical results to using sinusoidal positional encodings.

## Role in Context
Learned positional embeddings serve the same purpose as sinusoidal encodings: to inform the model about the order of elements in a sequence. While sinusoidal encodings offer theoretical advantages in extrapolation to longer sequences, learned embeddings provide a more adaptive, data-driven approach to representing position. Both methods are crucial for non-recurrent architectures like the Transformer to effectively process sequential data.
