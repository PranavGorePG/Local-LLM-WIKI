---
title: Checkpoint Averaging
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- training
tags:
- training
- optimization
confidence: High
updated: '2023-10-27'
---

Checkpoint averaging is a technique used in training deep learning models to improve generalization and robustness. It involves averaging the model weights from several intermediate checkpoints saved during training.

## Definition
During the training process, models are periodically saved as checkpoints. Checkpoint averaging takes multiple of these saved models (often the last few or those from specific intervals) and computes their average weights. This averaged model is then used for evaluation or further fine-tuning.

## Key Properties
In the "Attention Is All You Need" paper, checkpoint averaging was used for evaluation. For the base models, the last 5 checkpoints, saved at 10-minute intervals, were averaged. For the big models, the last 20 checkpoints were averaged. This process is typically done after training is completed and before hyperparameter tuning on the development set, though in this paper, it seems to be part of the evaluation setup.

## Role in Context
Checkpoint averaging helps to smooth out the optimization landscape and can lead to a more stable and performant final model. It leverages the knowledge captured across different stages of the training process.

## Related Concepts
* [[training|Training]]: The overall process where checkpoints are generated.
* [[model-evaluation|Model Evaluation]]: Checkpoint averaging is often part of the evaluation pipeline.

## References
* NIPS-2017-attention-is-all-you-need-Paper.pdf
