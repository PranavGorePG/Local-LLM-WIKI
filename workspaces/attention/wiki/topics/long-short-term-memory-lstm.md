---
title: Long Short-Term Memory (LSTM)
type: model architecture
source_documents:
- self_attention_and_rnns.pdf
related_pages: []
tags:
- RNN
- deep learning
---

[[Long Short-Term Memory (LSTM)]] is a type of [[Recurrent Neural Network (RNN)|RNN)]] architecture designed to effectively learn [[long-range dependency|long-range dependencies]] and overcome the [[vanishing gradient problem]]. LSTMs introduce a [[cell state]] alongside the [[hidden state]], which acts as a conveyor belt for information. This cell state is regulated by three key gates: the [[input gate]], [[forget gate]], and [[output gate]], which explicitly control what information is added to, removed from, or outputted from the cell state.
