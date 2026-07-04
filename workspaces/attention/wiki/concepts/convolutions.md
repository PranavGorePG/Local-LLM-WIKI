---
title: Convolutions
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- transformer
- convolutional-neural-network
tags:
- neural networks
- sequence modeling
updated: '2023-10-27'
---

Convolutions, particularly in the form of Convolutional Neural Networks (CNNs), have been employed in sequence modeling tasks to capture local patterns and dependencies within data. In sequence transduction, CNN-based models compute hidden representations in parallel for all positions, with the number of operations required to relate distant positions growing linearly or logarithmically with the distance. This contrasts with recurrent models, which process sequences step-by-step.

While CNNs offer some degree of parallelization compared to pure recurrence, they can still struggle with learning long-range dependencies efficiently. The Transformer architecture, by contrast, abandons convolutions entirely, relying solely on attention mechanisms. This allows the Transformer to relate signals from any two positions with a constant number of operations, thus simplifying the learning of long-range dependencies and enabling greater parallelization.
