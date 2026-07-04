---
title: Dilated Convolutions
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- convolutional-neural-network
tags:
- deep learning
- neural networks
- sequence modeling
- computer vision
confidence: high
updated: '2023-10-27'
---

Dilated convolutions, also known as à trous convolutions, are a technique used in convolutional neural networks (CNNs) to increase the receptive field of a convolutional layer without increasing the number of parameters or computational cost significantly. This is achieved by inserting gaps (or "holes") between the kernel elements, effectively skipping input units. This allows the network to capture larger-scale context while maintaining the same resolution.

In the context of sequence modeling, dilated convolutions have been employed to enable convolutional models to learn dependencies between distant positions in a sequence more effectively than standard convolutions. By increasing the receptive field with dilation, the number of operations required to relate distant signals is reduced compared to using a stack of standard convolutional layers. This approach helps in learning long-range dependencies by decreasing the maximum path length between any two positions in the network. However, compared to self-attention mechanisms, which reduce path lengths to a constant, dilated convolutions still have a path length that grows with the sequence length, albeit at a slower rate than standard convolutions.
