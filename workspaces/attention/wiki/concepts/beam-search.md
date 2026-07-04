---
title: Beam Search
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- machine-translation
- transformer
tags:
- decoding
- machine translation
confidence: High
updated: '2023-10-27'
---

Beam search is a heuristic search algorithm used in sequence generation tasks, such as machine translation, to find a likely output sequence. It is a generalization of greedy search that explores multiple hypotheses simultaneously.

## Definition
Instead of selecting only the most probable next token at each step (as in greedy search), beam search maintains a fixed number of the most probable partial sequences (the "beam width"). At each step, it expands each of these sequences by considering all possible next tokens and keeps the top-k most probable overall sequences to form the next beam.

## Key Properties
In the "Attention Is All You Need" paper, beam search with a beam size of 4 and a length penalty (α) of 0.6 was used for inference. The maximum output length during inference was set to the input length plus 50, with early termination when possible.

## Role in Context
Beam search is employed during the decoding phase of the Transformer model for machine translation tasks to generate the most probable output sentence. It offers a trade-off between computational cost and the quality of the generated sequence compared to greedy search or exhaustive search.

## Related Concepts
* [[greedy-search|Greedy Search]]: A simpler decoding strategy that always selects the most probable next token.
* [[machine-translation|Machine Translation]]: A task where beam search is commonly used for decoding.

## References
* NIPS-2017-attention-is-all-you-need-Paper.pdf
