---
title: Learning Rate
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages: []
tags:
- optimization
- training
confidence: High
updated: '2023-10-27'
---

The learning rate is a hyperparameter that controls how much the model's weights are updated with respect to the loss gradient during training. In the "Attention Is All You Need" paper, the Adam optimizer was used with a dynamic learning rate that varied over the course of training.

## Definition
The learning rate determines the step size taken by the optimization algorithm when updating model weights. A higher learning rate can lead to faster convergence but may overshoot the optimal solution, while a lower learning rate can result in slower convergence but a more precise final solution.

## Key Properties
In the context of the Transformer model, the learning rate was adjusted using a specific formula:

lrate = d⁻⁰.⁵
model
· min(step_num⁻⁰.⁵, step_num · warmup_steps⁻¹⁵)

This formula involves a warm-up period where the learning rate increases linearly for a set number of training steps (`warmup_steps`), followed by a decrease proportional to the inverse square root of the step number. For the Transformer, `warmup_steps` was set to 4000.

## Role in Context
The learning rate is a critical hyperparameter in training deep learning models, including the Transformer. Proper tuning of the learning rate and its schedule is essential for achieving optimal performance and efficient training.

## Related Concepts
* [[Adam Optimizer|Adam]]: An optimization algorithm used in conjunction with a specific learning rate schedule.
* [[Training|Training]]: The process of adjusting model parameters to minimize a loss function, heavily influenced by the learning rate.

## References
* NIPS-2017-attention-is-all-you-need-Paper.pdf
