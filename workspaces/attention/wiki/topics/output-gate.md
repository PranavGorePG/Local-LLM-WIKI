---
title: Output gate
type: model component
source_documents:
- self_attention_and_rnns.pdf
related_pages: []
tags:
- LSTM
- model component
---

The [[output gate]] is one of the gating mechanisms in a [[Long Short-Term Memory (LSTM)]] cell. It determines what parts of the [[cell state]] should be outputted as the new [[hidden state]]. It filters the updated cell state based on the current input and previous hidden state, controlling which information is passed on to the next time step.
