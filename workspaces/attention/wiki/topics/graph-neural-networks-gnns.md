---
title: Graph Neural Networks (GNNs)
type: Concept
source_documents:
- Attention_Mechanisms_Perspective_Exploring_LLM_Pro.pdf
related_pages:
- Graph-structured data
- Attention Mechanism
- Large Language Models (LLMs)
- Attention Window
tags:
- GNNs
- Graph Theory
- Deep Learning
- Machine Learning
---

[[Graph Neural Networks (GNNs)]] are a class of neural networks designed to operate directly on [[Graph-structured data]]. They typically employ message-passing mechanisms to aggregate information from a node's fixed neighbors, making them inherently well-suited for capturing topological connections.In contrast to [[Large Language Models (LLMs)]] that primarily use [[Attention Mechanism]]s, GNNs' fixed-linkage perspective allows them to effectively utilize correct connectivity information within graphs. Research by Guan et al. (2025) explores the suitability of GNNs' fixed-linkage view versus LLMs' fully connected attention for graph-structured tasks. The study found that neither extreme is universally optimal, and intermediate [[Attention Window]]s, which can be seen as incorporating some principles of both, can achieve superior performance. This highlights the distinct strengths of GNNs in handling explicit graph topologies.
