---
title: Skewed Line Sink
type: Concept
source_documents:
- Attention_Mechanisms_Perspective_Exploring_LLM_Pro.pdf
related_pages:
- Attention Mechanism
- Large Language Models (LLMs)
- Attention Sink
- Graph-structured data
tags:
- Attention
- LLMs
- Bias
- Graph-structured data
---

The [[Skewed Line Sink]] is a unique phenomenon identified by Guan et al. (2025) in the [[Attention Mechanism]]s of [[Large Language Models (LLMs)]] when processing [[Graph-structured data]]. It manifests as a diagonal with notably higher attention scores in the attention interaction matrix, distinct from simple adjacency relationships or the main diagonal where nodes attend to their immediate neighbors.This pattern, not typically found in textual attention analyses, suggests that LLMs might be learning unexpected spatial patterns or path dependencies inherent to the graph structure. Like the general "[[Attention Sink]]", the [[Skewed Line Sink]] interferes with the effective utilization of graph structural information by LLMs, preventing proper attention allocation between nodes. Understanding and correcting such biases is crucial for improving LLM performance on graph machine learning tasks.
