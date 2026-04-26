---
title: Attention Sink
type: Concept
source_documents:
- Attention_Mechanisms_Perspective_Exploring_LLM_Pro.pdf
related_pages:
- Attention Mechanism
- Large Language Models (LLMs)
- Skewed Line Sink
- Attention Window
tags:
- Attention
- LLMs
- Bias
- Graph-structured data
---

An [[Attention Sink]] is a phenomenon observed in [[Attention Mechanism]]s, particularly within [[Large Language Models (LLMs)]], where certain tokens or positions consistently attract disproportionately higher attention scores without significant semantic, topological, or sequential justification. Initially identified in natural language processing (NLP) for semantically limited initial tokens (Xiao et al., 2024), the concept has also been extended to [[Graph-structured data]].In the context of graph data, Guan et al. (2025) describe a simple "Attention Sink" where specific positions within the graph's tokenized representation consistently receive high attention scores. This phenomenon, along with the "[[Skewed Line Sink]]", can interfere with the proper allocation of attention between nodes, hindering LLMs' ability to effectively utilize graph structural information. Correcting these biases is an active area of research to improve model performance.
