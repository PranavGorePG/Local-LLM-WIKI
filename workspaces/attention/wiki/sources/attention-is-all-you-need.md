---
title: Attention Is All You Need
type: source
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- transformer
- self-attention
- multi-head-attention
- scaled-dot-product-attention
- ashish-vaswani
- authors
- google-brain
- google-research
- nips-2017
- nvidia-p100-gpus
- tensor2tensor
- university-of-toronto
- wmt-2014-english-french
- wmt-2014-english-german
tags:
- paper
- machine translation
- attention
confidence: High
updated: '2023-10-27'
---

The paper "Attention Is All You Need" introduces the Transformer, a novel neural network architecture that relies solely on attention mechanisms, dispensing with recurrence and convolutions entirely. This architecture significantly advanced the state-of-the-art in machine translation and demonstrated the power of attention-based models.

## Overview
This seminal paper, published at NIPS 2017, proposed the Transformer model, which eschews traditional recurrent neural networks (RNNs) and convolutional neural networks (CNNs) in favor of self-attention mechanisms. The authors argued that this approach allows for significantly more parallelization and can achieve superior translation quality with less training time.

## Key Findings
*   **Transformer Architecture:** The model utilizes stacked self-attention and point-wise, fully connected layers for both its encoder and decoder.
*   **Attention Mechanisms:** It employs Scaled Dot-Product Attention and Multi-Head Attention, enabling the model to jointly attend to information from different representation subspaces and positions.
*   **Performance:** The Transformer achieved state-of-the-art results on the WMT 2014 English-to-German and English-to-French translation tasks, significantly outperforming previous models, including ensembles, with a fraction of the training cost.
*   **Parallelization:** By removing recurrence, the Transformer allows for greater parallelization during training, leading to faster training times.

## Role in Context
This paper marked a paradigm shift in sequence modeling, particularly in natural language processing. The Transformer architecture has since become the foundation for many subsequent influential models, including BERT, GPT, and T5, driving progress in a wide range of NLP tasks.

## Related Concepts
*   [[transformer|Transformer]]: The core model architecture introduced in this paper.
*   [[self-attention|Self-Attention]]: A key mechanism that allows the model to weigh the importance of different parts of the input sequence.
*   [[multi-head-attention|Multi-Head Attention]]: An extension of self-attention that allows attending to information from different representation subspaces.
*   [[scaled-dot-product-attention|Scaled Dot-Product Attention]]: The specific attention function used in the Transformer.
*   [[machine-translation|Machine Translation]]: The primary task on which the Transformer was evaluated.

## References
*   NIPS-2017-attention-is-all-you-need-Paper.pdf
