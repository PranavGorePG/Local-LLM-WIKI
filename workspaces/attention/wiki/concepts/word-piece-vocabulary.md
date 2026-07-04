---
title: Word-Piece Vocabulary
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- byte-pair-encoding
- tokenization
tags:
- nlp
- tokenization
- subword units
- data preprocessing
confidence: high
updated: '2023-10-27'
---

A word-piece vocabulary is a type of subword tokenization method used in natural language processing. Similar to Byte-Pair Encoding (BPE), it aims to break down words into smaller, meaningful units, allowing models to handle rare words and reduce the overall vocabulary size. Word-piece models typically work by greedily selecting the most likely subword units to form words, often prioritizing units that maximize the likelihood of the training corpus.

The paper "Attention Is All You Need" utilized a word-piece vocabulary of 32,000 tokens for the WMT 2014 English-French translation task. This approach allows the model to represent a wide range of words, including those not seen during training, by composing them from these subword units. Word-piece tokenization helps in balancing the trade-off between having a vocabulary large enough to capture linguistic richness and small enough to maintain computational efficiency and avoid data sparsity issues. It is a crucial preprocessing step for many modern NLP models.
