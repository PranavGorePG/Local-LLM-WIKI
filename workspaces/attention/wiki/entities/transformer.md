---
title: Transformer
type: entity
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- attention-mechanism
- scaled-dot-product-attention
- multi-head-attention
- encoder-decoder-architecture
- self-attention
- positional-encoding
- adam-optimizer
- google-brain
- nvidia-p100-gpus
- tensor2tensor
tags:
- neural networks
- sequence transduction
- machine translation
confidence: High
updated: '2023-10-27'
---

The Transformer is a novel neural network architecture introduced in "Attention Is All You Need" that eschews recurrence and convolutions entirely, relying solely on attention mechanisms to draw global dependencies between input and output sequences.

## Overview
Designed primarily for sequence transduction tasks like machine translation, the Transformer follows an encoder-decoder structure. The encoder maps an input sequence to a sequence of continuous representations, and the decoder generates an output sequence element by element, conditioned on the encoder's output and previously generated elements. Unlike traditional recurrent or convolutional models, the Transformer processes sequences in parallel, significantly reducing training time and enabling it to achieve state-of-the-art results on tasks such as machine translation.

## Key Properties
The Transformer's architecture consists of stacked identical layers, each comprising a multi-head self-attention mechanism and a position-wise fully connected feed-forward network. Residual connections and layer normalization are employed around each sub-layer to facilitate training. Key components include:

*   **Encoder:** Composed of N identical layers, each with a multi-head self-attention sub-layer and a position-wise feed-forward network. It processes the input sequence.
*   **Decoder:** Also composed of N identical layers, including the encoder's sub-layers plus an additional multi-head attention sub-layer that attends to the encoder's output. Crucially, the decoder's self-attention is masked to prevent attending to future positions, preserving the auto-regressive property.
*   **Attention Mechanisms:** The core of the Transformer, enabling it to weigh the importance of different input or output positions. This includes Scaled Dot-Product Attention and Multi-Head Attention, which allows attending to information from different representation subspaces.
*   **Positional Encoding:** Since the model lacks recurrence, positional encodings (using sine and cosine functions) are added to the input embeddings to inject information about the relative or absolute positions of tokens.
*   **Optimizer:** The Adam optimizer is used with a specific learning rate schedule that increases the learning rate linearly for an initial period and then decreases it proportionally to the inverse square root of the step number.
*   **Regularization:** Techniques like dropout and label smoothing are applied to prevent overfitting and improve model performance.

## Role in Context
The Transformer architecture represented a significant shift in sequence modeling, particularly in natural language processing. The Transformer architecture has since become the foundation for many subsequent influential models, including BERT, GPT, and T5, driving progress in a wide range of NLP tasks.

## Related Concepts
*   [[attention-mechanism|Attention Mechanism]]: A mechanism that allows a model to focus on specific parts of the input when processing a sequence.
*   [[self-attention|Self-Attention]]: A type of attention mechanism where the model relates different positions of a single sequence to compute its representation.
*   [[multi-head-attention|Multi-Head Attention]]: An extension of the attention mechanism that allows the model to jointly attend to information from different representation subspaces.
*   [[positional-encoding|Positional Encoding]]: A technique used to inject information about the order of tokens in a sequence into models that do not inherently process sequential data.
*   [[encoder-decoder-architecture|Encoder-Decoder Architecture]]: A common framework for sequence-to-sequence models where an encoder processes the input and a decoder generates the output.
*   [[adam-optimizer|Adam Optimizer]]: A popular optimization algorithm used for training neural networks.

## References
*   NIPS-2017-attention-is-all-you-need-Paper.pdf
