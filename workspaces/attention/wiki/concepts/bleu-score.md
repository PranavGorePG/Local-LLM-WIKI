---
title: BLEU Score
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- Machine Translation
- Transformer Architecture
tags:
- evaluation metric
- natural language processing
---

The [[BLEU Score]] (Bilingual Evaluation Understudy) is an algorithm for evaluating the quality of text which has been machine-translated from one natural language to another. It is a widely used metric in the field of [[Machine Translation]] to assess how closely a machine-translated text resembles a set of high-quality human translations. Key Features: Measures the precision of n-grams (sequences of words) in the machine translation compared to reference translations. Includes a brevity penalty to prevent very short translations from getting high scores. A higher BLEU score indicates a translation that is closer to a professional human translation. In the "[[NIPS 2017 Attention Is All You Need Paper]]", the [[Transformer Architecture]] achieved state-of-the-art BLEU scores on various machine translation benchmarks, demonstrating its superior performance.
