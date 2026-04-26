---
title: Graph-structured data
type: Topic
source_documents:
- Attention_Mechanisms_Perspective_Exploring_LLM_Pro.pdf
related_pages:
- Large Language Models (LLMs)
- Graph Neural Networks (GNNs)
- Attention Mechanism
- Attention Sink
- Skewed Line Sink
- Attention Window
tags:
- Graphs
- Data Structures
- Machine Learning
---

[[Graph-structured data]] represents information as a collection of nodes (entities) and edges (relationships between entities), making it ubiquitous in various domains like social networks, biological networks, and knowledge graphs. Processing such data effectively requires models to emphasize topological connections and inter-node relationships.While [[Large Language Models (LLMs)]] excel in sequential language processing, their application to graph-structured data presents unique challenges. Guan et al. (2025) reveal that LLMs, despite recognizing graph data and capturing text-node interactions, often struggle to accurately model the complex inter-node relationships essential to graph structures. This limitation stems from inherent architectural constraints and manifests in attention distribution patterns like "[[Attention Sink]]" and "[[Skewed Line Sink]]", which deviate from ideal graph-adaptive attention. In contrast, [[Graph Neural Networks (GNNs)]] are specifically designed for graph-structured data, utilizing message-passing mechanisms over fixed links. Research suggests that for LLMs to effectively leverage graph-structured data, modifications to their [[Attention Window]]s to incorporate topological information are beneficial, bridging the gap between sequential and graph-aware processing.
