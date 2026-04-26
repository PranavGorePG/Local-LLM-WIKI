---
title: Attention score
type: metric
source_documents:
- self_attention_and_rnns.pdf
related_pages: []
tags:
- self-attention
- attention mechanism
---

An [[attention score]] quantifies the relevance of one token to another within an [[input sequence]] during the [[Self-attention]] process. It is typically computed as the [[dot product]] between a token's [[Query (Q)|Query]] vector and another token's [[Key (K)|Key]] vector, often scaled by the [[key dimension]]. These scores are then normalized using the [[softmax operation]] to obtain attention weights.
