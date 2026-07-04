---
title: Linear Transformation
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- multi-head-attention
- position-wise-feed-forward-networks
- transformer
tags:
- neural networks
- deep learning
- mathematical operation
---

A linear transformation is a fundamental mathematical operation in linear algebra and machine learning, used to map input vectors to output vectors while preserving the vector space structure. In neural networks, linear transformations are typically implemented as matrix multiplications, often followed by a bias term.

## Overview
In the context of neural networks, a linear transformation takes an input vector 'x' and transforms it into an output vector 'y' using a weight matrix 'W' and a bias vector 'b': y = xW + b (or y = Wx + b depending on convention). These transformations are applied at various stages within neural network architectures to modify and project data into different representation spaces.

## Key Properties
- **Projection**: Linear transformations can project data from one dimensional space to another.
- **Learned Parameters**: The weight matrix (W) and bias vector (b) are parameters that are learned during the training process.
- **Composition**: Multiple linear transformations can be composed to form more complex mappings.

## Role in Context
Linear transformations are a core component in several parts of the Transformer model. They are used in:
- **Multi-Head Attention**: Projecting queries, keys, and values into different subspaces.
- **Position-wise Feed-Forward Networks**: The two sub-layers within these networks are linear transformations with a ReLU activation in between.
- **Embeddings**: Converting input and output tokens into dense vector representations.

The ability to learn these transformations is what allows the Transformer to adapt to the specific patterns and relationships within the data it is trained on.
