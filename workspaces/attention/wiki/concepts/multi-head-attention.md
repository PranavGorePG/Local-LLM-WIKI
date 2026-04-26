---
title: Multi-Head Attention
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- Attention Mechanism
- Self-Attention
- Transformer Architecture
- Scaled Dot-Product Attention
tags:
- neural networks
- deep learning
- sequence transduction
---

[[Multi-Head Attention]] is an extension of the [[Attention Mechanism]] used in the [[Transformer Architecture]] that improves the model's ability to jointly attend to information from different representation subspaces at different positions. Instead of performing a single attention function on `dmodel`-dimensional keys, values, and queries, it performs `h` parallel attention layers, or "heads". Process: 1. The queries, keys, and values are linearly projected `h` times with different learned projections to lower dimensions (`dk`, `dk`, `dv`). 2. On each of these projected versions, a [[Scaled Dot-Product Attention]] function is applied in parallel, yielding `dv`-dimensional output values. 3. These `h` output values are then concatenated and once again linearly projected to produce the final result. Benefits: Allows the model to focus on different aspects of the information simultaneously. Averages attention from various perspectives, which helps overcome the limitation of a single attention head where averaging might inhibit diverse attending. The paper "[[NIPS 2017 Attention Is All You Need Paper]]" uses `h = 8` parallel attention layers, with `dk = dv = dmodel/h = 64`. Despite multiple heads, the total computational cost is similar to single-head attention with full dimensionality due to the reduced dimensions per head.
