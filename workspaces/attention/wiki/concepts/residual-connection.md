---
title: Residual Connection
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- transformer
- layer-normalization
- gradient-flow
tags:
- deep learning
- architecture
confidence: high
updated: '2023-10-27'
---

A residual connection, also known as a skip connection, is a technique used in deep neural networks to allow gradients to flow more easily through the network during training. Instead of just passing the output of a layer to the next layer, a residual connection adds the original input of the layer to its output. This is expressed as `x + Sublayer(x)`, where `x` is the input to the sub-layer and `Sublayer(x)` is the output of the sub-layer function. This addition is typically followed by a normalization step, such as Layer Normalization. In the Transformer architecture, residual connections are employed around each of the two sub-layers within both the encoder and decoder layers. This mechanism helps to mitigate the vanishing gradient problem, enabling the training of deeper networks and improving the ability to learn complex representations by ensuring that information from earlier layers is not lost. All sub-layers in the Transformer model, as well as embedding layers, produce outputs of dimension dmodel = 512, which is compatible with the residual connections.
