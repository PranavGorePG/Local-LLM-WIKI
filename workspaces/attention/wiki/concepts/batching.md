---
title: Batching
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- training-data
- adam-optimizer
tags:
- machine learning
- deep learning
- training
- optimization
confidence: high
updated: '2023-10-27'
---

Batching is a fundamental technique in machine learning and deep learning training processes. Instead of processing individual data points one by one, batching groups a number of training examples together into a "mini-batch." The model then computes gradients and updates its weights based on this mini-batch. This approach offers several advantages over processing single instances:

1.  **Computational Efficiency**: Modern hardware, especially GPUs, are highly optimized for parallel computations. Processing data in batches allows for more efficient utilization of this parallel processing power, leading to faster training times.
2.  **Gradient Stability**: While processing single examples can lead to noisy gradient updates, batching averages the gradients over multiple examples, resulting in more stable and reliable convergence towards a good minimum.
3.  **Memory Management**: Batching helps manage memory usage by loading only a subset of the training data into memory at a time. The size of the batch is a hyperparameter that needs to be tuned, balancing computational efficiency with memory constraints and gradient quality.

The "Attention Is All You Need" paper mentions that sentence pairs were batched together by approximate sequence length. Each training batch contained a set of sentence pairs with approximately 25,000 source tokens and 25,000 target tokens. This grouping by sequence length can further optimize training by minimizing padding, which is often necessary when sequences within a batch have varying lengths. Effective batching is crucial for efficient and stable training of large neural networks.
