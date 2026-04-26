---
title: Attention Window
type: Concept
source_documents:
- Attention_Mechanisms_Perspective_Exploring_LLM_Pro.pdf
related_pages:
- Attention Mechanism
- Large Language Models (LLMs)
- Graph Neural Networks (GNNs)
- Graph-structured data
tags:
- Attention
- LLMs
- GNNs
- Connectivity
---

An [[Attention Window]] defines the visibility range between tokens (or nodes) within a single layer of a neural network, determining how a model captures relationships. In traditional [[Large Language Models (LLMs)]] like BERT, the attention window is often bidirectionally fully connected, allowing each token to attend to all others. GPT-series models use a unidirectional causal mask, restricting attention to preceding tokens. In contrast, [[Graph Neural Networks (GNNs)]] define visibility based on fixed connections, where each node only attends to its directly linked neighbors.Research by Guan et al. (2025) explores the optimal [[Attention Window]] for LLMs when processing [[Graph-structured data]]. They introduce the Global Linkage Horizon (GLH) to measure this visibility. Their findings indicate that neither the fully connected view of LLMs nor the fixed-linkage view of GNNs is optimal. Instead, intermediate attention windows that incorporate certain topological link information achieve superior performance during training. Notably, models trained with smaller linkage horizons can be effectively deployed with larger ones, demonstrating beneficial transferability and addressing practical deployment challenges. This suggests that tailoring the attention window can significantly impact an LLM's understanding and utilization of graph structures.
