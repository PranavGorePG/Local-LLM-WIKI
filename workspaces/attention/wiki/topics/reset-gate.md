---
title: Reset gate
type: model component
source_documents:
- self_attention_and_rnns.pdf
related_pages: []
tags:
- GRU
- model component
---

The [[reset gate]] in a [[Gated Recurrent Unit (GRU)]] controls how much of the previous [[hidden state]] should be ignored. When the reset gate is close to 0, it effectively forgets the previous hidden state, allowing the GRU to capture new relevant information. This helps GRUs manage dependencies in [[sequential data]].
