---
title: Embedding
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages: []
tags:
- nlp
- representation learning
confidence: high
updated: '2023-10-27'
---

In natural language processing, embeddings are vector representations of discrete variables, such as words or tokens. They are learned such that words with similar meanings or that appear in similar contexts have similar vector representations in a high-dimensional space. The Transformer model utilizes learned embeddings to convert input and output tokens into vectors of dimension `dmodel`, which is set to 512 in the paper. These embeddings are then combined with positional encodings to provide the model with information about the order of tokens in a sequence. The Transformer shares the same weight matrix between the input and output embedding layers and the pre-softmax linear transformation, and these weights are multiplied by the square root of `dmodel` (`√dmodel`) in the embedding layers.
