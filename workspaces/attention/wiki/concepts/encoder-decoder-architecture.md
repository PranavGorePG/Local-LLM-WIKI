---
title: Encoder-Decoder Architecture
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- transformer
tags:
- sequence modeling
- neural networks
---

The encoder-decoder architecture is a common framework for sequence transduction tasks. In this architecture, an encoder component processes an input sequence and maps it to a sequence of continuous representations. A decoder component then takes these representations and generates an output sequence, typically one element at a time in an auto-regressive manner. This structure has been widely used in tasks like machine translation, where the encoder reads the source sentence and the decoder generates the translated sentence.

The Transformer model adopts this overall architecture but replaces the traditional recurrent or convolutional layers within the encoder and decoder with attention mechanisms. Each encoder and decoder layer in the Transformer consists of multi-head self-attention and position-wise feed-forward networks, enabling it to draw global dependencies between input and output sequences more effectively than previous methods.
