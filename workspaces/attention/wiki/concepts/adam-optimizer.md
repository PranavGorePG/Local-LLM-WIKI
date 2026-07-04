---
title: Adam Optimizer
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- batching
- optimization
tags:
- optimization
- deep learning
- training
- stochastic optimization
confidence: high
updated: '2023-10-27'
---

The Adam (Adaptive Moment Estimation) optimizer is a popular and effective algorithm for stochastic optimization in deep learning. It adapts the learning rate for each parameter based on estimates of both the first and second moments of the gradients. This adaptive approach allows Adam to converge quickly and efficiently, even in the presence of noisy or sparse gradients, and it often performs well across a wide range of deep learning tasks and architectures.

The "Attention Is All You Need" paper specifies the use of the Adam optimizer for training their Transformer models. They employed Adam with specific hyperparameter values: \(\beta_1 = 0.9\), \(\beta_2 = 0.98\), and \(\epsilon = 10^{-9}\). Furthermore, they implemented a dynamic learning rate schedule that increased the learning rate linearly for the first \(4000\) training steps (warmup steps) and then decreased it proportionally to the inverse square root of the step number. This learning rate scheduling is crucial for stable and effective training, particularly in the early stages, helping the model to learn without diverging and then fine-tuning the weights for optimal performance. The choice of Adam and this specific learning rate strategy contributed to the model's training efficiency and final performance.
