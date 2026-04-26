---
title: Exploding gradient
type: training problem
source_documents:
- self_attention_and_rnns.pdf
related_pages: []
tags:
- training
- RNN
- deep learning
---

The [[exploding gradient]] problem is the opposite of the [[vanishing gradient problem]] and occurs when gradients become excessively large during neural network training. This can cause large weight updates, leading to unstable training and divergence. It is a concern particularly in [[Recurrent Neural Network (RNN)|RNN]]s trained with [[Backpropagation Through Time (BPTT)]]. Techniques like gradient clipping are often used to mitigate this issue.
