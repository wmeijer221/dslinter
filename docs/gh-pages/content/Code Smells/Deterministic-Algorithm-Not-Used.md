---
title: "Deterministic Algorithm Not Used"
disableShare: true
# ShowReadingTime: true
tags: ["can be automated", "generic", "model training", "reproducibility"]
weight: 10
---

### Description

Some libraries provide APIs for developers to use the deterministic algorithm. Using deterministic algorithms is another effort that can be made to improve reproducibility. In PyTorch, it is suggested to set \textit{torch.use\_deterministic\_algorithms(True)} when debugging. However, the application will perform slower if this option is set, so it is suggested not to use it in the deploy stage. Developers should be aware of this setting during the development process.

### Type
Generic


### Existing Stage
Model Training

### Effect
Reproducibility

### Example

```python

### PyTorch
import torch

# Violated Code
# torch.use_deterministic_algorithms(True) not used

# Recommended Fix
torch.use_deterministic_algorithms(True)

```

### Source:

#### Paper 
#### Grey Literature

#### GitHub Commit

#### Stack Overflow

#### Documentation
- https://pytorch.org/docs/stable/notes/randomness.html
