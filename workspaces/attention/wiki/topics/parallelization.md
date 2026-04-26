---
title: Parallelization
type: computational method
source_documents:
- self_attention_and_rnns.pdf
related_pages: []
tags:
- computation
- efficiency
---

[[Parallelization]] is a computational method where multiple computations are performed simultaneously. In [[Self-attention]], all tokens in an [[input sequence]] can be processed in parallel, as the attention calculation for each token is independent of the others once Q, K, and V vectors are formed. This significantly speeds up training compared to [[Recurrent Neural Network (RNN)|RNN]]s, which process sequences [[sequential processing|sequentially]].
