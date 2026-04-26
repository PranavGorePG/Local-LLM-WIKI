---
title: Transformer Architecture
type: Concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
- Attention_Mechanisms_Perspective_Exploring_LLM_Pro.pdf
related_pages:
- Attention Mechanism
- Self-Attention
- Multi-Head Attention
- Positional Encoding
- Encoder-Decoder Architecture
- Recurrent Neural Networks (RNNs)
- Convolutional Neural Networks (CNNs) in Sequence Models
- Machine Translation
- Large Language Models (LLMs)
- NIPS 2017 Attention Is All You Need Paper
tags:
- Machine Learning
- Neural Networks
- NLP
- Deep Learning
- LLMs
---

The [[Transformer Architecture]] is a novel neural network model introduced in the paper "[[Attention Is All You Need]]" by Vaswani et al. (2017). It represents a significant departure from previous dominant sequence transduction models that relied on [[Recurrent Neural Networks (RNNs)]] or [[Convolutional Neural Networks (CNNs)]], as it dispenses with recurrence and convolutions entirely. Instead, the Transformer is based solely on [[Attention Mechanism]]s, particularly [[Self-Attention]] and [[Multi-Head Attention]], for drawing global dependencies between input and output sequences. It employs an [[Encoder-Decoder Architecture]] where both the encoder and decoder are composed of stacks of identical layers. Each layer includes multi-head self-attention and position-wise fully connected feed-forward networks, along with residual connections and layer normalization. To inject information about the order of the sequence, the Transformer uses [[Positional Encoding]]. This architecture allows for significant parallelization, leading to faster training times and state-of-the-art performance in tasks like [[Machine Translation]]. The Transformer's innovations laid the foundation for modern [[Large Language Models (LLMs)]].
