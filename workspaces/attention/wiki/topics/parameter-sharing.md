---
title: Parameter sharing
type: training technique
source_documents:
- self_attention_and_rnns.pdf
related_pages: []
tags:
- training
- efficiency
---

[[Parameter sharing]] is a technique where the same set of model parameters (weights and biases) are used multiple times within a model. In [[Recurrent Neural Network (RNN)|RNN]]s, the weight matrices are shared across all [[time step|time steps]], which makes the model parameter-efficient and allows it to handle sequences of varying lengths. This contrasts with [[Self-attention]], where parameters are typically learned for query, key, and value transformations, and potentially for multiple heads.
