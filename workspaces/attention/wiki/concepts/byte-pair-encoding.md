---
title: Byte-Pair Encoding
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- word-piece-vocabulary
- tokenization
tags:
- nlp
- tokenization
- subword units
- data preprocessing
confidence: high
updated: '2023-10-27'
---

Byte-Pair Encoding (BPE) is a data compression technique that can also be used as a subword tokenization method for natural language processing. It iteratively merges the most frequent pairs of bytes (or characters) in a given text to form new, longer symbols. This process continues until a desired vocabulary size is reached or a specified number of merges have been performed.

In the context of the "Attention Is All You Need" paper, BPE was used to create a shared source-target vocabulary of approximately 37,000 tokens for the WMT 2014 English-German translation task. By using BPE, the model can handle rare words and out-of-vocabulary words by breaking them down into known subword units. This approach helps in managing large vocabularies and improving the model's ability to generalize to unseen words, as it learns representations for subword units rather than just whole words. It is an effective method for balancing vocabulary size and the ability to represent diverse linguistic forms.
