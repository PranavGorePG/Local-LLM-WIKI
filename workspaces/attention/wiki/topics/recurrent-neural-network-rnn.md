---
title: Recurrent Neural Network (RNN)
type: model architecture
source_documents:
- self_attention_and_rnns.pdf
related_pages: []
tags:
- sequence modeling
- deep learning
---

A [[Recurrent Neural Network (RNN)|RNN]] is a class of neural networks specifically designed for processing [[sequential data]], where the order of elements is crucial. Unlike standard feedforward networks, RNNs utilize a feedback loop, allowing information from previous [[time step|time steps]] to influence the current step via a [[hidden state]]. This internal memory enables them to capture context within sequences.

How RNNs Work:
At each time step $t$, an RNN updates its [[hidden state]] $h_t$ using both the current input $x_t$ and the previous hidden state $h_{t-1}$: $h_t = f(W_{hh}h_{t-1} + W_{xh}x_t + b_h)$. Here, $f$ is a [[non-linear activation function]] (commonly tanh or ReLU), and $W_{hh}$, $W_{xh}$, and $b_h$ are [[weight matrix|weight matrices]] and a bias vector, respectively, that are shared across all time steps. This [[parameter sharing]] allows RNNs to maintain a compact model size regardless of sequence length.

Training typically employs [[Backpropagation Through Time (BPTT)]], where the network is unrolled across all time steps to compute and sum error gradients before updating weights.

Key Strengths:
- [[Sequential processing]]: Inherently models the order of elements in data.

Key Limitations:
- Sequential processing: Each time step depends on the previous one, preventing [[parallelization]] and slowing training.
- [[Vanishing gradient problem]]/[[Exploding gradient]]: Standard RNNs struggle to retain information from distant time steps.
- [[Long-sequence bottleneck]]: Even variants like LSTMs can degrade on very long sequences, as the entire context must be compressed into a fixed-size [[hidden state vector]].

Applications:
RNNs have been successfully applied to various sequential tasks, including [[Natural Language Processing (NLP)]] (language modeling, sentiment analysis, text generation), [[Machine Translation]] (Seq2Seq models), [[Speech Recognition]], [[Time Series Forecasting]] (stock price prediction, weather modeling), and [[Handwriting Recognition]].

Variants of RNNs designed to address the vanishing gradient problem include [[Long Short-Term Memory (LSTM)]] and [[Gated Recurrent Unit (GRU)]].

Comparison to Self-Attention:
While RNNs process sequences sequentially, [[Self-attention]] allows for parallel processing of all tokens simultaneously. Self-attention excels at capturing [[long-range dependency]] with direct paths, whereas RNNs' ability to capture long-range dependencies degrades with distance. However, RNNs inherently understand positional order, while self-attention requires explicit [[positional encoding]].
