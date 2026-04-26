---
title: NIPS 2017 Attention Is All You Need Paper
type: source
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- Transformer Architecture
- Attention Mechanism
- Self-Attention
- Multi-Head Attention
- Positional Encoding
- Encoder-Decoder Architecture
- Machine Translation
tags:
- research paper
- deep learning
- NLP
- seminal work
confidence: High
---

This seminal paper, "Attention Is All You Need", published at NIPS 2017, introduced the [[Transformer Architecture]], a novel sequence transduction model that entirely eschews recurrence and convolutions in favor of [[Attention Mechanism]]s. Authored by Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, and Illia Polosukhin (primarily from Google Brain and Google Research). Key Contribution: The paper demonstrated that a model based solely on attention mechanisms could achieve superior quality and be significantly more parallelizable and faster to train than previous state-of-the-art models based on complex recurrent or convolutional neural networks. Performance: The Transformer model achieved new state-of-the-art [[BLEU Score]]s on the WMT 2014 English-to-German (28.4 BLEU) and English-to-French (41.0 BLEU) [[Machine Translation]] tasks. Core Ideas: The paper detailed [[Scaled Dot-Product Attention]], [[Multi-Head Attention]], the specific [[Encoder-Decoder Architecture]] of the Transformer, [[Positional Encoding]], and the benefits of [[Self-Attention]] in terms of computational complexity, parallelization, and path length for long-range dependencies. The code for the Transformer model was made available as part of the TensorFlow `tensor2tensor` library.
