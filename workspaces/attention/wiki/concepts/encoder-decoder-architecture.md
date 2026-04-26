---
title: Encoder-Decoder Architecture
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- Transformer Architecture
- Attention Mechanism
- Self-Attention
tags:
- neural networks
- deep learning
- sequence transduction
---

The [[Encoder-Decoder Architecture]] is a prevalent structure in competitive neural sequence transduction models, including the [[Transformer Architecture]]. It consists of two main parts: Encoder: Maps an input sequence of symbol representations `(x1, ..., xn)` to a sequence of continuous representations `z = (z1, ..., zn)`. Decoder: Given `z`, generates an output sequence `(y1, ..., ym)` of symbols one element at a time. It is auto-regressive, consuming previously generated symbols as additional input for the next prediction. Transformer's Implementation: Encoder Stack: Composed of `N=6` identical layers. Each layer has two sub-layers: a [[Multi-Head Attention]] (specifically [[Self-Attention]]) mechanism and a position-wise fully connected feed-forward network. Residual connections and layer normalization are employed. Decoder Stack: Also composed of `N=6` identical layers. In addition to the two sub-layers found in the encoder, it includes a third sub-layer for "encoder-decoder attention". This third sub-layer performs multi-head attention over the output of the encoder stack, allowing every position in the decoder to attend over all positions in the input sequence. The self-attention sub-layer in the decoder is modified to prevent positions from attending to subsequent positions (masking). All sub-layers and embedding layers in the Transformer produce outputs of dimension `dmodel = 512` to facilitate residual connections.
