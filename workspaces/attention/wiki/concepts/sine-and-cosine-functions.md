---
title: Sine and Cosine Functions
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- positional-encoding
- positional-representation
- transformer
- positional-encoding
tags:
- positional encoding
- mathematics
- transformer
updated: '2023-10-27'
---

Sine and cosine functions are trigonometric functions used in the Transformer architecture for generating positional encodings. These functions are employed to inject information about the order of tokens in a sequence when the model itself lacks inherent sequential processing capabilities.

## Overview
In the Transformer, positional encodings are added to the input embeddings to provide the model with information about the relative or absolute position of tokens. The chosen method uses sine and cosine functions of different frequencies for each dimension of the positional encoding vector. Specifically, for a position 'pos' and dimension 'i', the encoding is calculated as:

PE(pos, 2i) = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))

where d_model is the dimensionality of the embeddings.

## Key Properties
- **Geometric Progression of Wavelengths**: The wavelengths of the sinusoids form a geometric progression from 2π to 10000 * 2π.
- **Relative Position Learning**: This formulation is hypothesized to allow the model to easily learn to attend by relative positions, as PE(pos+k) can be represented as a linear function of PE(pos) for any fixed offset k.
- **Extrapolation**: The sinusoidal nature may enable the model to extrapolate to sequence lengths longer than those encountered during training.

## Role in Context
These mathematical functions are a key component of the positional encoding strategy in the Transformer. By providing a consistent and structured way to represent positions, they enable the model to leverage sequential information, which is crucial for understanding language and other sequential data.
