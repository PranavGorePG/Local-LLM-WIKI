---
title: Cell state
type: model state
source_documents:
- self_attention_and_rnns.pdf
related_pages: []
tags:
- LSTM
- model state
---

The [[cell state]] is a core component of [[Long Short-Term Memory (LSTM)]] networks. It acts as a long-term memory that runs through the entire sequence, allowing information to be carried forward with minimal degradation. The [[input gate]], [[forget gate]], and [[output gate]] control the flow of information into, out of, and within the cell state, making LSTMs effective at learning [[long-range dependency|long-range dependencies]].
