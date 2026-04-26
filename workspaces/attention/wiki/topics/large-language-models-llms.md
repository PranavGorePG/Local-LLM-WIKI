---
title: Large Language Models (LLMs)
type: Concept
source_documents:
- Attention_Mechanisms_Perspective_Exploring_LLM_Pro.pdf
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- Attention Mechanism
- Transformer Architecture
- Graph-structured data
- Attention Sink
- Attention Window
- Graph Neural Networks (GNNs)
tags:
- LLMs
- NLP
- Deep Learning
- Transformers
---

[[Large Language Models (LLMs)]] are advanced neural networks, often built upon the [[Transformer Architecture]], that have achieved remarkable success in various natural language processing tasks. Their efficacy is largely driven by sophisticated [[Attention Mechanism]]s, which enable them to comprehend complex contexts by linking tokens across long sequences.While highly successful in language processing, research by Guan et al. (2025) indicates that LLMs face specific challenges when processing [[Graph-structured data]]. They demonstrate that while LLMs can recognize graph data and understand interactions between text and nodes, they often struggle to accurately model inter-node relationships within the graph topology. This limitation is partly attributed to inherent architectural constraints and manifests in phenomena like "[[Attention Sink]]" and "[[Skewed Line Sink]]" in their attention distributions, which deviate from ideal structural patterns for graphs. The study suggests that for graph-structured tasks, intermediate [[Attention Window]]s incorporating topological information can be more effective than the fully connected attention commonly found in LLMs, highlighting a key area for improvement in LLM applications beyond traditional text.
