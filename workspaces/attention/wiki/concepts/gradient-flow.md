---
title: Gradient Flow
type: concept
source_documents:
- NIPS-2017-attention-is-all-you-need-Paper.pdf
related_pages:
- long-range-dependencies
- recurrent-neural-network
- transformer
- residual-connection
tags:
- neural networks
- deep learning
- training
updated: '2023-10-27'
---

Gradient flow refers to the propagation of gradients during the backpropagation process in neural networks. It is a critical factor in a model's ability to learn, especially concerning the capture of long-range dependencies.

## Overview
In deep neural networks, training involves computing gradients of the loss function with respect to the network's parameters. These gradients flow backward from the output layer to the input layer. The ease or difficulty with which gradients can flow through multiple layers significantly impacts learning. Issues like vanishing or exploding gradients can hinder the learning of complex patterns, particularly those spanning long distances in a sequence or data structure.

## Key Properties
- **Vanishing Gradients**: Gradients become exponentially smaller as they propagate backward, making it difficult to update weights in earlier layers. This is common in very deep recurrent networks.
- **Exploding Gradients**: Gradients become exponentially larger, leading to unstable training.
- **Path Length**: The number of sequential operations or layers between two points in a network determines the path length for gradient flow. Shorter paths generally facilitate easier learning of dependencies.

## Role in Context
The difficulty of learning long-term dependencies is closely related to gradient flow issues in recurrent neural networks (RNNs). The sequential nature of RNNs often results in long paths for gradients, exacerbating the vanishing gradient problem. The Transformer architecture, by using self-attention, aims to alleviate this by creating constant-length paths between any two positions, thereby improving gradient flow and making it easier to learn long-range dependencies compared to traditional RNNs.
