---
title: Attention Mechanism
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- Transformer Architecture
- Self-Attention
- Multi-Head Attention
- Scaled Dot-Product Attention
- Encoder-Decoder Architecture
tags:
- neural networks
- deep learning
- sequence transduction
---

An [[Attention Mechanism]] is a technique in neural networks that allows the model to weigh the importance of different parts of an input sequence when predicting an output. It functions by mapping a query and a set of key-value pairs to an output, which is a weighted sum of the values. The weights are determined by a compatibility function of the query with corresponding keys. In the context of the [[Transformer Architecture]], attention mechanisms are fundamental, entirely replacing [[Recurrent Neural Networks (RNNs)]] and [[Convolutional Neural Networks (CNNs) in Sequence Models]]. Types of Attention in Transformer: [[Scaled Dot-Product Attention]]: The specific attention function used, involving dot products of queries and keys, scaled by `1/√dk`, followed by a softmax to get weights. [[Multi-Head Attention]]: An enhancement where multiple attention functions run in parallel on linearly projected versions of queries, keys, and values. [[Self-Attention]]: Relates different positions of a single sequence to compute a representation of that sequence. Encoder-Decoder Attention: Where queries come from the decoder and keys/values from the encoder output, allowing the decoder to attend to the entire input sequence.
