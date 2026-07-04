---
title: Convolutional Neural Network
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- dilated-convolutions
- separable-convolutions
- attention-mechanism
tags:
- deep learning
- neural networks
- computer vision
- sequence modeling
confidence: high
updated: '2023-10-27'
---

Convolutional Neural Networks (CNNs) are a class of deep neural networks, most commonly applied to analyzing visual imagery, though they are also used in other domains such as natural language processing and sequence modeling. CNNs employ convolutional layers, which apply filters to input data to detect spatial hierarchies of features. Unlike standard neural networks, CNNs have a built-in bias that leverages the spatially local correlations in input data.

In sequence transduction tasks, CNNs have been used as a basic building block, computing hidden representations in parallel for all input and output positions. In these models, the number of operations required to relate signals from two arbitrary input or output positions grows with the distance between positions, linearly for models like ConvS2S. This can make it more difficult to learn dependencies between distant positions compared to architectures that utilize attention mechanisms. However, CNNs offer efficient computation and can be parallelized.

Key aspects of CNNs include convolutional layers, pooling layers, and activation functions. They are known for their effectiveness in tasks requiring the identification of local patterns and structures. While the "Attention Is All You Need" paper contrasts its Transformer model with CNNs, highlighting the Transformer's ability to reduce path lengths to a constant number of operations, CNNs remain a significant architecture in deep learning.
