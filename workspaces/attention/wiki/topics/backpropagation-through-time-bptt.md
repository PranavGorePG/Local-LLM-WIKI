---
title: Backpropagation Through Time (BPTT)
type: training algorithm
source_documents:
- self_attention_and_rnns.pdf
related_pages: []
tags:
- training
- RNN
---

[[Backpropagation Through Time (BPTT)]] is the standard algorithm used to train [[Recurrent Neural Network (RNN)|RNN]]s. It involves unrolling the recurrent network across all [[time step|time steps]] of the input sequence, effectively creating a deep feedforward network. Gradients are then computed using backpropagation and summed across the unrolled steps before updating the shared network weights. BPTT can be susceptible to the [[vanishing gradient problem]] and [[exploding gradient]] issues.
