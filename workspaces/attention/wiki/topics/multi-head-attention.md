---
title: Multi-Head Attention
type: model architecture component
source_documents:
- self_attention_and_rnns.pdf
related_pages: []
tags:
- self-attention
- Transformer
---

[[Multi-Head Attention]] is a component of the [[Transformer architecture]] that enhances [[Self-attention]] by allowing the model to jointly attend to information from different representation subspaces at different positions. It works by running the self-attention mechanism multiple times in parallel with different, learned linear projections of the Queries, Keys, and Values. Each "head" can potentially learn to focus on different types of relationships or aspects of the input sequence.
