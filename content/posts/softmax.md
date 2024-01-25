title: Softmax Layers are invertible unless overparametrised
date: Sunday, 25 January 2024 at 18:38

$$
\newcommand{\R}{\mathbb{R}}
\newcommand{\vv}[1]{\mathbf{ #1 }}
\newcommand{\T}{^\top}
\newcommand{\sigmoid}[1]{\operatorname{\sigma}\left( #1 \right)}
\newcommand{\softmax}[1]{\operatorname{softmax}\left( #1 \right)}
$$
In this note, I want to clarify that there is no reason why softmax layers cannot be invertible.
By invertible, I mean that given the output I can tell you what the input to the layer was.

But wait, I hear you say, the softmax function is not invertible - are we not doomed?
If you can use the implementation of the layer I specify below, no.[^1]

Below is a proof by code, read on for an explanation.

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
## Recap: Softmax function is not invertible

Recall the softmax function defined on a vector of logits $\vv{z}$:
$$
\softmax{\vv{z}}_i = \frac{e^{\vv{z}_i}}{\sum_j e^{\vv{z}_j}}
$$
Note that the output of the softmax function does not change if we offset the logits by a constant $c$:
$$
\softmax{\vv{z} + c}_i =
\frac{e^{\vv{z}_i+c}}{\sum_j e^{\vv{z}_j+c}}=
\frac{e^{c}e^{\vv{z}_i}}{e^{c}\sum_j e^{\vv{z}_j}}=
\frac{e^{\vv{z}_i}}{\sum_j e^{\vv{z}_j}}=
\softmax{\vv{z}}
$$
If we want to invert a single softmax output, we could take the log:
$$
\log \softmax{\vv{z}}_i=\log e^{\vv{z}_i} - \log \sum_j e^{\vv{z}_j} = \vv{z}_i - \log \sum_j e^{\vv{z}_j}
$$

But, we need to take account of the offset $c$.

Is there an input to the layer that when changed in isolation does not change the softmax output? Well, if the constant vector is in the columnspace, then yes. This is true if $\vv{W} \in \R^{n \times n}$ and is full rank. Softmax in this case is overparametrised: we can we rewrite $\vv{W}$ to have a columnvector of constant parameters - this column vector is redundant (see also [redundant parameters](https://mlpr.inf.ed.ac.uk/2023/notes/w6c_softmax_regression.html)).

Solution: We can remove that direction from $\vv{W}$, i.e. make all columns perpendicular to the constant vector. How? A simple way is to subtract from each column its mean.

## Claim: We can construct softmax layers such that they are invertible

A linear softmax layer is invertible when done right. It should have n rows and n-1 columns. While the constant vector will not be in the columnspace by chance, we can guarantee it is not in the columnspace by subtracting off the mean of each column of W after each update.
### Scenario
We are doing multi-class classification over $n$ output classes.
We have a linear softmax output layer, parametrised by $\vv{W} \in \R^{n \times d}$, that takes a $d$ dimensional feature vector $\vv{x} \in \R^d$ as input and outputs a categorical distribution over the classes $P(\vv{y} \mid \vv{x}) = \softmax{\vv{Wx}}$.

### Precise claim
Given $\vv{W} \in \R^{n \times d},\, d \leq n-1$ and $P(\vv{y} \mid \vv{x})$ we can recompute $\vv{x}$.

### Solution
Consider the function $f(\vv{x}) = \vv{Wx},\, \vv{W} \in \R^{n \times d}$. $f$ is a low-rank linear function, which means that its image is a subspace of $n$ dimensional space.

My claim, more precisely, is that if you tell me the parametrisation of the softmax layer, $\vv{W}$, and you give me the output probabilities over the classes $\vv{y}$, i.e. $P(\vv{y} \mid \vv{x})$ , I can tell you what the input feature vector, $\vv{x}$, was.

Up until very recently, if you asked me if a Softmax layer is invertible, I would have answered: No, the softmax function is not invertible, and therefore softmax layers cannot be invertible.

Here is why I would have been wrong.
### Softmax
Consider a linear softmax layer parametrised by $\vv{W} \in \R^{n \times d}$.
$$
P(\vv{y}_i \mid \vv{x}) = \softmax{\vv{Wx}}_i = \frac{e^{\vv{w}_i\T\vv{x}}}{\mathcal{Z}}
$$
where $\mathcal{Z}=\sum_i e^{\vv{w}_i\T\vv{x}}$.

It is straightforward to invert the last step from probabilities to log probabilities:
$$
\log P(\vv{y}_i \mid \vv{x}) = \vv{w}_i\T\vv{x} - \log \mathcal{Z}
$$
Note that each log probability is the logit offset by the log normalisation term.

[^1]: Also, if the softmax layer you are using has less inputs than outputs (i.e. the parametrisation is low rank), then again, probably no. The constant vector is unlikely to be in the columnspace of your classifier.
