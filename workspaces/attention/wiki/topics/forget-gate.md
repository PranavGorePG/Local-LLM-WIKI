---
title: Forget gate
type: model component
source_documents:
- self_attention_and_rnns.pdf
related_pages: []
tags:
- LSTM
- model component
---

The [[forget gate]] is a gating mechanism in a [[Long Short-Term Memory (LSTM)]] cell responsible for deciding which information to throw away from the [[cell state]]. It looks at the previous [[hidden state]] and the current input and outputs a number between 0 and 1 for each number in the [[cell state]]. A 1 means "completely keep this" and a 0 means "completely get rid of this." This allows LSTMs to selectively forget irrelevant information.
