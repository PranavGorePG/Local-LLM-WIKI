---
title: Development Set
type: topic
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- hyperparameter-tuning
- model-evaluation
tags:
- evaluation
- training
confidence: High
updated: '2023-10-27'
---

A development set, often referred to as a validation set, is a subset of the training data used to tune hyperparameters and evaluate model performance during the development phase of a machine learning project. It helps in selecting the best model configuration before final evaluation on a separate test set.

## Definition
The development set is used to make decisions about the model architecture, hyperparameters, and training procedures. By evaluating the model on the development set, researchers can get an estimate of how the model will perform on unseen data without overfitting to the test set.

## Key Properties
In the "Attention Is All You Need" paper, hyperparameter choices such as beam search width and length penalty were determined after experimentation on the development set (newstest2013 for English-to-German translation). Model variations, such as changes in attention heads or dropout rates, were also evaluated using performance on the development set.

## Role in Context
The development set plays a crucial role in the iterative process of model development and tuning. It guides the selection of optimal hyperparameters and model configurations, ensuring that the final model generalizes well to new data.

## Related Concepts
* [[hyperparameter-tuning|Hyperparameter Tuning]]: The process of selecting the optimal values for hyperparameters, often guided by performance on a development set.
* [[model-evaluation|Model Evaluation]]: The process of assessing a model's performance, typically using development and test sets.

## References
* NIPS-2017-attention-is-all-you-need-Paper.pdf
