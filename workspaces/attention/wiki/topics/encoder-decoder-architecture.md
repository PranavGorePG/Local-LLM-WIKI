---
title: Encoder-Decoder Architecture
type: Concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- Machine Translation
- Recurrent Neural Networks (RNNs)
- Self-Attention
- Transformer Architecture
- Attention Mechanism
- Multi-Head Attention
- Convolutional Neural Networks (CNNs) in Sequence Models
tags:
- Neural Networks
- Deep Learning
- Sequence Models
---

The [[Encoder-Decoder Architecture]] is a common framework in neural sequence transduction models, particularly for tasks like [[Machine Translation]]. It consists of two main parts: an encoder and a decoder. The encoder processes an input sequence of symbol representations (e.g., source language words) and transforms it into a sequence of continuous representations, often referred to as a context vector or hidden states. The decoder then takes this encoded representation and generates an output sequence of symbols (e.g., target language words), typically one element at a time, in an auto-regressive manner.Many early models used [[Recurrent Neural Networks (RNNs)]] or [[Convolutional Neural Networks (CNNs)]] for both the encoder and decoder. The [[Transformer Architecture]], introduced in "[[Attention Is All You Need]]" (Vaswani et al., 2017), also follows this overall structure, but replaces RNNs and CNNs with stacked [[Self-Attention]] and point-wise fully connected layers. The decoder in a Transformer specifically inserts a third [[Multi-Head Attention]] sub-layer that performs attention over the output of the encoder stack, allowing every position in the decoder to attend to all positions in the input sequence.
