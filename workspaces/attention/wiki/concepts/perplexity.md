---
title: Perplexity
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- label-smoothing
- language-modeling
tags:
- evaluation
- language modeling
confidence: High
updated: '2023-10-27'
---

Perplexity is a common evaluation metric for language models. It quantifies how well a probability distribution or probability model predicts a sample. In the context of language modeling, lower perplexity indicates a better model.

## Definition
Perplexity is the exponentiated average negative log-likelihood of a sequence. For a sequence of words $W = w_1, w_2, 

..., w_N$, the perplexity is calculated as:

$PPL(W) = 

exp
\left(-
\frac{1}{N} 

\sum_{i=1}^{N} 

\log p(w_i | w_1, ..., w_{i-1})
\right)$

where $p(w_i | w_1, ..., w_{i-1})$ is the probability assigned to the $i$-th word given the preceding words.

## Key Properties
Lower perplexity values indicate that the language model is better at predicting the next word in a sequence. It is mentioned in the "Attention Is All You Need" paper that label smoothing can hurt perplexity because the model learns to be more unsure, but it improves accuracy and BLEU score.

## Role in Context
Perplexity is used to evaluate the quality of language models, which can be a component of larger sequence transduction systems. While the primary evaluation metric in the paper is BLEU score for machine translation, perplexity provides an intrinsic measure of language model performance.

## Related Concepts
* [[label-smoothing|Label Smoothing]]: A regularization technique that can affect perplexity.
* [[language-modeling|Language Modeling]]: The task of predicting the next word in a sequence, for which perplexity is a key evaluation metric.

## References
* NIPS-2017-attention-is-all-you-need-Paper.pdf
