---
title: Sequence Transduction
type: topic
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- sequence-modeling
- machine-translation
- transformer
tags:
- sequence modeling
- machine translation
updated: '2023-10-27'
---

Sequence transduction refers to the task of mapping an input sequence to an output sequence. This is a fundamental problem in natural language processing and machine learning, with applications in areas such as machine translation, text summarization, and question answering. Traditional models for sequence transduction often rely on recurrent neural networks (RNNs) or convolutional neural networks (CNNs) to process sequential data. However, these architectures can suffer from limitations in parallelization and in capturing long-range dependencies.

The Transformer model, introduced in "Attention Is All You Need," revolutionized sequence transduction by relying solely on attention mechanisms, dispensing with recurrence and convolutions. This approach allows for greater parallelization and can achieve superior quality and training efficiency on tasks like machine translation.
