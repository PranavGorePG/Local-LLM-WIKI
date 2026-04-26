---
title: Convolutional Neural Networks (CNNs) in Sequence Models
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- Transformer Architecture
- Recurrent Neural Networks (RNNs)
tags:
- neural networks
- deep learning
- sequence modeling
---

While primarily known for image processing, [[Convolutional Neural Networks (CNNs) in Sequence Models]] have also been used as basic building blocks for sequence transduction models, such as the Extended Neural GPU, ByteNet, and ConvS2S. These models compute hidden representations in parallel for all input and output positions, aiming to reduce sequential computation compared to [[Recurrent Neural Networks (RNNs)]]. Mechanism: CNNs apply filters (kernels) to local regions of the input sequence to extract features. By stacking multiple convolutional layers, they can capture broader contexts. Limitations Addressed by Transformer: Path Length: In CNN-based models, the number of operations required to relate signals from two arbitrary input or output positions grows with the distance between positions (linearly for ConvS2S, logarithmically for ByteNet). This can make it difficult to learn dependencies between distant positions. Computational Cost: Convolutional layers can be more expensive than recurrent layers, particularly for wider kernels. The [[Transformer Architecture]] offers an improvement by reducing the path length between any two positions to a constant number of operations using [[Self-Attention]], which allows for more efficient learning of long-range dependencies and greater parallelization than both RNNs and many CNN-based sequence models.
