---
title: Positional Encoding
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- Transformer Architecture
tags:
- neural networks
- deep learning
- sequence transduction
---

Since the [[Transformer Architecture]] contains no recurrence and no convolution, it requires a mechanism to incorporate information about the relative or absolute position of tokens in the sequence. This is achieved through [[Positional Encoding]]. These encodings are added to the input embeddings at the bottom of both the encoder and decoder stacks. Method: The Transformer uses sine and cosine functions of different frequencies for positional encoding: `PE(pos, 2i) = sin(pos / 10000^(2i/dmodel))` `PE(pos, 2i+1) = cos(pos / 10000^(2i/dmodel))` where `pos` is the position and `i` is the dimension. Each dimension of the positional encoding corresponds to a sinusoid, with wavelengths forming a geometric progression. Rationale: This choice allows the model to easily learn to attend by relative positions, as `PEpos+k` can be represented as a linear function of `PEpos`. Alternatives: Learned positional embeddings were also experimented with but yielded nearly identical results to the sinusoidal version. The sinusoidal approach was preferred for its potential to extrapolate to sequence lengths longer than those encountered during training. The positional encodings have the same dimension (`dmodel`) as the embeddings, allowing them to be summed.
