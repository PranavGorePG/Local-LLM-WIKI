---
title: NVIDIA P100 GPUs
type: entity
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- transformer
tags:
- hardware
- gpu
- computation
confidence: high
updated: '2023-10-27'
---

NVIDIA P100 GPUs (Graphics Processing Units) are high-performance hardware accelerators designed for deep learning, high-performance computing, and scientific research. Based on NVIDIA's Pascal architecture, the P100 offered significant improvements in processing power and memory bandwidth compared to previous generations, making them well-suited for training large and complex neural networks.

The "Attention Is All You Need" paper highlights the use of NVIDIA P100 GPUs in their training setup. Specifically, the paper mentions training their models on "one machine with 8 NVIDIA P100 GPUs." For their "big" Transformer models, training took 3.5 days on these GPUs. The paper also provides estimated sustained single-precision floating-point capacities for various GPUs, including the P100, which was valued at 9.5 TFLOPS. The availability and performance of such hardware were critical factors enabling the researchers to train the large Transformer models and achieve state-of-the-art results in machine translation within a reasonable timeframe.
