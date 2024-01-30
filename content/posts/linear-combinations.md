title: Linear combinations, an illustrated pseudo-3D tale
date: Monday, 21 October 2019 at 01:18

{% set BLUE = '1f78b4' %}
{% set GREEN = '33a02c' %}
{% set RED = 'e31a1c' %}
{% set ORANGE = 'ff7f00' %}
{% set PURPLE = '6a3d9a' %}

$$
\require{color}
\require{newcommand}
\definecolor{myblue}{RGB}{ {{ BLUE | hex_to_rgb }} }
\definecolor{mygreen}{RGB}{ {{ GREEN | hex_to_rgb }} }
\definecolor{myred}{RGB}{ {{ RED | hex_to_rgb }} }
\definecolor{myorange}{RGB}{ {{ ORANGE | hex_to_rgb }} }
\definecolor{mypurple}{RGB}{ {{ PURPLE | hex_to_rgb }} }
\def\xa{ {\color{myblue} x_1} }
\def\xb{ {\color{mygreen} x_2} }
\def\xc{ {\color{myorange} x_3} }
\def\yy{ {\color{mypurple} y} }
$$

{% set sumlabel = '<svg width="25.12027pt" height="25.53891pt" viewBox="-72 -72 30.12027 24.53891" style="overflow: visible; position: relative;"><g transform="translate(-53.730712890624986,-60.689086914062486) scale(1,-1)"><g> <g stroke="rgb(0.0%,0.0%,0.0%)"> <g fill="rgb(0.0%,0.0%,0.0%)"> <g stroke-width="0.4pt"> <g> <g> <g stroke="rgb(100.0%,0.0%,0.0%)"> <g fill="rgb(100.0%,0.0%,0.0%)"> <g stroke="rgb(0.0%,0.0%,0.0%)"> <path d=" M  0.0 0.0 L  11.38092 0.0 C  11.38092 6.28558 6.28558 11.38092 0.0 11.38092 Z  "></path> </g> </g> </g> </g> <g> <g stroke="rgb(0.0%,0.0%,100.0%)"> <g fill="rgb(0.0%,0.0%,100.0%)"> <g stroke="rgb(0.0%,0.0%,0.0%)"> <path d=" M  0.0 0.0 L  0.0 11.38092 C  -4.06552 11.38092 -7.82352 9.21121 -9.85619 5.69046 C  -11.19388 3.3735 -11.67264 0.65852 -11.20811 -1.97623 Z  "></path> </g> </g> </g> </g> <g> <g stroke="rgb(0.0%,100.0%,0.0%)"> <g fill="rgb(0.0%,100.0%,0.0%)"> <g stroke="rgb(0.0%,0.0%,0.0%)"> <path d=" M  0.0 0.0 L  -11.20813 -1.97583 C  -10.7436 -4.61058 -9.36491 -6.99825 -7.31557 -8.7178 Z  "></path> </g> </g> </g> </g> <g> <g stroke="rgb(100.0%,50.0%,0.0%)"> <g fill="rgb(100.0%,50.0%,0.0%)"> <g stroke="rgb(0.0%,0.0%,0.0%)"> <path d=" M  0.0 0.0 L  -7.31549 -8.71782 C  -2.50063 -12.758 4.67809 -12.13004 8.71826 -7.31517 C  10.43782 -5.26582 11.38098 -2.675 11.38098 0.00038 Z  "></path> </g> </g> </g> </g> </g> </g> </g> </g> </g> </g></svg>' %}
{% set poslabel = '<i class="fa fa-plus" style="font-size: 30px; padding-left: .25em; color: #555555;"></i>' %}

## Introduction

In this writeup, I will go over some visualisations I made to help me better understand some rudimentary mathematical concepts from the course of [Convex Optimisation](https://web.stanford.edu/~boyd/cvxbook/) by Stephen Boyd.
I have attempted to use optical illusions, also known as 3D plots, to try to visualise these sets in a bit more detail than possible in [Flatland](https://en.wikipedia.org/wiki/Flatland).

The introduction in the <a href="https://web.stanford.edu/~boyd/cvxbook/" target="_blank">book</a> explains how to create [affine](#Affine sets), [convex](#Convex sets) and [conic](#Conic sets) sets using linear combinations. All the aforementioned sets are expressed as a [linear combination](https://en.wikipedia.org/wiki/Linear_combination) of some seed vectors $x_i$ in $\mathbb{R}^n$ using scalar coefficients $\theta$ in $\mathbb{R}$.

The general form of the generator equation for these sets is $$\yy=\theta_1 \xa + \theta_2 \xb + \ldots + \theta_n x_n$$

A set is thus constructed by plugging in all possible $\theta_i$'s to obtain all possible $\yy$'s.
The way in which the sets discussed will differ, is in the values we allow the $\theta_i$'s to take on. Constraints on the coefficients $\theta_i$ we will work with are:

<!-- <script type="text/tikz"> -->
<!-- 	\def\sector#1#2#3#4#5{\fill[#5] (#1) -- (#3:#2) arc (#3:#4:#2) -- cycle;} -->
<!-- 	\xdef\r{.35} -->
<!-- 	\begin{tikzpicture} -->
<!-- 		\sector{0,0}{\r}{0}{90}{color=red, draw=black} -->
<!-- 		\sector{0,0}{\r}{90}{190}{color=blue, draw=black} -->
<!-- 		\sector{0,0}{\r}{190}{230}{color=green, draw=black} -->
<!-- 		\sector{0,0}{\r}{230}{360}{color=orange, draw=black} -->
<!-- 	\end{tikzpicture} -->
<!-- </script> -->


Constraint on $\theta_i$   | Equation                          | Symbol
-------------------------- | --------------------------------  | -----------
Sum to 1                   | $\sum_{i}\theta_i = 1$          |  {{ sumlabel | safe }}
Non-negative               | $\theta_i \geq 0 \quad \forall i$ | {{ poslabel | safe }}

We shall refer to these constraints using the symbols in the last column, which are hopefully intuitive. For all visualisations below, the $x_i$'s will be in $\mathbb{R}^3$.
I will use unit vectors for $\xa$, $\xb$ and $\xc$, but the same plots could have been drawn for arbitrary vectors.
<a id='Affine sets'></a>
##Affine sets {{ sumlabel | safe }}

As hinted by the symbol following the title, we get affine sets if we only impose that $\theta_i$'s sum to $1$. 
If we have two vectors $\xa, \xb$ in $\mathbb{R}^3, \xa \ne \xb$, then for any scalar values $\theta_i$
\begin{align}
	\yy&=\theta_1 \xa + \theta_2 \xb, \quad \text{where} \quad \theta_1 + \theta_2 = 1 \\\\
	   &=\theta_1 \xa + (1 - \theta_1) \xb
\end{align}

$\yy$ will be in the affine set, the line that passes through the head of vectors $\xa$ and $\xb$. The points $\yy$ can be generated by scaling vector $\xa$ by $\theta_1$ and then
adding that vector to the result of scaling $\xb$ by $(1-\theta_1)$. This combination of vectors is visualised using dotted vectors below.

![affine set]({{ url_for('static', filename='images/posts/affine2d.png') }})

However, while this visual construction shows how the points created when choosing $\theta_1$ in such a way lie on a line, the result is more complex than it needs to be.
This is so since we are still bestowing upon $\theta_2 = 1 - \theta_1$ and $\theta_1$ the priviledge of free parameters, when in reality $\theta_2$ is powerless, there is only one free parameter because of the constraint.

A clearer way to see the affine set, is to regroup the terms containing $\theta_1$.

\begin{align}
\yy &=\theta_1 \xa + (1 - \theta_1) \xb \\\\
& =\theta_1 \xa + \xb - \theta_1\xb \\\\
& =\xb + \theta_1 (\xa - \xb)
\end{align}

After this algebraic manipulation, we get a much clearer visual understanding of the situation.
We compute the vector $\xa - \xb$, which we scale using all possible values of $\theta_1$.
We then offset the result by $\xb$ to get all possible points on the line, the affine set. 

![affine set diff]({{ url_for('static', filename='images/posts/affine2d-diff.png') }})

In the case where we have 3 non collinear vectors, the situation generalizes as follows:

\begin{align}
\yy &=\theta_1 \xa + \theta_2 \xb + (1 - \theta_1 - \theta_2) \xc \\\\
    &=\theta_1 \xa + \theta_2 \xb + \xc - \theta_1 \xc - \theta_2 \xc \\\\
    &=\theta_1 (\xa - \xc) + \theta_2 (\xb - \xc) + \xc
\end{align}

This time we calculate two differences, $\xa - \xc$ and $\xb - \xc$. We notice that taking all linear combinations of these vectors, $\theta_1 (\xa - \xc) + \theta_2 (\xb - \xc)$
fill the semi-transparent brownish plane.
![affine set plane linear combination]({{ url_for('static', filename='images/posts/affine3d.png') }})

Now, if we offset this plane by $\xc$, we generate our target affine set. Something that is clearer from the plot than the equations, is that we could actually offset the plane by any of the vectors $\xa$, $\xb$ or $\xc$ and still get the target affine set. Depending on which vector is used, each point from the brownish plane through the origin $O$ will get offset to a different point on the plane. However, the plane has infinite points, so the difference would be indistinguishable.

![affine set plane]({{ url_for('static', filename='images/posts/affine3dsurf.png') }})

<a id="Convex sets"></a>
##Convex sets {{ sumlabel | safe }} {{ poslabel | safe }}

For convex sets, we can continue from where we left off with the affine set.
	   $$\yy=\xb + \theta_1 (\xa - \xb)$$
However, for a convex set we further constrain the thetas to be positive. Constraining $\theta_1$ to be positive, limits the range of vectors we can produce when scaling $\xa - \xb$ by $\theta_1$, as can be seen in the plot below.
This means, the vectors in our set lie on a line segment joining $\xb$ and $\xa$.

![convex line]({{ url_for('static', filename='images/posts/convex2d.png') }})

In the 3D case:
$$\yy=\theta_1 (\xa - \xc) + \theta_2 (\xb - \xc) + \xc$$
we are constrained to a 2-simplex (triangle).

![convex plane]({{ url_for('static', filename='images/posts/convex3d.png') }})

As before, we can add the offset $\xc$. Note, however, that in this case we can only offset by $\xc$ if we want to get the target convex set.

![convex plane 3D]({{ url_for('static', filename='images/posts/convex3dsurf.png') }})

<a id="Conic sets"></a>
## Conic sets {{ poslabel | safe }}


For Conic sets we only have the constraint that $\theta_i$'s should be positive. So for the 2D case:
   $$\yy=\theta_1 \xa + \theta_2 \xb, \quad \theta_1,\theta_2 \geq 0$$
our two parameters, $\theta_1$ and $\theta_2$, are not entangled through some constraint, but are both required to take values in the positive quadrant of $\mathbb{R}^2$.
Therefore, we can only combine our seed vectors $\xa$ and $\xb$ to get $\yy$ in ways that "remain between" the two vectors.

![conic set 2D]({{ url_for('static', filename='images/posts/conic2d.png') }})

For the 3D case

   $$\yy=\theta_1 \xa + \theta_2 \xb + \theta_3 \xc, \quad \theta_1,\theta_2, \theta_3 \geq 0$$

we can offset the current set using $\xc$ scaled by positive values of $\theta_3$.

![conic set 3D]({{ url_for('static', filename='images/posts/conic3d.png') }})

<!-- ## Conclusion -->
<!--  -->
<!-- Set                        | Constraints -->
<!-- -------------------------- | ----------- -->
<!-- Affine set                 | {{ sumlabel | safe }} -->
<!-- Convex set                 | {{ sumlabel | safe }} {{ poslabel | safe }} -->
<!-- Conic set                  | {{ poslabel | safe }} -->
