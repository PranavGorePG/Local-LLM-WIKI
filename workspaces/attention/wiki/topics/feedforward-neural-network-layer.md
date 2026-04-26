---
title: Feedforward neural network layer
type: model architecture component
source_documents:
- self_attention_and_rnns.pdf
related_pages: []
tags:
- Transformer
- deep learning
---

A [[feedforward neural network layer]] is a standard component in many neural network architectures, including the [[Transformer architecture]]. In Transformers, after the [[Multi-Head Attention]] layer, the output for each position is passed through a position-wise feedforward network. This typically consists of two linear transformations with a [[non-linear activation function]] (like ReLU) in between, allowing the model to process the combined information from the attention heads.
