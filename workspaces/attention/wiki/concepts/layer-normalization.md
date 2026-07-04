---
title: Layer Normalization
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages: []
tags:
- normalization
- deep learning
confidence: high
updated: '2023-10-27'
---

Layer Normalization (LayerNorm) is a technique used in neural networks to stabilize training by normalizing the inputs to a layer across all of the features. This normalization is applied independently for each training example. In the context of the Transformer model, Layer Normalization is applied around each sub-layer (like the multi-head self-attention mechanism and the position-wise feed-forward network) before it is added to the sub-layer input and normalized. The output of each sub-layer is computed as LayerNorm(x + Sublayer(x)), where x is the input to the sub-layer and Sublayer(x) is the output of the sub-layer function. This helps to regulate the flow of information and prevent issues like vanishing or exploding gradients, contributing to faster convergence and improved performance during training. The Transformer model utilizes Layer Normalization with a dimension of dmodel = 512 for its sub-layers.
