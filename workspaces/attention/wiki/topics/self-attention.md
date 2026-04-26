---
title: Self-attention
type: model architecture
source_documents:
- self_attention_and_rnns.pdf
related_pages: []
tags:
- attention mechanism
- Transformer
---

Self-attention is an attention mechanism in [[machine learning model]]s that weighs the importance of tokens or words in an [[input sequence]] to better understand the relationships between them. Unlike processing tokens in isolation, self-attention allows every token to dynamically focus on every other token in the sequence, producing rich, context-aware representations. It was formally introduced in the 2017 paper "Attention Is All You Need," which proposed the [[Transformer architecture]] and eliminated the need for [[Recurrent Neural Network (RNN)|RNN]]s entirely.

The mechanism transforms each [[embedding]] token embedding into three vectors using learned [[weight matrix|weight matrices]]:
- Query (Q): Represents what the current token is "looking for."
- Key (K): Represents what each token "offers" or contains.
- Value (V): Represents the actual content to be aggregated.

The [[attention score]] between two tokens is computed as the [[dot product]] of their Query and Key vectors, scaled by the square root of the [[key dimension]]. The [[softmax operation]] normalizes the scores into a [[probability distribution]], and the final output is the [[weighted sum]] of Value vectors. This entire operation can be subject to [[parallelization]], giving self-attention a computational advantage over sequential models.

In practice, the Transformer stacks multiple self-attention "heads" in parallel, known as [[Multi-Head Attention]], each learning different aspects of token relationships. For example, one head might attend to syntactic dependencies (verbs to their objects), while another captures long-range semantic relationships. The outputs from all heads are concatenated and passed to a [[feedforward neural network layer]], allowing the model to combine multiple relational perspectives in a single forward pass.

Key Strengths:
- [[Parallelization]]: All tokens are processed simultaneously, enabling efficient training on large datasets.
- [[Long-range dependency]]: Captures relationships between distant tokens with equal ease as nearby ones.
- [[Context-sensitivity]]: The same word generates different representations depending on surrounding context.
- [[Interpretability]]: Attention weights provide insight into which token relationships the model finds most relevant.

Key Limitations:
- [[Quadratic complexity]]: Computing attention scores for all token pairs scales quadratically with [[sequence length]], making it expensive for very long sequences.
- No inherent positional awareness: Unlike RNNs, self-attention has no built-in notion of order, requiring explicit [[positional encoding]] to be added to the input.
