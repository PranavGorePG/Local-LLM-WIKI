---
title: Label Smoothing
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages: []
tags:
- regularization
- training
confidence: High
updated: '2023-10-27'
---

Label smoothing is a regularization technique applied during training that prevents the model from becoming too confident in its predictions. Instead of using hard targets (e.g., 0 or 1), it uses softened targets.

## Definition
Label smoothing modifies the target labels during training. For a classification task, instead of assigning a probability of 1 to the correct class and 0 to all others, it assigns a slightly smaller probability (e.g., 1 - ϵ) to the correct class and distributes the remaining probability (ϵ) across all other classes. In the "Attention Is All You Need" paper, a label smoothing value (ϵls) of 0.1 was employed.

## Key Properties
Using label smoothing can lead to a decrease in perplexity, as the model learns to be more uncertain. However, it has been shown to improve accuracy and BLEU scores, as observed in the context of machine translation.

## Role in Context
Label smoothing is used as a regularization method in the Transformer's training process to encourage more robust and less overconfident predictions, ultimately leading to better performance on downstream tasks like machine translation.

## Related Concepts
* [[Perplexity|Perplexity]]: A measure of how well a probability model predicts a sample, often used in language modeling. Label smoothing can affect perplexity.
* [[Regularization|Regularization]]: Techniques used to prevent overfitting and improve the generalization of machine learning models.

## References
* NIPS-2017-attention-is-all-you-need-Paper.pdf
