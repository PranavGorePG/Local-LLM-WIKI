---
title: Update gate
type: model component
source_documents:
- self_attention_and_rnns.pdf
related_pages: []
tags:
- GRU
- model component
---

The [[update gate]] in a [[Gated Recurrent Unit (GRU)]] determines how much of the previous [[hidden state]] should be carried over to the current [[hidden state]]. It balances the amount of new information to incorporate versus how much of the old information to retain, similar to the combined function of the input and forget gates in [[Long Short-Term Memory (LSTM)|LSTMs]].
