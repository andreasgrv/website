title: Softmax Layers can and should be invertible
date: Sunday, 30 January 2024 at 23:32

$$
\newcommand{\R}{\mathbb{R}}
\newcommand{\vv}[1]{\mathbf{ #1 }}
\newcommand{\T}{^\top}
\newcommand{\sigmoid}[1]{\operatorname{\sigma}\left( #1 \right)}
\newcommand{\softmax}[1]{\operatorname{softmax}\left( #1 \right)}
$$


<span class="wip">Work in Progress</span>
# Invertible Softmax Layers

Suppose I tell you the parameters of a linear softmax layer and a vector of output probabilities, can you invert the layer to reconstruct its inputs?
It is commonly assumed that since the softmax function is not invertible, a softmax layer cannot be invertible.
In this note, I want to highlight that this is not true: the softmax layer implementation below is invertible and can be fully expressive.[^1]

### **TL;DR;** The softmax layer below is invertible, read on for the derivation.

```python
import torch


class InvertibleSoftmaxLayer(torch.nn.Module):
    def __init__(self, n, d=None):
        super().__init__()
        assert d <= n-1
        self.n = n
        if d is None:
            # If d is not specified we create a fully expressive softmax
            # We only need n-1 inputs for a fully expressive softmax. Why?
            # The direction [c c c ... c].T in the output space
            # is redundant, since softmax(Wx + c) = softmax(Wx).
            # As such, we can parametrise a fully expressive softmax
            # using n-1 columns in W and making sure that all columns are
            # perpendicular to constant column (subtract mean from columns)
            self.d = n - 1
        else:
            self.d = d
        self.W = torch.nn.Linear(self.d, self.n, bias=False)

    def forward(self, xx):
        # Make sure columns are perpendicular to constant vector
        # TODO: Maybe this should be a no grad operation?
        self.W.weight.data -= self.W.weight.data.mean(axis=0)
        zz = self.W(xx)
        return torch.softmax(zz, dim=1)


if __name__ == "__main__":

    torch.set_printoptions(precision=7)
    torch.manual_seed(13)

    N = 20
    D = 19
    assert D <= N - 1

    SL = InvertibleSoftmaxLayer(N, D)
    xx = torch.normal(0, .1, (1, D), dtype=torch.float32)

    # We only need D+1 outputs to reconstruct the input
    idxs = torch.multinomial(torch.ones(N)/N,
            num_samples=D+1,
            replacement=False)

    # Output probabilities
    pp = SL(xx).squeeze()
    W = SL.W.weight.data

    Wp = torch.hstack([-torch.ones((N, 1)), W])
    xxp = torch.linalg.solve(Wp[idxs, :], torch.log(pp)[idxs])
    print('Input xx:\n', xx)
    print('Reconstructed xx:\n', xxp[1:])
    # NOTE: Pytorch not as accurate as numpy:
    assert torch.allclose(xx, xxp[1:], atol=1e-4)
```

# Introduction

## Scenario
We are doing multi-class classification over $n$ output classes.
We have a linear softmax output layer, parametrised by $\vv{W} \in \R^{n \times d}$, that takes a $d$-dimensional feature vector $\vv{x} \in \R^d$ as input and outputs $P(\vv{y} \mid \vv{x}) = \softmax{\vv{Wx}}$, a categorical distribution over the classes. We limit our analysis to the common case where $d < n$.

### Problem Statement
<!-- Suppose you have a linear softmax layer parametrised by $\vv{W},\, \vv{W} \in \R^{n \times d}$, which computes the output probabilities over the classes $\vv{y}$ as $P(\vv{y} \mid \vv{x})=\softmax{\vv{Wx}}$. -->
> You are given $P(\vv{y} \mid \vv{x}')$ computed from some unknown $\vv{x}'$, as well as $\vv{W}$, which has rank $d,\, d < n$. Can you tell me what $\vv{x}'$ was?

### Result
A softmax layer parametrised by $\vv{W} \in \R^{n \times d},\, d < n$ is invertible if the constant vector $\begin{bmatrix}1 & 1 & \ldots & 1 \end{bmatrix}^\top$ is not in the columnspace of $\vv{W}$.

Two comments:

* For a random matrix, the constant column is not in the columnspace with probability 1.
* We can always parametrise $\vv{W}$ such that the above criterion holds, see code above. 

# Derivation
## Recap: The softmax function is not invertible

Recall that the softmax function defined on a vector of logits $\vv{z}$:
$$
\softmax{\vv{z}}_i = \frac{e^{\vv{z}_i}}{\sum_j e^{\vv{z}_j}}
$$
Note that the output of the softmax function does not change if we offset the logits by a constant $c$:
$$
\softmax{\vv{z} + c}_i =
\frac{e^{\vv{z}_i+c}}{\sum_j e^{\vv{z}_j+c}}=
\frac{e^{c}e^{\vv{z}_i}}{e^{c}\sum_j e^{\vv{z}_j}}=
\frac{e^{\vv{z}_i}}{\sum_j e^{\vv{z}_j}}=
\softmax{\vv{z}}_i
$$
This means that given a vector of output probabilities, we can only distinguish the inputs up to a scalar offset, and as such the softmax function is not invertible.
However, it is "nearly" invertible. There is one degree of freedom (the offset) which we cannot pin down.
We will show how to engineer the softmax parametrisation, $\vv{W}$, such that we can pin this offset down.

## Where can the constant $c$ come from?
"But what offset $c$?", I hear you say. "We computed $\vv{z} = \vv{Wx}$, there is no $c$ we need to worry about!".

Well, sometimes this is true, but what if $\vv{W}$ is a full-rank matrix?
Via a change of basis we can obtain a parametrisation that has a constant column $\vv{W}' = \begin{bmatrix}\vv{W_{:,:d-1}'} & 1\end{bmatrix}$, and then we have:
$$
\vv{W}'\vv{x} = \begin{bmatrix}\vv{W_{:,:d-1}'} & 1 \end{bmatrix} \vv{x} = \vv{W_{:,:d-1}'}\vv{x} + \vv{x}_1
$$

I.e., for such a matrix with a constant column, an input feature acts as an offset!
**Constants $c$ arise when the "constant" vector is in the columnspace of $\vv{W}$.**
As we saw, these constants do not change the softmax output, and as such the constant column vector of parameters is redundant (see also [redundant parameters](https://mlpr.inf.ed.ac.uk/2023/notes/w6c_softmax_regression.html)).
In other words, using a full-rank matrix for softmax is an overparametrisation, and it actually breaks invertability.


## Let's invert the softmax layer anyway
We set $\vv{z}' = \vv{z} + c$ for some unknown constant offset $c$.
How can we attempt to invert softmax? Well, we can expose each logit by taking the log:
$$
\log \softmax{\vv{z}'}_i=\log e^{\vv{z}'_i} - \log \sum_j e^{\vv{z}'_j} = \vv{z}'_i - \log \sum_j e^{\vv{z}'_j}
$$
where $\log \sum_j e^{\vv{z}'_j}$ is the log of the normalising constant which is the same for all logits.
Here is where knowing $\vv{W}$ can make a difference.
**Observation**: if the logits had $d \leq n-1$ degrees of freedom, we could recover the normalising constant and the input $\vv{x}$ by solving the following linear system:

$$\begin{bmatrix}\vv{W} & 1 \end{bmatrix}\vv{x} = \log \softmax{\vv{z}}$$

## Solution by construction: Remove the constant direction from $\vv{W}$

We can remove the constant direction from $\vv{W}$, i.e. make all columns perpendicular to the constant vector. How? We can subtract from each column its mean (see code).

[^1]: By fully expressive, I mean that any categorical distribution over its support can be produced.
[^2]: Also, if the softmax layer you are using has less inputs than outputs (i.e. the parametrisation is low rank), then again, probably no. The constant vector is unlikely to be in the columnspace of your classifier.
