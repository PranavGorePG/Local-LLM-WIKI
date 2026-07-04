---
title: Encoder-Decoder Attention
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- transformer
- attention-mechanism
tags:
- attention
- sequence-to-sequence
- encoder-decoder
---

Encoder-decoder attention is a mechanism used in sequence transduction models, particularly within the Transformer architecture, to allow the decoder to focus on relevant parts of the input sequence. In this setup, the queries are derived from the previous decoder layer's output, while the keys and values are sourced from the output of the encoder stack. This enables each position in the decoder to attend to all positions in the input sequence, mirroring traditional encoder-decoder attention mechanisms.

## Details
This mechanism is a crucial component of the Transformer's encoder-decoder architecture. It facilitates the flow of information from the encoder's representation of the input to the decoder's generation of the output. By allowing the decoder to selectively attend to different parts of the encoded input, it helps in tasks like machine translation where the alignment between source and target sequences is not always one-to-one.

## Role in Context
Encoder-decoder attention is vital for sequence-to-sequence tasks. It bridges the gap between the encoder's understanding of the input and the decoder's need to generate a corresponding output. The Transformer leverages this form of attention extensively, replacing recurrent and convolutional layers to achieve state-of-the-art results in translation.
