---
title: Language Modeling
type: topic
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- sequence-modeling
- recurrent-neural-network
- perplexity
tags:
- natural language processing
- deep learning
confidence: high
updated: '2023-10-27'
---

Language modeling is the task of predicting the likelihood of a sequence of words. In essence, it involves learning the probability distribution over sequences of words in a given language. This capability is foundational for many natural language processing (NLP) applications, including machine translation, speech recognition, text generation, and spell checking.

Traditional approaches to language modeling often relied on statistical methods like n-grams. However, with the rise of deep learning, Recurrent Neural Networks (RNNs), and subsequently LSTMs and GRUs, became the state-of-the-art for capturing the sequential dependencies in language. The "Attention Is All You Need" paper positions the Transformer architecture as a powerful alternative, demonstrating its effectiveness in sequence transduction tasks like machine translation, which are closely related to language modeling, by relying solely on attention mechanisms.
