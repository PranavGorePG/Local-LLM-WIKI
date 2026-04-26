---
title: Convolutional Neural Networks (CNNs) in Sequence Models
type: Concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- Recurrent Neural Networks (RNNs)
- Transformer Architecture
- Attention Mechanism
- NIPS 2017 Attention Is All You Need Paper
tags:
- Neural Networks
- Deep Learning
- Sequence Models
---

While primarily known for image processing, [[Convolutional Neural Networks (CNNs) in Sequence Models]] have also been applied to sequence transduction tasks, offering an alternative to [[Recurrent Neural Networks (RNNs)]]. Models like ByteNet and ConvS2S use convolutional layers as their basic building block, computing hidden representations in parallel for all input and output positions. This parallel computation can offer advantages over the sequential nature of RNNs.However, in these models, the number of operations required to relate signals from two arbitrary input or output positions typically grows with the distance between positions (linearly for ConvS2S, logarithmically for ByteNet), making it potentially more difficult to learn dependencies between very distant positions. To connect all pairs of input and output positions, a stack of O(n/k) convolutional layers (contiguous kernels) or O(logk(n)) layers (dilated convolutions) might be required, increasing the path length for long-range dependencies. The [[Transformer Architecture]], introduced in "[[Attention Is All You Need]]" (Vaswani et al., 2017), contrasts with these approaches by using [[Attention Mechanism]]s, which directly relate all positions with a constant number of operations, providing a shorter path length for learning long-range dependencies.
