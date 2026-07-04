---
title: Machine Translation
type: topic
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- transformer
- attention-mechanism
- bleu-score
- beam-search
- wmt-2014-english-german
- wmt-2014-english-french
tags:
- nlp
- sequence modeling
- translation
updated: '2023-10-27'
---

Machine translation is a subfield of computational linguistics that deals with the automatic translation of human language. This involves converting text or speech from one language (the source language) to another language (the target language) using software. Dominant sequence transduction models, such as those based on recurrent or convolutional neural networks, have historically been employed for these tasks. These models typically incorporate an encoder-decoder structure. Recent advancements have seen architectures solely based on attention mechanisms, like the Transformer, achieve state-of-the-art results by dispensing with recurrence and convolutions entirely. These attention-based models often require less training time and can be more parallelizable, leading to significant improvements in translation quality.
