---
title: Training Data
type: topic
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- batching
- training
tags:
- machine learning
- deep learning
- data
- training
confidence: high
updated: '2023-10-27'
---

Training data refers to the collection of examples used to teach a machine learning model a specific task. The quality, quantity, and characteristics of the training data significantly influence the model's performance, generalization ability, and robustness. In sequence transduction tasks, such as machine translation, training data typically consists of pairs of sequences, for instance, sentences in a source language and their corresponding translations in a target language.

The paper "Attention Is All You Need" used specific datasets for its experiments. For English-to-German translation, it employed the standard WMT 2014 dataset, comprising approximately 4.5 million sentence pairs. For English-to-French translation, a larger dataset from WMT 2014 was used, containing 36 million sentences. These datasets were preprocessed using tokenization methods like Byte-Pair Encoding (BPE) and word-piece vocabularies to manage vocabulary size and handle rare words effectively. The training data is crucial for the model to learn the underlying patterns, dependencies, and translation mappings required for the task. The way this data is structured and presented to the model during training, such as through batching, also plays a vital role.
