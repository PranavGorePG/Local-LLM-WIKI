---
title: Encoder-decoder architecture
type: model architecture
source_documents:
- self_attention_and_rnns.pdf
related_pages: []
tags:
- sequence to sequence
- deep learning
---

An [[Encoder-decoder architecture]] is a framework used in sequence-to-sequence modeling. It consists of two main parts: an encoder that processes the input sequence and compresses it into a fixed-length context vector, and a decoder that generates the output sequence based on this context vector. This architecture was commonly implemented using [[Recurrent Neural Network (RNN|RNN]]s for tasks like [[Machine Translation]] and [[Seq2Seq model|Seq2Seq]] tasks. The [[Transformer architecture]] employs a similar concept but uses [[Self-attention]] mechanisms instead of recurrence.
