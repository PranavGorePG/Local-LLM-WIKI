---
title: Separable Convolutions
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- convolutional-neural-network
- dilated-convolutions
- transformer
tags:
- deep learning
- neural networks
- convolution
- efficiency
confidence: high
updated: '2023-10-27'
---

Separable convolutions are a type of convolutional operation that decomposes a standard convolution into two steps: a depthwise convolution and a pointwise convolution. A depthwise convolution applies a single filter to each input channel, while a pointwise convolution (a 1x1 convolution) then combines the outputs of the depthwise convolution across channels.

This decomposition significantly reduces the computational complexity compared to standard convolutions. The paper "Attention Is All You Need" mentions that separable convolutions can decrease computational complexity considerably. Even when the kernel size k is equal to the sequence length n, the complexity of a separable convolution is comparable to the combination of a self-attention layer and a point-wise feed-forward layer, which is the approach taken in the Transformer model. Separable convolutions offer a way to create deeper and wider networks with fewer parameters and less computation, making them an efficient alternative in various deep learning applications, particularly where computational resources are constrained.
