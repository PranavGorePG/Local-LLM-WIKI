---
title: Dropout
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages: []
tags:
- regularization
- training
confidence: High
updated: '2023-10-27'
---

Dropout is a regularization technique used during the training of neural networks to prevent overfitting. It works by randomly setting a fraction of the output units of a layer to zero at each update during training time.

## Definition
Dropout is a method of reducing overfitting in neural networks by randomly disabling (setting to zero) a proportion of neurons during each training iteration. This forces the network to learn more robust representations as it cannot rely on any single neuron.

## Key Properties
In the Transformer model, dropout is applied to the output of each sub-layer before it is added to the sub-layer input and normalized. It is also applied to the sums of embeddings and positional encodings in both the encoder and decoder stacks. For the base model, a dropout rate (Pdrop) of 0.1 was used. For the English-to-French translation task, a dropout rate of 0.3 was used for the big model. The paper also notes that dropout is very helpful in avoiding overfitting, as observed in Table 3.

## Role in Context
Dropout plays a crucial role in the Transformer's training process by enhancing its generalization ability and preventing it from memorizing the training data. This is particularly important given the model's large capacity.

## Related Concepts
* [[Overfitting|Overfitting]]: A phenomenon where a model learns the training data too well, leading to poor performance on unseen data. Dropout is a common technique to combat this.
* [[Regularization|Regularization]]: Techniques used to prevent overfitting and improve the generalization of machine learning models.

## References
* NIPS-2017-attention-is-all-you-need-Paper.pdf
