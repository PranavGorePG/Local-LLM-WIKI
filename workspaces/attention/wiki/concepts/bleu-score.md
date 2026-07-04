---
title: BLEU Score
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- machine-translation
- transformer
tags:
- evaluation metric
- machine translation
---

BLEU (Bilingual Evaluation Understudy) is an algorithm for evaluating the quality of machine-translated text. It measures the similarity between a machine-generated translation and one or more human-created reference translations. The score is based on the precision of n-grams (contiguous sequences of n words) in the machine translation compared to the reference translations, with a penalty for translations that are too short.

BLEU scores range from 0 to 1, with higher scores indicating better translation quality. It is a widely used metric in machine translation research for comparing different models and approaches. The paper "Attention Is All You Need" reports BLEU scores for its Transformer models on tasks like the WMT 2014 English-to-German translation, achieving a state-of-the-art score of 28.4.
