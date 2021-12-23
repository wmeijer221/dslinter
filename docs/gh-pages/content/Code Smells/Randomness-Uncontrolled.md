---
title: "Randomness Uncontrolled"
disableShare: true
# ShowReadingTime: true
tags: ["can be automated","generic","reproducibility"]
weight: 1
---

### Description

Debugging is easier if the results are reproducible when developing ML systems. Also, reproducibility helps conduct studies based on previous models. Setting random seeds significantly contributes to the reproducibility of ML applications. There are several scenes that a random seed is involved. In Scikit-Learn, randomness is inherently involved in some estimators(e.g., Random Forest) and cross-validation splitters. If the random seed is not set, the random forest algorithm might provide a different result every time it runs, and the dataset split by cross-validation splitter will also be different next time it runs \ref{grey:sklearn_best_practice}. In Pytorch and Numpy, it is also recommended to set global random seed first for reproducible result \ref{grey:pytorch_randomness}. Specifically, \textit{DataLoader} in PyTorch needs the setting of random seed to ensure the data splitted and loaded in the same way every time running the code. In various grey literature \ref{grey:ml_perfect}, \ref{grey:pytorch_randomness}, the importance of setting random seed is noted. Therefore, we suggest the developers set random seed explicitly during the development process whenever a possible random procedure is involved in the application.


### Type

Generic

### Existing Stage

General

### Effect

Reproducibility

### Example

```python

### python in general

# Violated Code
# random seed not set

# Recommended Fix
import random
random.seed(0)

### Tensorflow

# Violated Code
# random seed not set

# Recommended Fix
import tensoflow as tf
tf.random.set_seed(0)

### PyTorch

# Violated Code
# random seed not set

# Recommended Fix
import torch
torch.manual_seed(0)

### Scikit-Learn
from sklearn.model_selection 
import KFold

# Violated Code
kf = KFold(random_state=None)

# Recommended Fix
rng = 0
kf = KFold(random_state=rng)

### NumPy

# Violated Code
# random seed not set

# Recommended Fix
import numpy as np
np.random.seed(0)

```

### Source:

#### Paper 

#### Grey Literature
- https://towardsdatascience.com/my-machine-learning-model-is-perfect-9a7928e0f604
- https://github.com/IgorSusmelj/pytorch-styleguide

#### GitHub Commit

#### Stack Overflow
- https://stackoverflow.com/questions/57416925/best-practices-for-generating-a-random-seeds-to-seed-pytorch

#### Documentation
- https://pytorch.org/docs/stable/notes/randomness.html
