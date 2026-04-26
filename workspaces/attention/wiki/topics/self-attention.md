---
title: Self-Attention
type: Concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
- Attention_Mechanisms_Perspective_Exploring_LLM_Pro.pdf
related_pages:
- Attention Mechanism
- Transformer Architecture
- Multi-Head Attention
- Scaled Dot-Product Attention
- Large Language Models (LLMs)
- Graph-structured data
- NIPS 2017 Attention Is All You Need Paper
- 'Attention Mechanisms Perspective: Exploring LLM Processing of Graph-Structured
  Data (Guan et al. 2025)'
tags:
- Attention
- Neural Networks
- NLP
- LLMs
- Graphs
---

[[Self-Attention]], sometimes referred to as intra-attention, is an [[Attention Mechanism]] that relates different positions of a single sequence to compute a representation of that same sequence. It allows the model to weigh the importance of different words or tokens in the input sentence relative to each other when encoding a particular word. For example, if translating the sentence "The animal didn't cross the street because it was too tired," self-attention helps determine that "it" refers to "animal." This mechanism is a core component of the [[Transformer Architecture]], enabling it to model long-range dependencies without the need for recurrence or convolutions, as described in "[[Attention Is All You Need]]" (Vaswani et al., 2017).In the context of [[Large Language Models (LLMs)]] and [[Graph-structured data]], while self-attention allows LLMs to recognize graph data and capture text-node interactions, research by Guan et al. (2025) suggests it struggles to effectively model inter-node relationships. The distribution of self-attention scores on graph nodes can deviate from ideal structural patterns, indicating limitations in adapting to graph topology nuances.
