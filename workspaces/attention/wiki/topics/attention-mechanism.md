---
title: Attention Mechanism
type: Concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
- Attention_Mechanisms_Perspective_Exploring_LLM_Pro.pdf
related_pages:
- Transformer Architecture
- Self-Attention
- Multi-Head Attention
- Scaled Dot-Product Attention
- Large Language Models (LLMs)
- Graph Neural Networks (GNNs)
- Graph-structured data
- Attention Sink
- Skewed Line Sink
- Attention Window
- NIPS 2017 Attention Is All You Need Paper
- 'Attention Mechanisms Perspective: Exploring LLM Processing of Graph-Structured
  Data (Guan et al. 2025)'
tags:
- Machine Learning
- Neural Networks
- NLP
- LLMs
- Graphs
---

The [[Attention Mechanism]] is a crucial component in neural networks, particularly in sequence modeling and transduction problems. It allows a model to focus on specific parts of an input sequence when processing another sequence, rather than having to encode the entire input into a single fixed-length vector. This is especially important for long sequences, as it helps in modeling dependencies regardless of their distance. The mechanism works by computing a weighted sum of 'value' vectors, where the weights are determined by the compatibility between a 'query' vector and 'key' vectors. This capability is fundamental to the success of models like the [[Transformer Architecture]], where it entirely replaces recurrence and convolutions, as detailed in "[[Attention Is All You Need]]" (Vaswani et al., 2017).Attention mechanisms come in various forms, including [[Self-Attention]], [[Scaled Dot-Product Attention]], and [[Multi-Head Attention]]. While highly effective in natural language processing, their application to [[Graph-structured data]] in [[Large Language Models (LLMs)]] presents unique challenges. Research by Guan et al. (2025) indicates that traditional LLM attention struggles to model inter-node relationships in graphs, exhibiting phenomena like "[[Attention Sink]]" and "[[Skewed Line Sink]]" where attention distribution deviates from ideal graph topology. This suggests that for graph data, a model's [[Attention Window]] – the visible range between tokens – needs to be carefully considered, with intermediate perspectives often outperforming fully connected or fixed-linkage approaches. This highlights a nuanced understanding of attention, where its effectiveness can vary significantly depending on the data structure and specific task.
